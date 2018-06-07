## Manifest (`.test/manifest`)

Test targets and their properties are stored in the manifest file.

The manifest contains a list of files (or directories) that should be tested. Each test
target may have additional information ([flavours](#flavours) or
[arguments](#arguments)) to define the exact procedure for the test.

### Target

Target is a single test to be carried out. It may refer to a single file or a
directory containing a Makefile. In the manifest the target path is enclosed
in square brackets, e.g. `[path/to/target/foo.c]`.

One can define additional properties to the test by using tags or arguments in
the target definition. *Tag* is a simple turn-on switch for a flavour and is
given in the form of `+flavour`. *Argument* is a key-value pair given in the
form of `key=value`. Both tags and arguments can be freely placed in new lines
(or the same line), but no whitespace can be used between + or = and the
adjoining text.

For example, to test file `foo/bar.c` with MPI enabled (flavour `mpi`) and to
check for a correct output string, the target could be defined as:
```
[foo/bar.c] +mpi
  type=text
  reference='foobar: 5.6'
```

It is also possible to give the test `type` and `reference` value in the
short-form omitting the key assignment completely, i.e.
```
[foo/bar.c] +mpi text 'foobar: 5.6'
```

### Flavours

Currently there are two flavours that can be turned on using tags:

**+mpi** -- use MPI

**+omp** -- use OpenMP threading

Turning on a flavour may affect both compilation and running of the test and
both flavours can be turned on for hybrid MPI/OpenMP programs.

### Arguments

Below is a list of supported argument keys. The values can be given either as
a single quoted (or non-quoted) string or as a comma-separated list of such
strings enclosed in parentheses. Depending on the argument, these may then be
converted e.g. to numbers.
```
type=text
reference='foobar: 5.6'
export=('MPICH_MAX_THREAD_SAFETY=multiple', 'FOOBAR=56')
```

---

#### type
Defines the type of test to be used for checking the output. By default any
output is just ignored (`type=pass`). Valid values are:

- `pass`  -- ignore output (default)

Not yet implemented:

- `text`  -- exact string (full output)
- `grep`  -- exact string (somewhere in the output)
- `int`   -- integer number
- `float` -- floating point number (cf. tolerance)
- `blob`  -- (binary) blob, i.e. compare files

#### reference
The expected (=correct) output that should be reproduced for the test to
pass. If using type `blob`, it should be the name of a reference file.

#### makefile
Use a non-standard name for the Makefile (see option `-f` in `man make`).

#### user_input
Can be used to pipe "user" input to the target program. Value should be a
single string that can be echoed to the program, i.e.
`echo '{string}' | {program}`.

#### arguments
Command line arguments to the target program. Value should be a single string
that can be appended to the end of the command to be executed.

#### export
Environment variables to be defined when running the target program. Can be a
single value or a list of values. E.g.
`export=('MPICH_MAX_THREAD_SAFETY=multiple')`

#### output
Name of a file that will contain the output instead of STDOUT.

#### tolerance (not implemented)
Defines the error tolerance when comparing floating point numbers, i.e.
`difference(x, reference) < tolerance`.

#### skip_run (boolean)
Do not run the program; only build it.

#### do_not_link (boolean)
Do not link the object; only compile the code into an object.

---

#### Boolean values
For arguments that expect an boolean value, one can use `true` or `yes` for
True and `false` or `no` for False. Capitalisation does not matter; case will
be ignored. In addition, one can also use the tag syntax as a short-hand to set arbitrary
arguments to True, e.g. `+skip_run` is equivalent to `skip_run=true`.

