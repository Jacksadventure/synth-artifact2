# FSynth

Artifact repository

## How to build and run the project

To build the docker image, clone this repository and run

```bash
docker build -t fsynth:$(git rev-parse --short HEAD) -f Dockerfile .
```

from the repository's root directory. Then, the Docker image can be run with

```bash
docker run -v /home/xxx/results:/home/repairer -h fsynth -it fsynth:$(git rev-parse --short HEAD)
```

In this command, `/home/xxx/results` needs to be replaced by the full absolute path of a directory where results should be stored.

The test files are stored in the `/testfiles` directory inside the Docker image. The experiments can be run inside the docker image with the command `fsynth -R 500 -i /testfiles -s statistics.db`. If an error occurs during the run, the run can be resumed using the same command, skipping all files that have already been tested.

## Command-Line Arguments

### Usage

##### Repair a file using the given algorithm

> `fsynth -r -i <inputfile> [-o <outputdir>] -a <algorithm>`

##### Mutate all files in directory

For a list of algorithms, see the CLI help text.

> `fsynth -M -i <inputdir> -o <outputdir> [-t <times>] [-a <algorithm>]`

##### Run a subject program on a given file

> `fsynth -O <subject> -i <inputfile> [-o <outputfile>]`

##### Build the CSV tables

> `fsynth -S`

This will automatically create the CSV output files in the output directory `reports`.