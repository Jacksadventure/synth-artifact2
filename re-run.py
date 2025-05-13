#!/usr/bin/env python3
"""
update_repairs_method.py
------------------------------------------------------------
Re-runs or overwrites repair results for ONE algorithm
(e.g. DDMax, DDMaxG, erepair, Antlr).

Typical use
-----------
# re-run DDMax only for the rows where it has never been tried
python update_repairs_method.py -m DDMax -o result10.db

# re-run DDMax for *all* rows, overwriting old values (using 4 processes)
python update_repairs_method.py -m DDMax -o result10.db --force -j 4

# re-run Antlr, but only on formats json and ini
python update_repairs_method.py -m Antlr -f json ini -o result10.db

# re-run Antlr for the format associated with the 'cjson' executable,
# potentially using its CIL file if the Antlr command is configured for it.
python update_repairs_method.py -m Antlr --cil path/to/cjson.cil -o result10.db
"""
from __future__ import annotations
import argparse, os, random, re, sqlite3, subprocess, textwrap, time
from pathlib import Path
from typing import List, Tuple, Optional, Any
import multiprocessing # Added for multiprocessing

# ───────────────────────── copied-verbatim config ───────────────────────── #
ALL_MUTATION_DBS = {
    "dot":  "mutated_files/double_dot.db",
    "json": "mutated_files/double_json.db",
    "ini":  "mutated_files/double_ini.db",
    "lisp": "mutated_files/double_lisp.db",
    "obj":  "mutated_files/double_obj.db",
}
PROJECT_PATHS = {
    "json": "/Users/jack/fsynth-artifact/project/bin/subjects/cjson/cjson",
    "ini":  "/Users/jack/fsynth-artifact/project/bin/subjects/ini/ini",
    "lisp": "/Users/jack/fsynth-artifact/project/bin/subjects/sexp-parser/sexp",
    "dot":  "/Users/jack/fsynth-artifact/project/bin/subjects/dot/build/dot_parser",
    "obj":  "/Users/jack/fsynth-artifact/project/bin/subjects/obj/build/obj_parser"
}
REPAIR_ALGORITHMS = ["DDMax", "erepair", "DDMaxG", "Antlr"]

ALGORITHM_CMDS = {
    "erepair": [ "java", "-jar", "./project/bin/erepair.jar", "-r", "-a", "erepair",
                 "-i", "{infile}", "-o", "{outfile}"],
    "DDMax":   ["java", "-jar", "./project/bin/erepair.jar", "-r", "-a", "DDMax",
                 "-i", "{infile}", "-o", "{outfile}"],
    "DDMaxG":  ["java", "-jar", "./project/bin/erepair.jar", "-r", "-a", "DDMaxG",
                 "-i", "{infile}", "-o", "{outfile}"],
    "Antlr":   ["java", "-jar", "./project/bin/erepair.jar", "-r", "-a", "Antlr",
                 "-i", "{infile}", "-o", "{outfile}"],
    # Example of how Antlr might use a cilfile if erepair.jar supported it:
    # "Antlr":   ["java", "-jar", "./project/bin/erepair.jar", "-r", "-a", "Antlr",
    #              "-i", "{infile}", "-o", "{outfile}", "--grammar-or-cil", "{cilfile}"],
}
VALIDATION_TIMEOUT = 30
REPAIR_TIMEOUT     = 240
REPAIR_OUTPUT_DIR  = "repair_results"
# Main process creates this, workers use it.
if multiprocessing.current_process().name == 'MainProcess':
    os.makedirs(REPAIR_OUTPUT_DIR, exist_ok=True)
# ──────────────────────────────────────────────────────────────────────────── #

def lev(a: str, b: str) -> int:
    """Levenshtein distance (no external deps)."""
    if a == b:          return 0
    if not a:           return len(b)
    if not b:           return len(a)
    prev = list(range(len(b) + 1))
    for ca in a:
        cur = [prev[0] + 1]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[-1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]

