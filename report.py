import sqlite3
import math
from typing import Tuple

# Paths to SQLite databases
DATABASES = ["multiple.db", "truncated.db", "single.db"]
DEFAULT_TIMEOUT = 240.0  # Default time (4 minutes) for missing repair times

def calculate_and_display_detailed_metrics():
    """
    Calculate and display detailed metrics in table-like structures for:
    1. Each database separately.
    2. Combined results across all databases.
    """
    combined_data = {}
    
    for db_path in DATABASES:
        print(f"\nProcessing database: {db_path}")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Query to get all attempts (both successful and unsuccessful repairs)
        cursor.execute("""
            SELECT 
                format,
                algorithm,
                distance_original_broken,
                distance_broken_repaired,
                distance_original_repaired,
                fixed = 1 AS is_successful,
                IFNULL(repair_time, ?) AS repair_time
            FROM results
        """, (DEFAULT_TIMEOUT,))
        
        # Organize data by format and algorithm
        data = {}
        for row in cursor.fetchall():
            format_, algorithm, dist_ob, dist_br, dist_or, is_successful, repair_time = row
            key = (format_, algorithm)
            if key not in data:
                data[key] = {
                    "broken_repaired": [],
                    "original_repaired": [],
                    "repair_times": [],
                    "successful_times": [],
                    "total_attempts": 0,
                    "successes": 0
                }
            data[key]["total_attempts"] += 1
            data[key]["repair_times"].append(repair_time)
            if is_successful:
                data[key]["broken_repaired"].append(dist_br)
                data[key]["original_repaired"].append(dist_or)
                data[key]["successful_times"].append(repair_time)
                data[key]["successes"] += 1
            
            # Merge data across databases for combined statistics
            if key not in combined_data:
                combined_data[key] = {
                    "broken_repaired": [],
                    "original_repaired": [],
                    "repair_times": [],
                    "successful_times": [],
                    "total_attempts": 0,
                    "successes": 0
                }
            combined_data[key]["total_attempts"] += 1
            combined_data[key]["repair_times"].append(repair_time)
            if is_successful:
                combined_data[key]["broken_repaired"].append(dist_br)
                combined_data[key]["original_repaired"].append(dist_or)
                combined_data[key]["successful_times"].append(repair_time)
                combined_data[key]["successes"] += 1

        conn.close()
        
        # Display results per database
        display_metrics(data, f"Metrics for {db_path}")
    
    # Display combined results
    display_metrics(combined_data, "Combined Metrics Across All Databases")
    

