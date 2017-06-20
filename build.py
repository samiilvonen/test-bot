import execute

class BaseCompiler(object):
    def __init__(self, command, options=None, output=None,
            out=None, err=None):
        self.command = str(command)
        self.options = self.parse_options(options)
        self.output = str(output) and output
        self.stdout = out
        self.stderr = err

    def parse_options(self, options):
        if type(options) is str:
            return [options]
        elif type(options) is list:
            return [str(x) for x in options]
        else:
            return []

    def __str__(self):
        return self.invocation()

    def invocation(self):
        cmd = self.command + ' '
        cmd += ' '.join(self.options)
        if self.output:
            cmd += ' -o ' + self.output
        return cmd + ' %s'

    def __call__(self, filename):
        str(self) + filename
        cmd = self.invocation() % filename
        execute.serial(cmd, out=self.stdout, err=self.stderr)


class Compiler(BaseCompiler):
    def compile(self, filename):
        self(filename)


class Linker(BaseCompiler):
    def __init__(self, command, options=None, libraries=None, output=None):
        self.command = str(command)
        self.options = self.parse_options(options)
        self.output = str(output) and output
        self.libraries = []
        for library in libraries:
            self.add_library(library)

    def invocation(self):
        cmd = self.command + ' '
        cmd += ' '.join(self.options)
        for library in self.libraries:
            cmd += ' -l' + library
        if self.output:
            cmd += ' -o ' + self.output
        return cmd + ' %s'

    def link(self, filename):
        self(filename)

    def add_library(self, library):
        if type(library) is not str:
            raise TypeError, 'Library name should be given as a string.'
        if library.startswith('-l'):
            self.libraries.append(library[2:])
        else:
            self.libraries.append(library)

