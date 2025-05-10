# Erepair

## Artifact repository

This repository is the artifact repository of epsilonRepair.

***EpsilonRepair is an algorithm we proposed to help users repair corrupted text files, such as JSON, INI, TinyC, etc., even when the exact format is unknown. It ensures high efficiency while minimizing information loss as much as possible.***

## How to build and run the project
We provide both C and Java versions of epsilonRepair. The C version includes more experimental features, runs faster, and is suitable for personal use, whereas the Java version provides more debugging information and is better suited for commercial use.

### Install Java version
Before installing epsilonRepair, please make sure the latest versions of JDK and Gradle are installed properly.

> `cd project`
> `gradle deployJar --stacktrace --info`

### Install C version
You should have any C++ compiler(g++, clang++, msvc...) with at least C++17 support installed in your computer. Then, run:

> `g++<or clang++ if use clang> -std=c++17 ./erepair.cpp -o erepair`

Please note that there is another cpp file in the repo called erepair2.cpp, it applies same epsilonRepair algorithm with more aggressive pruning strategy make it excellent at truncation completing task. You can also choose it to compile if needed.
## Command-Line Arguments

### Usage

#### Start with Java version
###### Repair a file using the given algorithm 
> `java -jar erepair -r -i <inputfile> [-o <outputdir>] -a <algorithm,use erepair for lauch epsilonRepair process>`

###### Mutate all files in directory

For a list of algorithms, see the CLI help text.

> `java -jar erepair -M -i <inputdir> -o <outputdir> [-t <times>] [-a <algorithm>]`

###### Run a subject program on a given file

> `java -jar erepair -O <subject> -i <inputfile> [-o <outputfile>]`

#### Start with C version
First, you need to determine the target interpreter. You can use any interpreter that meets the requirements outlined in the paper and provides the corresponding state return values. Alternatively, you can use the interpreters provided in our repository, including TinyC, cJSON, INI, and SExp. You can find them in the project/erepair-subjects folder. If these interpreters do not run properly on your computer, please recompile them using the `make` command first.

Then run command:
> `./erepair <PathtoIntepreter> <inputfile> <outputfile>`

### Build your own "interpreter" as target