def all_distances():
    data = {}
    
    for db in DATABASES:
        conn = sqlite3.connect(db)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                algorithm,
                distance_broken_repaired,
                distance_original_repaired
            FROM results
            WHERE fixed = 1
        """)
        
        for row in cursor.fetchall():
            algorithm, dist_br, dist_or = row
            if algorithm not in data:
                data[algorithm] = {"broken_repaired": [], "original_repaired": []}
            
            if dist_br >= 0:
                data[algorithm]["broken_repaired"].append(dist_br)
            if dist_or >= 0:
                data[algorithm]["original_repaired"].append(dist_or)
        
        conn.close()
    
    def calculate_stats(values):
        values = [float(v) for v in values if v is not None]  # 添加 float 转换
        n = len(values)
        mean = sum(values) / n if n > 0 else 0
        stdev = math.sqrt(sum((x - mean) ** 2 for x in values) / n) if n > 1 else 0
        return mean, stdev
    
    print("\nOverall Distance Metrics Across All Databases")
    print("-" * 80)
    print(f"{'Algorithm':<15} {'Avg BR':<10} {'Stdev BR':<10} {'Avg OR':<10} {'Stdev OR':<10}")
    print("-" * 80)
    
    for algorithm, metrics in data.items():
        avg_br, stdev_br = calculate_stats(metrics["broken_repaired"])
        avg_or, stdev_or = calculate_stats(metrics["original_repaired"])
        
        print(f"{algorithm:<15} {avg_br:<10.2f} {stdev_br:<10.2f} {avg_or:<10.2f} {stdev_or:<10.2f}")
    
def display_metrics(data, title):
    """Display formatted results in a table."""
    print(f"\n{title}")
    print("-" * 130)
    print(f"{'Format':<10} {'Algorithm':<10} {'Avg BR':<10} {'Stdev BR':<10} {'Avg OR':<10} {'Stdev OR':<10} {'Avg Time':<12} {'Stdev Time':<12} {'Successes':<10} {'Total':<10}")
    print("-" * 130)
    
    def calculate_stats(values):
        n = len(values)
        mean = sum(values) / n if n > 0 else 0
        stdev = math.sqrt(sum((x - mean) ** 2 for x in values) / n) if n > 1 else 0
        return mean, stdev

    for (format_, algorithm), metrics in data.items():
        avg_br, stdev_br = calculate_stats(metrics["broken_repaired"])
        avg_or, stdev_or = calculate_stats(metrics["original_repaired"])
        avg_time, stdev_time = calculate_stats(metrics["repair_times"])
        successes = metrics["successes"]
        total_attempts = metrics["total_attempts"]
        
        print(f"{format_:<10} {algorithm:<10} {avg_br:<10.2f} {stdev_br:<10.2f} {avg_or:<10.2f} {stdev_or:<10.2f} {avg_time:<12.2f} {stdev_time:<12.2f} {successes:<10} {total_attempts:<10}")

def edit_distance_with_ops(strA: str, strB: str) -> Tuple[int, int, int, int]:
    """
    Calculate the shortest edit distance from strA to strB and count operations:
    - Delete, Insert, Replace.

    Returns:
      (dist, del_count, ins_count, rep_count)
    """
    m, n = len(strA), len(strB)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    op = [[""] * (n + 1) for _ in range(m + 1)]

    # 初始化dp和op
    for i in range(1, m + 1):
        dp[i][0] = i
        op[i][0] = 'D'

    for j in range(1, n + 1):
        dp[0][j] = j
        op[0][j] = 'I'

    # 填充dp和op
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if strA[i - 1] == strB[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
                op[i][j] = 'M'
            else:
                del_cost = dp[i - 1][j] + 1
                ins_cost = dp[i][j - 1] + 1
                rep_cost = dp[i - 1][j - 1] + 1
                min_cost = min(del_cost, ins_cost, rep_cost)
                dp[i][j] = min_cost
                if min_cost == del_cost:
                    op[i][j] = 'D'
                elif min_cost == ins_cost:
                    op[i][j] = 'I'
                else:
                    op[i][j] = 'R'

    dist = dp[m][n]
    del_count = 0
    ins_count = 0
    rep_count = 0

    # 回溯操作
    i, j = m, n
    while i > 0 or j > 0:
        current_op = op[i][j]
        if current_op == 'M':
            i -= 1
            j -= 1
        elif current_op == 'D':
            del_count += 1
            i -= 1
        elif current_op == 'I':
            ins_count += 1
            j -= 1
        elif current_op == 'R':
            rep_count += 1
            i -= 1
            j -= 1

    return dist, del_count, ins_count, rep_count

def calculate_average_delete_operations():
    combined_results = {}
    database_results = {db: {} for db in DATABASES}
    database_format_results = {db: {} for db in DATABASES}

    def update_results(results_dict, key, distance, del_count):
        """
        通用的更新函数，储存并累计编辑距离和删除操作数
        """
        if key not in results_dict:
            results_dict[key] = {
                "total_distance": 0,
                "total_deletes": 0,
                "count": 0
            }
        results_dict[key]["total_distance"] += distance
        results_dict[key]["total_deletes"] += del_count
        results_dict[key]["count"] += 1

    for db_path in DATABASES:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # 获取 fixed=1 且 repaired_text 不为空的记录
        cursor.execute("""
            SELECT format, algorithm, broken_text, repaired_text
            FROM results
            WHERE fixed = 1 AND repaired_text IS NOT NULL
        """)

        rows = cursor.fetchall()
        conn.close()

        for format_, algorithm, original_text, repaired_text in rows:
            dist, del_count, _, _ = edit_distance_with_ops(original_text, repaired_text)
            
            # 更新当前数据库中的算法统计
            update_results(database_results[db_path], algorithm, dist, del_count)
            
            # 更新总的合并统计
            update_results(combined_results, algorithm, dist, del_count)
            
            # 更新format维度的统计
            if algorithm not in database_format_results[db_path]:
                database_format_results[db_path][algorithm] = {}
            update_results(database_format_results[db_path][algorithm], format_, dist, del_count)

    # --- 输出 1： 组合所有数据库的结果 ---
    print("Combined Results Across All Databases:")
    print("-" * 70)
    print(f"{'Algorithm':<15} {'Avg Distance':<15} {'Avg Deletes':<15} {'Count':<10}")
    print("-" * 70)
    for algorithm, data in combined_results.items():
        count = data["count"]
        avg_dist = data["total_distance"] / count if count > 0 else 0
        avg_del = data["total_deletes"] / count if count > 0 else 0
        print(f"{algorithm:<15} {avg_dist:<15.2f} {avg_del:<15.2f} {count:<10}")

    # --- 输出 2： 各数据库分别的结果 ---
    for db_path, results in database_results.items():
        print(f"\nResults for {db_path}:")
        print("-" * 70)
        print(f"{'Algorithm':<15} {'Avg Distance':<15} {'Avg Deletes':<15} {'Count':<10}")
        print("-" * 70)
        for algorithm, data in results.items():
            count = data["count"]
            avg_dist = data["total_distance"] / count if count > 0 else 0
            avg_del = data["total_deletes"] / count if count > 0 else 0
            print(f"{algorithm:<15} {avg_dist:<15.2f} {avg_del:<15.2f} {count:<10}")

        # --- 输出 3： 按格式分类的结果 ---
        print(f"\nFormat-Specific Results for {db_path}:")
        print("-" * 80)
        print(f"{'Algorithm':<15} {'Format':<15} {'Avg Distance':<15} {'Avg Deletes':<15} {'Count':<10}")
        print("-" * 80)
        for algorithm, formats in database_format_results[db_path].items():
            for format_, data in formats.items():
                count = data["count"]
                avg_dist = data["total_distance"] / count if count > 0 else 0
                avg_del = data["total_deletes"] / count if count > 0 else 0
                print(f"{algorithm:<15} {format_:<15} {avg_dist:<15.2f} {avg_del:<15.2f} {count:<10}")

def get_iterations():
    def calculate_average_iterations(database):
        conn = sqlite3.connect(database)
        cursor = conn.cursor()

        # Ensure the iterations column exists
        cursor.execute("PRAGMA table_info(results)")
        columns = [col[1] for col in cursor.fetchall()]
        if "iterations" not in columns:
            print(f"[WARNING] 'iterations' column not found in {database}. Skipping.")
            conn.close()
            return {}

        # Query to calculate average iterations by algorithm
        cursor.execute("""
            SELECT algorithm, COUNT(*), AVG(iterations) 
            FROM results
            WHERE iterations > 0
            GROUP BY algorithm
        """)

        results = cursor.fetchall()
        conn.close()

        # Return as a dictionary
        return {row[0]: (row[1], row[2]) for row in results}

    # Aggregate results from all databases
    algorithm_stats = {}

    for db in DATABASES:
        db_stats = calculate_average_iterations(db)
        for algorithm, (count, avg_iterations) in db_stats.items():
            if algorithm not in algorithm_stats:
                algorithm_stats[algorithm] = {"total_count": 0, "total_iterations": 0.0}
            algorithm_stats[algorithm]["total_count"] += count
            algorithm_stats[algorithm]["total_iterations"] += count * avg_iterations

    # Calculate and display overall average iterations for each algorithm
    print(f"{'Algorithm':<15}{'Total Count':<15}{'Average Iterations':<20}")
    print("-" * 50)
    for algorithm, stats in algorithm_stats.items():
        total_count = stats["total_count"]
        avg_iterations = stats["total_iterations"] / total_count if total_count > 0 else 0
        print(f"{algorithm:<15}{total_count:<15}{avg_iterations:<20.2f}")

def calculate_average_delete_operations():
    """
    1. Compute both Broken→Repaired (BR) and Original→Repaired (OR) distances and deletions.
    2. Aggregate results across:
       - All three databases combined
       - Individual databases
       - Format-specific within each database
    """
    combined_results_BR = {}
    combined_results_OR = {}
    database_results_BR = {db: {} for db in DATABASES}
    database_results_OR = {db: {} for db in DATABASES}
    database_format_results_BR = {db: {} for db in DATABASES}
    database_format_results_OR = {db: {} for db in DATABASES}

    def update_results(results_dict, key, distance, del_count):
        if key not in results_dict:
            results_dict[key] = {
                "total_distance": 0,
                "total_deletes": 0,
                "count": 0
            }
        results_dict[key]["total_distance"] += distance
        results_dict[key]["total_deletes"] += del_count
        results_dict[key]["count"] += 1

    for db_path in DATABASES:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT format, algorithm, broken_text, repaired_text, original_text
            FROM results
            WHERE fixed = 1 AND repaired_text IS NOT NULL
        """)

        rows = cursor.fetchall()
        conn.close()

        for format_, algorithm, broken_text, repaired_text, original_text in rows:
            # Compute distances for BR (Broken → Repaired) and OR (Original → Repaired)
            dist_br, del_count_br, _, _ = edit_distance_with_ops(broken_text, repaired_text)
            dist_or, del_count_or, _, _ = edit_distance_with_ops(original_text, repaired_text)

            # Update per-database and overall statistics
            update_results(database_results_BR[db_path], algorithm, dist_br, del_count_br)
            update_results(database_results_OR[db_path], algorithm, dist_or, del_count_or)
            update_results(combined_results_BR, algorithm, dist_br, del_count_br)
            update_results(combined_results_OR, algorithm, dist_or, del_count_or)

            # Format-specific
            if algorithm not in database_format_results_BR[db_path]:
                database_format_results_BR[db_path][algorithm] = {}
            update_results(database_format_results_BR[db_path][algorithm], format_, dist_br, del_count_br)

            if algorithm not in database_format_results_OR[db_path]:
                database_format_results_OR[db_path][algorithm] = {}
            update_results(database_format_results_OR[db_path][algorithm], format_, dist_or, del_count_or)

    # Print Combined Results
    def print_table(title, results):
        print(f"\n{title}:")
        print("-" * 70)
        print(f"{'Algorithm':<15} {'Avg Distance':<15} {'Avg Deletes':<15} {'Count':<10}")
        print("-" * 70)
        for algorithm, data in results.items():
            count = data["count"]
            avg_dist = data["total_distance"] / count if count > 0 else 0
            avg_del = data["total_deletes"] / count if count > 0 else 0
            print(f"{algorithm:<15} {avg_dist:<15.2f} {avg_del:<15.2f} {count:<10}")

    print_table("Combined Broken → Repaired (BR) Results", combined_results_BR)
    print_table("Combined Original → Repaired (OR) Results", combined_results_OR)

    # Print per-database results
    for db_path in DATABASES:
        print_table(f"Results for {db_path} (BR)", database_results_BR[db_path])
        print_table(f"Results for {db_path} (OR)", database_results_OR[db_path])

        # Print format-specific results
        print(f"\nFormat-Specific Results for {db_path}:")
        print("-" * 80)
        print(f"{'Algorithm':<15} {'Format':<15} {'Avg Distance':<15} {'Avg Deletes':<15} {'Count':<10}")
        print("-" * 80)
        for algorithm, formats in database_format_results_BR[db_path].items():
            for format_, data in formats.items():
                count = data["count"]
                avg_dist = data["total_distance"] / count if count > 0 else 0
                avg_del = data["total_deletes"] / count if count > 0 else 0
                print(f"{algorithm:<15} {format_:<15} {avg_dist:<15.2f} {avg_del:<15.2f} {count:<10}")