def validate(path: str, fmt: str) -> bool:
    exe = PROJECT_PATHS.get(fmt)
    if not exe:
        # Print to stderr for worker processes so it's more noticeable
        print(f"Process {os.getpid()}: Error: No project path defined for format '{fmt}'. Cannot validate.", file=os.sys.stderr)
        return False
    try:
        res = subprocess.run([exe, path], stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, timeout=VALIDATION_TIMEOUT)
        return res.returncode == 0
    except Exception as e:
        print(f"Process {os.getpid()}: Error during validation for {path} with format {fmt}: {e}", file=os.sys.stderr)
        return False

def oracle_info(out: bytes) -> Tuple[int,int,int,int]:
    txt = out.decode(errors="ignore")
    m = re.search(r"oracle runs: (\d+) correct: (\d+) incorrect: (\d+) incomplete: (\d+)", txt)
    return tuple(map(int, m.groups())) if m else (0,0,0,0)

# This function will be executed by worker processes
def worker_repair_and_update(db_path: str, row_tuple: Tuple,
                             idx: int, total_rows_overall: int, alg: str,
                             cil_file_path_for_tool: Optional[str]) -> None:
    # Unpack row_tuple; ensure the order matches how it was packed
    # Original SELECT * might have many columns, ensure these are the ones needed
    # (rid, fmt, fid, cidx, _alg_from_db, orig, broken, rep_from_db, fixed_from_db, *_rest) = row
    # Let's assume row_tuple is (id, format, original_text, broken_text, repaired_text_from_db)
    # We need: id, format, original_text, broken_text, repaired_text_from_db
    # The full row is passed as a tuple, so indices match sqlite3.Row
    rid, fmt, _fid, _cidx, _alg_from_db, orig, broken, rep_from_db, _fixed_from_db = row_tuple[:9] # Adapt if schema changes

    # Per-process output prefix
    proc_prefix = f"[P{os.getpid()}]"

    if fmt not in PROJECT_PATHS:
        print(f"{proc_prefix} [SKIPPING] row {rid}: Format '{fmt}' has no defined project path. Cannot validate or repair.", file=os.sys.stderr)
        return

    # Unique temporary filenames using rid and process ID for safety
    rand_suffix = random.randint(0,99999)
    infile_path_str  = f"tmp_{rid}_{os.getpid()}_{rand_suffix}.{fmt}"
    outfile_name = f"rep_{rid}_{os.getpid()}_{rand_suffix}.{fmt}" # Make outfile unique per attempt too
    outfile_path = Path(REPAIR_OUTPUT_DIR) / outfile_name
    infile_path = Path(infile_path_str) # Usually in CWD, ensure this is fine

    try:
        infile_path.write_text(broken, encoding="utf-8")
    except Exception as e:
        print(f"{proc_prefix} Error writing temporary input file {infile_path} for row {rid}: {e}", file=os.sys.stderr)
        return

    cmd_template = ALGORITHM_CMDS[alg]
    formatter_kwargs = {
        "infile": str(infile_path),
        "outfile": str(outfile_path),
        "fmt_exe": PROJECT_PATHS.get(fmt, ""),
        "cilfile": str(cil_file_path_for_tool) if cil_file_path_for_tool else ""
    }
    cmd = [part.format(**formatter_kwargs) for part in cmd_template]

    dist_ob = lev(orig, broken)
    dist_br = -1
    dist_or = -1
    iters = cor = incor = incom = 0
    
    repaired_text_content = rep_from_db if rep_from_db is not None else broken
    current_fixed_status = 0
    elapsed = 0.0

    try:
        start_time = time.monotonic()
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = proc.communicate(timeout=REPAIR_TIMEOUT)
        elapsed = time.monotonic() - start_time

        if proc.returncode != 0:
            print(f"{proc_prefix} [WARN] Repair process for row {rid} (alg {alg}, fmt {fmt}) exited with code {proc.returncode}.", file=os.sys.stderr)
            if stderr:
                print(f"{proc_prefix}        Stderr: {stderr.decode(errors='ignore').strip()}", file=os.sys.stderr)
        
        iters_info = oracle_info(stdout)
        iters,cor,incor,incom = iters_info

        if outfile_path.exists() and outfile_path.stat().st_size >= 0:
            try:
                repaired_text_content = outfile_path.read_text(encoding="utf-8", errors="ignore")
                if validate(str(outfile_path), fmt):
                    current_fixed_status = 1
                else:
                    current_fixed_status = 0
                dist_br = lev(broken, repaired_text_content)
                dist_or = lev(orig, repaired_text_content)
            except Exception as e:
                print(f"{proc_prefix} Error reading/processing output file {outfile_path} for row {rid}: {e}", file=os.sys.stderr)
                repaired_text_content = rep_from_db if rep_from_db is not None else broken
                current_fixed_status = 0
        else:
            # print(f"{proc_prefix} [WARN] Output file {outfile_path} not found or empty for row {rid}. Assuming repair failed.", file=os.sys.stderr)
            repaired_text_content = rep_from_db if rep_from_db is not None else broken
            current_fixed_status = 0

    except subprocess.TimeoutExpired:
        elapsed = REPAIR_TIMEOUT # Ensure elapsed reflects timeout
        print(f"{proc_prefix} [TIMEOUT] row {rid} for algorithm {alg}, format {fmt}", file=os.sys.stderr)
        repaired_text_content = rep_from_db if rep_from_db is not None else broken
        current_fixed_status = 0
    except Exception as e:
        print(f"{proc_prefix} An unexpected error during repair for row {rid} (alg {alg}, fmt {fmt}): {e}", file=os.sys.stderr)
        repaired_text_content = rep_from_db if rep_from_db is not None else broken
        current_fixed_status = 0
    finally:
        for p_obj in [infile_path, outfile_path]:
            if p_obj.exists():
                try:
                    os.remove(p_obj)
                except OSError as e:
                    print(f"{proc_prefix} Warning: could not remove temporary file {p_obj}: {e}", file=os.sys.stderr)

    # Database connection per worker
    conn_worker = None
    try:
        # It's crucial that WAL mode is enabled for concurrent writes from multiple processes.
        # Or, ensure that writes are serialized if not using WAL or if high contention.
        # For simplicity, we'll assume WAL is enabled on the DB or accept potential "database is locked"
        # errors if multiple processes try to commit at the exact same microsecond without WAL.
        # A short random sleep before commit can sometimes mitigate this in non-WAL scenarios, but WAL is better.
        conn_worker = sqlite3.connect(db_path, timeout=10) # Add timeout for busy DB
        cur_worker = conn_worker.cursor()
        
        # Short delay to reduce simultaneous commit attempts if not in WAL mode
        # time.sleep(random.uniform(0.01, 0.1))

        cur_worker.execute(textwrap.dedent("""\
            UPDATE results SET repaired_text=?, fixed=?, iterations=?, repair_time=?,
                   correct_runs=?, incorrect_runs=?, incomplete_runs=?,
                   distance_original_broken=?, distance_broken_repaired=?,
                   distance_original_repaired=? WHERE id=?"""),
            (repaired_text_content, current_fixed_status, iters, elapsed, cor, incor, incom,
             dist_ob, dist_br, dist_or, rid))
        conn_worker.commit()
        print(f"{proc_prefix} [{idx:04}/{total_rows_overall}] {fmt:<4} {alg:<6} fixed={current_fixed_status} t={elapsed:4.1f}s iters={iters} Oracle(C/I/Inc):{cor}/{incor}/{incom} DB_ID:{rid} -> Updated")
    except sqlite3.Error as e:
        print(f"{proc_prefix} DB Error for row {rid}: {e}. Data: fixed={current_fixed_status}, time={elapsed:.1f}", file=os.sys.stderr)
        if conn_worker:
             conn_worker.rollback() # Rollback on error
    finally:
        if conn_worker:
            conn_worker.close()


