## Configuration file (`.test/config`)

System specific configurations are stored in a separate configuration file.

It should contain commands and options for the compiler and linker needed to
build the test targets. Each supported compiler family should have a separate
[section](#sections) and within a section, one can further define e.g.
language specific options or commands in [subsections](#subsections).

The compiler family that is actually used for building the test targets can be
selected at runtime with the `--compiler` option. Please see
[config.example](config.example) for an example configuration file.


### Keywords

The commands and options can be defined using the following keywords:

`compiler` -- command to use both as compiler and as linker

`compile-options` -- options to pass on to the compiler

`link-options` -- options to pass on to the linker

`libraries` -- libraries to include at the linking stage


### Sections

Each section should at least define a compiler command to be used.

```
[gnu]
  compiler=gcc
```

It may also include default compile/link options or libraries as well as
subsections for more fine-grained control.


### Subsections

A section may contain one or more subsections that define language specific
or flavour specific build options.

```
[gnu]
  compiler=gcc

  (fortran)
    compiler=gfortran

  (+omp)
    compile-options=-fopenmp
```

Currently supported (=auto-detected) languages are: `c` and `fortran`. One can
also combine a language and a flavour, e.g. `(fortran+mpi)`, to specify
language specific options that are valid only for a particular flavour.

