# test-bot
*Automated build+execute testing with a HPC twist.*

Simple tool for setting up and running tests to verify the correctness of one
or more programs in different compiler/run environments. Originally designed
to handle automatic testing of model solutions in
[CSC Summer School in HPC](https://github.com/csc-training/summerschool) and
thus supports parallel programs using MPI and/or OpenMP.


## Installation

No need to install anything. One can simply clone the git repository and run
from there. :smiley:

```shell
git clone https://github.com/mlouhivu/test-bot.git
source test-bot/bin/env.sh
bot --help
```

## Usage

### Setting up

**Step 1. Initialise the tests**. This will create a directory (`.test`) and
populate it with initial files.

```bash
bot init
```

**Step 2. Add test targets**. One or more source code files can be added with
a single command:
```bash
bot add foo.c
bot add example/one.c example/two.f90
```

You can also simply add a base directory, which will then add all source code
files (and directories with Makefiles) recursively:
```bash
bot add example/
```

**Step 3.** (optional) **Edit the manifest** (`.test/manifest`) that lists
all test targets, to specify any special requirements for the tests. See
[manifest](doc/manifest.md) for more detailed information on what can be
done.

**Step 4.** (optional) **Edit the configuration** (`.test/config`) to match
the compile environment of your system. See [config](doc/config.md) for more
details.

### Running

**Step 5. Run tests.**

```bash
bot run
```

**Step 6.** Modify your software and go back to step 5. Rinse and repeat.


## Tests with MPI

No MPI launcher is needed even if you have some tests for MPI programs.
Instead you should edit the [manifest](doc/manifest.md) to enable MPI for
those tests (flavour `+mpi`) and add the command for the correct MPI launcher
into the [config](doc/config.md) file. When running the tests, `bot` will then
use the MPI launcher if and when needed automatically.

```
[example/message.c] +mpi
  test=pass
```

If needed, you can also define a special compiler and compile/link options in
the config file, e.g. inside a `(fortran+mpi)` subsection.


## Tests with OpenMP

Similar to MPI, threading is automatically used for tests that have OpenMP
enabled (flavour `+omp`) in the [manifest](doc/manifest.md).

```
[example/thread.c] +omp
  test=pass
```

If needed, you can also define special compiler and compile/link options in
the config file, e.g. inside a `(c+omp)` subsection.


## Batch jobs

An example batch job script for SLURM:
```bash
#!/bin/bash
#SBATCH -J test-bot
#SBATCH -p test
#SBATCH -N 1
#SBATCH --time=00:30:00

source $HOME/test-bot/bin/env.sh

bot run 2>&1
```