def run_updates(db_path: str, alg: str, formats: Optional[List[str]],
                force: bool, failed_only: bool,
                cil_file_path_for_tool: Optional[str],
                num_processes: int) -> None: # Added num_processes
    conn_main = sqlite3.connect(db_path)
    conn_main.row_factory = sqlite3.Row # For the main thread's fetching
    cur_main = conn_main.cursor()

    # Enable WAL mode for better concurrency if this script is the primary writer
    # Do this once in the main process.
    try:
        cur_main.execute("PRAGMA journal_mode=WAL;")
        print("[INFO] Attempted to set WAL mode for the database.")
    except sqlite3.Error as e:
        print(f"[WARN] Could not set WAL mode: {e}. Concurrent writes might be slow or error-prone.", file=os.sys.stderr)


    where_clauses: List[str] = ["algorithm=?"]
    params: List[Any] = [alg]

    if formats:
        placeholders = ','.join('?' * len(formats))
        where_clauses.append(f"format IN ({placeholders})")
        params.extend(formats)

    if force:
        pass
    elif failed_only:
        where_clauses.append("fixed=0")
    else:
        where_clauses.append("repair_time=0")

    sql_query = f"SELECT * FROM results WHERE {' AND '.join(where_clauses)}"
    
    try:
        cur_main.execute(sql_query, params)
    except sqlite3.OperationalError as e:
        print(f"Error executing SQL query: {sql_query} with params: {params}", file=os.sys.stderr)
        print(f"SQLite error: {e}", file=os.sys.stderr)
        conn_main.close()
        return
        
    rows_to_process = cur_main.fetchall()
    conn_main.close() # Close main connection after fetching
    
    total_to_process = len(rows_to_process)
    
    if total_to_process == 0:
        filter_desc = ""
        if formats:
            filter_desc += f" for formats {', '.join(formats)}"
        
        run_condition_desc = ""
        if force:
            run_condition_desc = " (forced re-run, ignoring previous state)"
        elif failed_only:
            run_condition_desc = " (targeting only previously failed [fixed=0] attempts)"
        else:
            run_condition_desc = " (targeting only not-yet-attempted [repair_time=0] rows)"
        
        print(f"[INFO] No rows match the criteria for algorithm {alg}{filter_desc}{run_condition_desc}. Nothing to do.")
        
        if not force and not failed_only:
            suggestions = [
                f"       - If you intended to re-run all matching '{alg}' rows{filter_desc} regardless of past attempts, use the --force option.",
                f"       - If you intended to re-run only those that were attempted but failed (fixed=0), use the --failed-only option.",
                f"       - Otherwise, this means all relevant rows have already been attempted at least once."
            ]
            print("\n".join(suggestions))
        return

    print(f"[UPDATE] {total_to_process} rows will be processed for algorithm {alg}" +
          (f" in formats: {', '.join(formats)}" if formats else " (all applicable formats)"))

    # Prepare arguments for worker_repair_and_update
    # Pass row as a tuple because sqlite3.Row objects might not be perfectly pickleable
    # or might behave unexpectedly across process boundaries. Tuples are safe.
    tasks_args = [
        (db_path, tuple(r), i + 1, total_to_process, alg, cil_file_path_for_tool)
        for i, r in enumerate(rows_to_process)
    ]

    actual_num_processes = min(num_processes, total_to_process) # Don't start more processes than tasks
    if actual_num_processes <= 0: actual_num_processes = 1 # Ensure at least one process

    if actual_num_processes > 1 and total_to_process > 1:
        print(f"[INFO] Using {actual_num_processes} parallel processes (max requested: {num_processes}).")
        # Make sure REPAIR_OUTPUT_DIR exists before pool starts workers that might use it
        os.makedirs(REPAIR_OUTPUT_DIR, exist_ok=True)
        with multiprocessing.Pool(processes=actual_num_processes) as pool:
            try:
                # starmap applies function with arguments from each tuple in tasks_args
                pool.starmap(worker_repair_and_update, tasks_args)
            except Exception as e:
                print(f"A critical error occurred in the multiprocessing pool: {e}", file=os.sys.stderr)
                # Consider how to handle partial completion or errors from workers.
                # `starmap` will raise the first exception it encounters from a worker.
    else:
        print("[INFO] Running in single-process mode.")
        # Make sure REPAIR_OUTPUT_DIR exists
        os.makedirs(REPAIR_OUTPUT_DIR, exist_ok=True)
        for task_arg_tuple in tasks_args:
            worker_repair_and_update(*task_arg_tuple)
    
    print(f"[INFO] Finished processing {total_to_process} rows.")