def delete_ratio():
    """
    1. Compute both Broken→Repaired (BR) and Original→Repaired (OR) distances and deletions.
    2. Aggregate results across:
       - All three databases combined
       - Individual databases
       - Format-specific within each database
    """
    combined_results_BR = {}
    combined_results_OR = {}
    database_results_BR = {db: {} for db in DATABASES}
    database_results_OR = {db: {} for db in DATABASES}
    database_format_results_BR = {db: {} for db in DATABASES}
    database_format_results_OR = {db: {} for db in DATABASES}

    def update_results(results_dict, key, distance, del_count):
        if key not in results_dict:
            results_dict[key] = {
                "total_distance": 0,
                "total_deletes": 0,
                "count": 0
            }
        results_dict[key]["total_distance"] += distance
        results_dict[key]["total_deletes"] += del_count
        results_dict[key]["count"] += 1

    for db_path in DATABASES:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT format, algorithm, broken_text, repaired_text, original_text
            FROM results
            WHERE fixed = 1 AND repaired_text IS NOT NULL
        """)

        rows = cursor.fetchall()
        conn.close()

        for format_, algorithm, broken_text, repaired_text, original_text in rows:
            # Compute distances for BR (Broken → Repaired) and OR (Original → Repaired)
            dist_br, del_count_br, _, _ = edit_distance_with_ops(broken_text, repaired_text)
            dist_or, del_count_or, _, _ = edit_distance_with_ops(original_text, repaired_text)

            # Update per-database and overall statistics
            update_results(database_results_BR[db_path], algorithm, dist_br, del_count_br)
            update_results(database_results_OR[db_path], algorithm, dist_or, del_count_or)
            update_results(combined_results_BR, algorithm, dist_br, del_count_br)
            update_results(combined_results_OR, algorithm, dist_or, del_count_or)

            # Format-specific
            if algorithm not in database_format_results_BR[db_path]:
                database_format_results_BR[db_path][algorithm] = {}
            update_results(database_format_results_BR[db_path][algorithm], format_, dist_br, del_count_br)

            if algorithm not in database_format_results_OR[db_path]:
                database_format_results_OR[db_path][algorithm] = {}
            update_results(database_format_results_OR[db_path][algorithm], format_, dist_or, del_count_or)

    # Print Combined Results
    def print_table(title, results):
        print(f"\n{title}:")
        print("-" * 70)
        print(f"{'Algorithm':<15} {'Avg Distance':<15} {'Avg Deletes':<15} {'Count':<10}")
        print("-" * 70)
        for algorithm, data in results.items():
            count = data["count"]
            avg_dist = data["total_distance"] / count if count > 0 else 0
            avg_del = data["total_deletes"] / count if count > 0 else 0
            print(f"{algorithm:<15} {avg_dist:<15.2f} {avg_del:<15.2f} {count:<10}")

    print_table("Combined Broken → Repaired (BR) Results", combined_results_BR)
    print_table("Combined Original → Repaired (OR) Results", combined_results_OR)

    # Print per-database results
    for db_path in DATABASES:
        print_table(f"Results for {db_path} (BR)", database_results_BR[db_path])
        print_table(f"Results for {db_path} (OR)", database_results_OR[db_path])

        # Print format-specific results
        print(f"\nFormat-Specific Results for {db_path}:")
        print("-" * 80)
        print(f"{'Algorithm':<15} {'Format':<15} {'Avg Distance':<15} {'Avg Deletes':<15} {'Count':<10}")
        print("-" * 80)
        for algorithm, formats in database_format_results_BR[db_path].items():
            for format_, data in formats.items():
                count = data["count"]
                avg_dist = data["total_distance"] / count if count > 0 else 0
                avg_del = data["total_deletes"] / count if count > 0 else 0
                print(f"{algorithm:<15} {format_:<15} {avg_dist:<15.2f} {avg_del:<15.2f} {count:<10}")

def count_fixed_files():
    """
    Counts the number of successfully repaired files per algorithm across multiple databases.
    """
    # Dictionary to store results
    total_counts = {}
    database_counts = {db: {} for db in DATABASES}

    for db_path in DATABASES:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Query to count fixed records per algorithm
        cursor.execute("""
            SELECT algorithm, COUNT(*) 
            FROM results 
            WHERE fixed = 1 
            GROUP BY algorithm
        """)

        for algorithm, count in cursor.fetchall():
            # Update per-database count
            database_counts[db_path][algorithm] = count

            # Update total count
            if algorithm not in total_counts:
                total_counts[algorithm] = 0
            total_counts[algorithm] += count

        conn.close()

    # Print per-database results
    for db_path, counts in database_counts.items():
        print(f"\nResults for {db_path}:")
        print("-" * 40)
        print(f"{'Algorithm':<15} {'Fixed Count':<15}")
        print("-" * 40)
        for algorithm, count in counts.items():
            print(f"{algorithm:<15} {count:<15}")

    # Print combined results
    print("\nTotal Fixed Files Across All Databases:")
    print("-" * 40)
    print(f"{'Algorithm':<15} {'Fixed Count':<15}")
    print("-" * 40)
    for algorithm, count in total_counts.items():
        print(f"{algorithm:<15} {count:<15}")

def count_perfect_repairs_by_algorithm():
    """
    Count the number of perfectly repaired entries in each database by algorithm and format.
    A perfect repair means the original and repaired texts have a distance of 0.
    """
    for db_path in DATABASES:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Query to count perfect repairs by format and algorithm
        cursor.execute("""
            SELECT format, algorithm, COUNT(*)
            FROM results
            WHERE distance_original_repaired = 0
            GROUP BY format, algorithm
        """)

        results = cursor.fetchall()

        print(f"Perfect Repairs by Algorithm in {db_path}:")
        if results:
            for format_, algorithm, count in results:
                print(f"  Format: {format_}, Algorithm: {algorithm}, Perfect Repairs: {count}")
        else:
            print("  No perfect repairs found.")

        conn.close()

def calculate_avg_runtime():
    """
    Calculates the average runtime of each algorithm when fixed=1 (successful repair).
    """
    total_runtimes = {}  # Store total runtime per algorithm
    total_counts = {}  # Store count of successful repairs per algorithm
    database_runtimes = {db: {} for db in DATABASES}  # Store per-database results

    for db_path in DATABASES:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Query to calculate average runtime for fixed=1 cases
        cursor.execute("""
            SELECT algorithm, AVG(repair_time), COUNT(*)
            FROM results 
            GROUP BY algorithm
        """)

        for algorithm, avg_runtime, count in cursor.fetchall():
            # Store per-database statistics
            database_runtimes[db_path][algorithm] = (avg_runtime, count)

            # Update total statistics
            if algorithm not in total_runtimes:
                total_runtimes[algorithm] = 0
                total_counts[algorithm] = 0
            total_runtimes[algorithm] += avg_runtime * count  # Accumulate total time
            total_counts[algorithm] += count  # Accumulate total successful repairs

        conn.close()

    # Print per-database results
    for db_path, runtimes in database_runtimes.items():
        print(f"\nAverage Runtime for {db_path} (Successful Repairs Only):")
        print("-" * 50)
        print(f"{'Algorithm':<15} {'Avg Time (s)':<15} {'Count':<10}")
        print("-" * 50)
        for algorithm, (avg_runtime, count) in runtimes.items():
            print(f"{algorithm:<15} {avg_runtime:<15.2f} {count:<10}")

    # Print combined results
    print("\nOverall Average Runtime Across All Databases:")
    print("-" * 50)
    print(f"{'Algorithm':<15} {'Avg Time (s)':<15} {'Count':<10}")
    print("-" * 50)
    for algorithm in total_runtimes:
        avg_runtime = total_runtimes[algorithm] / total_counts[algorithm] if total_counts[algorithm] > 0 else 0
        print(f"{algorithm:<15} {avg_runtime:<15.2f} {total_counts[algorithm]:<10}")

def edit_distance_with_ops(strA: str, strB: str) -> Tuple[int, int, int, int]:
    """
    Compute the Levenshtein distance and count delete, insert, and replace operations.
    
    Returns:
      (distance, del_count, ins_count, rep_count)
    """
    m, n = len(strA), len(strB)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    op = [[""] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        dp[i][0] = i
        op[i][0] = 'D'  # Deletion

    for j in range(1, n + 1):
        dp[0][j] = j
        op[0][j] = 'I'  # Insertion

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if strA[i - 1] == strB[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
                op[i][j] = 'M'
            else:
                del_cost = dp[i - 1][j] + 1
                ins_cost = dp[i][j - 1] + 1
                rep_cost = dp[i - 1][j - 1] + 1
                dp[i][j] = min(del_cost, ins_cost, rep_cost)

                if dp[i][j] == del_cost:
                    op[i][j] = 'D'
                elif dp[i][j] == ins_cost:
                    op[i][j] = 'I'
                else:
                    op[i][j] = 'R'

    dist = dp[m][n]
    del_count = 0
    ins_count = 0
    rep_count = 0

    i, j = m, n
    while i > 0 or j > 0:
        if i > 0 and j > 0 and op[i][j] == 'M':
            i -= 1
            j -= 1
        elif i > 0 and op[i][j] == 'D':
            del_count += 1
            i -= 1
        elif j > 0 and op[i][j] == 'I':
            ins_count += 1
            j -= 1
        elif i > 0 and j > 0 and op[i][j] == 'R':
            rep_count += 1
            i -= 1
            j -= 1
        else:
            break  # Avoid infinite loops

    return dist, del_count, ins_count, rep_count

def calculate_avg_surviving_data():
    def update_results(results_dict, key, surviving_ratio):
        if key not in results_dict:
            results_dict[key] = {"ratios": [], "total_ratio": 0, "count": 0}
        results_dict[key]["ratios"].append(surviving_ratio)
        results_dict[key]["total_ratio"] += surviving_ratio
        results_dict[key]["count"] += 1

    def calculate_stats(data):
        count = len(data)
        mean = sum(data) / count if count > 0 else 0
        stdev = math.sqrt(sum((x - mean) ** 2 for x in data) / count) if count > 1 else 0
        return mean, stdev

    for mode, column in [("OR", "original_text"), ("CR", "broken_text")]:
        results = {}
        db_results = {db: {} for db in DATABASES}

        for db_path in DATABASES:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            cursor.execute(f"""
                SELECT algorithm, {column}, repaired_text 
                FROM results
                WHERE fixed = 1 AND repaired_text IS NOT NULL
            """)

            rows = cursor.fetchall()
            conn.close()

            for algorithm, original_text, repaired_text in rows:
                L = len(original_text)
                _, d, _, _ = edit_distance_with_ops(original_text, repaired_text)
                surviving_ratio = (L - d) / L if L > 0 else 0

                update_results(db_results[db_path], algorithm, surviving_ratio)
                update_results(results, algorithm, surviving_ratio)

        print(f"\n Surviving Data Ratio ({mode})")
        for db_path, algorithms in db_results.items():
            print(f"\nResults for {db_path}:")
            print("-" * 70)
            print(f"{'Algorithm':<15} {'Avg Surviving Ratio':<20} {'Stdev':<15} {'Count':<10}")
            print("-" * 70)
            for algorithm, data in algorithms.items():
                avg_ratio, stdev = calculate_stats(data["ratios"])
                print(f"{algorithm:<15} {avg_ratio:<20.4f} {stdev:<15.4f} {data['count']:<10}")

        print(f"\nOverall Results Across All Databases ({mode}):")
        print("-" * 70)
        print(f"{'Algorithm':<15} {'Avg Surviving Ratio':<20} {'Stdev':<15} {'Count':<10}")
        print("-" * 70)
        for algorithm, data in results.items():
            avg_ratio, stdev = calculate_stats(data["ratios"])
            print(f"{algorithm:<15} {avg_ratio:<20.4f} {stdev:<15.4f} {data['count']:<10}")

if __name__ == "__main__":
    print("----------------Table 4-5(General)------------------------------------")
    calculate_and_display_detailed_metrics()
    print("----------------Table 4-5(Data Survive)-------------------------------")
    calculate_avg_surviving_data()
    print("----------------Table 4-5(levenshtein distances)----------------------")
    all_distances()
    print("----------------Table 6(Count repaired)-------------------------------")
    count_fixed_files()
    print("----------------Table 7(Perfectly repaire)----------------------------")
    count_perfect_repairs_by_algorithm()
    print("----------------Table 8(Efficiency)-----------------------------------")
    calculate_avg_runtime()
    get_iterations()
    