You can also repair files whose grammar is defined by regular expressions. with [regex](https://pypi.org/project/regex/), for example:

```python 
import regex as re
import sys
import argparse

# Define regular expressions for the formats
patterns = {
    "Date": r"^\d{4}-\d{2}-\d{2}$",  # Format: YYYY-MM-DD
    "Time": r"^\d{2}:\d{2}:\d{2}$",  # Format: HH:MM:SS
    "URL":  r"https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)",
    "ISBN": r"^(?:\d[- ]?){9}[\dX]$",  # ISBN-10 
    "IPv4": r"^(\d{1,3}\.){3}\d{1,3}$",
    "IPv6": r"^([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}$",
    "FilePath": r"^[a-zA-Z]:\\(?:[^\\/:*?\"<>|\r\n]+\\)*[^\\/:*?\"<>|\r\n]*$"
}

def validate_data_with_partial(pattern, data):
    """Validate the data using partial matches."""
    match = re.match(pattern, data, partial=True)
    if match:
        if match.partial:
            return -1  # Partial match
        else:
            return 0  # Full match
    return 1  # Parsing error

def main(): 
    parser = argparse.ArgumentParser(description="Validate file content with partial match support.")
    parser.add_argument("category", choices=patterns.keys(), help="Category to validate against.")
    parser.add_argument("file_path", help="Path to the input file.")
    args = parser.parse_args()

    # Read the file
    try:
        with open(args.file_path, 'r') as file:
            data = file.read().strip()
    except FileNotFoundError:
        print(f"Error: File '{args.file_path}' not found.", file=sys.stderr)
        sys.exit(1)

    # Validate data
    pattern = patterns[args.category]
    result = validate_data_with_partial(pattern, data)
    sys.exit(result)

if __name__ == "__main__":
    main()
```

Save it as match.py, then, you can use the full command to run this file as the interpreter path for erepair.

> `./erepair 'python3 match.py <category>' <inputfile> <outputfile>`

### Evaluation

Once you have been satisfied all steps above, you can also have your own benchmark, for sure!

#### Fetech the dataset from github
You can use the following command to fetch typef of files you desire from the Github:
> `python3 fetch_dataset.py -e <extension> -q <query> -size <size> -out <outputdir>`
##### Start mutation
> `python3 mutation_[single|double|truncated].py --folder <Path to Original file> --validator <target intepreter>> --database <database to save>`

##### Single mutation

> `python3 benchmark_single.py -f <format> -d <database to store the result>`

##### double mutation

> `python3 benchmark_multiple.py -f <format> -d <database to store the result>`

##### Truncation mutation

> `python3 benchmark_prefix.py -f <format> -d <database to store the result>`

#### Obtain statistical report

You can obtain all tables in the paper with one command:

```
python3 report.py --single <database> --double <database> --truncated <database> --output <outputdir>
```

Example:
```
fsynth-artifact % python '/Users/jack/fsynth-artifact/report.py' --single '/Users/jack/fsynth-artifact/single.db' --double '/Users/jack/fsynth-artifact/double.db' --truncated '/Users/jack/fsynth-artifact/truncated.db'

**TABLE III: Number of corrupt inputs**

| Format | Record Len.     | Single Corr. | Double Corr. | Truncated   |
|--------|-----------------|--------------|--------------|-------------|
| DOT    | 2716.7 σ 2047.1 | 3096         | 400          | 400 (12.9%) |
| INI    | 2950.3 σ 2255.7 | 2320         | 400          | 400 (17.2%) |
| JSON   | 3635.1 σ 2389.3 | 3932         | 400          | 400 (10.2%) |
| LISP   | 131.6 σ 65.0    | 4000         | 400          | 400 (10.0%) |
| OBJ    | 3468.2 σ 2691.8 | 1932         | 400          | 400 (20.7%) |

**TABLE IV: Distance between corrupt data and repaired data**

| Format |         Format-free         |          Format-dependent         |
|        | εREPAIR       | DDMax       | DDMaxG          | ANTLR           |
|--------|---------------|-------------|-----------------|-----------------|
| DOT    | 7.3 σ 90.3    | 5.1 σ 14.3  | 653.1 σ 612.2   | 1256.2 σ 975.7  |
| INI    | 24.4 σ 62.2   | 24.1 σ 62.0 | 1304.3 σ 1654.5 | 1363.1 σ 1721.2 |
| JSON   | 48.0 σ 424.3  | 8.4 σ 20.8  | 1060.0 σ 1176.8 | 1056.4 σ 1157.1 |
| LISP   | 68.7 σ 65.5   | 21.1 σ 24.2 | 70.8 σ 47.1     | n.a             |
| OBJ    | 137.5 σ 502.6 | 43.0 σ 83.9 | n.a             | n.a             |
| Format |          Format-free          |          Format-dependent         |
|        | εREPAIR       | DDMax         | DDMaxG          | ANTLR           |
|--------|---------------|---------------|-----------------|-----------------|
| DOT    | 5.9 σ 17.0    | 5.6 σ 2.6     | 718.0 σ 593.8   | n.a             |
| INI    | 17.1 σ 41.4   | 15.9 σ 41.2   | 1244.3 σ 1541.8 | 1316.3 σ 1649.2 |
| JSON   | 70.8 σ 304.2  | 221.9 σ 641.7 | 1106.2 σ 1136.5 | 1111.3 σ 1102.4 |
| LISP   | 49.2 σ 58.9   | 37.2 σ 40.8   | 85.9 σ 57.3     | n.a             |
| OBJ    | 155.8 σ 581.0 | 47.1 σ 93.0   | n.a             | n.a             |
| Format |           Format-free           |          Format-dependent         |
|        | εREPAIR       | DDMax           | DDMaxG          | ANTLR           |
|--------|---------------|-----------------|-----------------|-----------------|
| DOT    | 6.6 σ 16.5    | n.a             | n.a             | n.a             |
| INI    | 17.1 σ 41.4   | 15.9 σ 41.2     | 1244.3 σ 1541.8 | 1316.3 σ 1649.2 |
| JSON   | 70.8 σ 304.2  | 1303.4 σ 2258.8 | 1153.5 σ 1170.0 | 1111.3 σ 1102.4 |
| LISP   | 49.2 σ 58.9   | 37.2 σ 40.8     | 85.9 σ 57.3     | n.a             |
| OBJ    | 159.0 σ 578.9 | 47.1 σ 93.0     | n.a             | n.a             |
|--------|---------------|-----------------|-----------------|-----------------|
| Average | 55.1 σ 295.4  | 37.5 σ 250.2    | 745.8 σ 1141.0  | 1194.9 σ 1432.5 |
| Recovery | 90% σ 29.47   | 63% σ 48.15     | 73% σ 44.54     | 31% σ 46.23     |

**TABLE V: Distance from original data to repaired data**

| Format |         Format-free         |          Format-dependent         |
|        | εREPAIR       | DDMax       | DDMaxG          | ANTLR           |
|--------|---------------|-------------|-----------------|-----------------|
| DOT    | 7.3 σ 90.3    | 5.8 σ 14.3  | 653.0 σ 612.3   | 1256.5 σ 975.6  |
| INI    | 26.4 σ 62.2   | 25.8 σ 62.1 | 1305.4 σ 1654.1 | 1364.3 σ 1720.7 |
| JSON   | 47.9 σ 424.4  | 9.6 σ 20.6  | 1060.0 σ 1176.9 | 1056.3 σ 1157.2 |
| LISP   | 69.8 σ 65.3   | 22.5 σ 23.9 | 70.8 σ 47.1     | n.a             |
| OBJ    | 138.1 σ 502.6 | 44.3 σ 83.9 | n.a             | n.a             |
| Format |          Format-free          |          Format-dependent         |
|        | εREPAIR       | DDMax         | DDMaxG          | ANTLR           |
|--------|---------------|---------------|-----------------|-----------------|
| DOT    | 6.0 σ 17.0    | 6.2 σ 1.9     | 717.8 σ 593.8   | n.a             |
| INI    | 19.0 σ 41.4   | 17.8 σ 41.2   | 1245.5 σ 1541.4 | 1317.5 σ 1648.8 |
| JSON   | 70.9 σ 304.2  | 223.3 σ 641.3 | 1106.0 σ 1136.5 | 1111.2 σ 1102.5 |
| LISP   | 50.3 σ 58.8   | 38.4 σ 40.3   | 85.8 σ 57.4     | n.a             |
| OBJ    | 156.2 σ 580.9 | 48.4 σ 93.1   | n.a             | n.a             |
| Format |           Format-free           |          Format-dependent         |
|        | εREPAIR       | DDMax           | DDMaxG          | ANTLR           |
|--------|---------------|-----------------|-----------------|-----------------|
| DOT    | 375.3 σ 521.9 | n.a             | n.a             | n.a             |
| INI    | 19.0 σ 41.4   | 17.8 σ 41.2     | 1245.5 σ 1541.4 | 1317.5 σ 1648.8 |
| JSON   | 70.9 σ 304.2  | 1304.3 σ 2258.3 | 1153.3 σ 1170.0 | 1111.2 σ 1102.5 |
| LISP   | 50.3 σ 58.8   | 38.4 σ 40.3     | 85.8 σ 57.4     | n.a             |
| OBJ    | 159.3 σ 578.8 | 48.4 σ 93.1     | n.a             | n.a             |
|--------|---------------|-----------------|-----------------|-----------------|
| Average | 61.0 σ 304.2  | 38.9 σ 250.1    | 746.0 σ 1141.0  | 1195.4 σ 1432.4 |
| Recovery | 90% σ 29.47   | 63% σ 48.15     | 73% σ 44.54     | 31% σ 46.23     |

**TABLE VI: Number of corrupt records repaired**

| Scenario  | Format | erepair | DDMax | DDMaxG | Antlr |
|-----------|--------|---------|-------|--------|-------|
| Single    | DOT    | 705     | 198   | 524    | 4     |
| Single    | INI    | 580     | 580   | 580    | 503   |
| Single    | JSON   | 852     | 245   | 868    | 681   |
| Single    | LISP   | 796     | 901   | 863    | 0     |
| Single    | OBJ    | 481     | 483   | 0      | 0     |
| Double    | DOT    | 94      | 9     | 90     | 0     |
| Double    | INI    | 100     | 100   | 100    | 85    |
| Double    | JSON   | 94      | 17    | 89     | 67    |
| Double    | LISP   | 100     | 100   | 100    | 0     |
| Double    | OBJ    | 99      | 100   | 0      | 0     |
| Truncated | DOT    | 62      | 0     | 0      | 0     |
| Truncated | INI    | 100     | 100   | 100    | 85    |
| Truncated | JSON   | 94      | 26    | 91     | 67    |
| Truncated | LISP   | 100     | 100   | 100    | 0     |
| Truncated | OBJ    | 100     | 100   | 0      | 0     |
| Total     |        | 4357    | 3059  | 3505   | 1492  |

**TABLE VII: Number of perfectly repaired files**

| Scenario  | Format | erepair | DDMax | DDMaxG | Antlr |
|-----------|--------|---------|-------|--------|-------|
| Single    | DOT    | 46      | 1     | 0      | 0     |
| Single    | INI    | 0       | 1     | 0      | 0     |
| Single    | JSON   | 83      | 0     | 0      | 0     |
| Single    | OBJ    | 19      | 1     | 0      | 0     |
| Double    | JSON   | 2       | 0     | 0      | 0     |
| Double    | OBJ    | 9       | 0     | 0      | 0     |
| Truncated | JSON   | 2       | 0     | 0      | 0     |
| Truncated | OBJ    | 9       | 0     | 0      | 0     |

**TABLE VIII: Efficiency of data repair (Average)**

| Metric | erepair   | DDMax     | DDMaxG    | Antlr     |
|--------|-----------|-----------|-----------|-----------|
| Runtime | 3.61 secs | 3.83 secs | 4.54 secs | 0.36 secs |
| #Execs | 2591539   | 2542675   | 3218364   | 1492      |
```