def get_format_from_cil(cil_path_str: str) -> Optional[str]:
    cil_path = Path(cil_path_str)
    cil_stem = cil_path.stem 

    for fmt_key, exe_path_str in PROJECT_PATHS.items():
        exe_name = Path(exe_path_str).name 
        if cil_stem == exe_name:
            return fmt_key 
    return None

def cli() -> None:
    doc_parts = (__doc__ or "").split("Typical use\n-----------", 1)
    typical_use_epilog = textwrap.dedent(doc_parts[1]) if len(doc_parts) > 1 else ""

    p = argparse.ArgumentParser(
        description="Re-run / overwrite repair results for a single algorithm. "
                    "Specify target format(s) using --formats or --cil.",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog=f"Typical use\n-----------\n{typical_use_epilog}"
    )
    p.add_argument('-m','--method', required=True, choices=REPAIR_ALGORITHMS,
                   help="Which repair algorithm to (re)run.")
    p.add_argument('-o','--result-db', default="result10.db",
                   help="SQLite DB you want to update (default: result10.db).")
    p.add_argument('-j', '--num-processes', type=int, default=os.cpu_count(),
                   help=f"Number of parallel processes to use (default: {os.cpu_count()} CPU cores). Use 1 for no parallelism.")


    format_selection_group = p.add_mutually_exclusive_group(required=False)
    format_selection_group.add_argument(
        '-f','--formats', nargs='*', 
        choices=list(ALL_MUTATION_DBS.keys()),
        default=None, 
        help="Restrict to these formats only (e.g., json ini).\n"
             "If neither --formats nor --cil is given, runs on all applicable formats."
    )
    format_selection_group.add_argument(
        '--cil', type=str, default=None,
        help="Path to a CIL file (e.g., subjects/cjson/cjson.cil).\n"
             "The format is derived by matching the CIL filename's stem\n"
             "(e.g., 'cjson' from 'cjson.cil') against known project executable names.\n"
             "The CIL file path may also be passed to the repair tool if its command\n"
             "template in ALGORITHM_CMDS uses the {cilfile} placeholder."
    )

    condition_group = p.add_mutually_exclusive_group()
    condition_group.add_argument('--force', action='store_true',
                                 help="Re-run regardless of previous state (overwrite existing results).")
    condition_group.add_argument('--failed-only', action='store_true',
                                 help="Re-run only rows where 'fixed=0'.")
    
    args = p.parse_args()

    selected_formats: Optional[List[str]] = None 
    actual_cil_path: Optional[str] = None

    if args.cil:
        actual_cil_path = args.cil 
        cil_file_path_obj = Path(args.cil)
        if not cil_file_path_obj.is_file():
            p.error(f"CIL file not found: {args.cil}")

        derived_format = get_format_from_cil(args.cil)
        if derived_format:
            if derived_format not in ALL_MUTATION_DBS:
                p.error(f"Format '{derived_format}' derived from CIL file '{args.cil}' is not a known runnable format "
                        f"in ALL_MUTATION_DBS. Known formats: {', '.join(ALL_MUTATION_DBS.keys())}")
            selected_formats = [derived_format]
            print(f"[INFO] Format derived from CIL file '{args.cil}': {derived_format}")
        else:
            executable_names = sorted(list(set(Path(p_path).name for p_path in PROJECT_PATHS.values())))
            p.error(f"Could not determine format from CIL file '{args.cil}'.\n"
                    f"Ensure the CIL filename (e.g., 'cjson' from 'cjson.cil') matches one of these executable names:\n"
                    f"{', '.join(executable_names)}")
    elif args.formats is not None: 
        if not args.formats: 
            p.error("Argument -f/--formats: expected one or more format names. Example: -f json ini")
        selected_formats = args.formats
        print(f"[INFO] Running for specified formats: {', '.join(selected_formats)}")
    else:
        print("[INFO] No specific format filter given; will process rows for all applicable formats.")

    if not Path(args.result_db).exists():
        p.error(f"Result database not found: {args.result_db}")

    run_updates(args.result_db, args.method, selected_formats, 
                args.force, args.failed_only, actual_cil_path,
                args.num_processes)

if __name__ == "__main__":
    # On Windows, pool creation needs to be guarded by if __name__ == "__main__":
    # It's good practice on all platforms.
    multiprocessing.freeze_support() # For Windows frozen executables, no-op elsewhere
    cli()