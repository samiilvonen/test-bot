import os
import core

defaults = {
        'type': 'pass',
        'reference': None,
        'mpi': False,
        'omp': False,
        }


class Target(object):
    def __init__(self, path, **kwargs):
        self.__keys__ = set()
        self.setup(path)
        args = defaults.copy()
        args.update(kwargs)
        self.define(**args)

    def setup(self, path):
        try:
            if os.path.exists(path):
                self.name = path
            else:
                raise ValueError, 'Target path does not exist.'
        except TypeError:
            raise TypeError, 'Invalid target path: ' + repr(path)

    def path(self):
        return os.path.join(core.basedir, self.name)

    def define(self, **args):
        for key,value in args.items():
            setattr(self, key, value)
            self.__keys__.add(key)

    def __cmp__(self, other):
        return cmp(str(self), str(other))

    def __str__(self):
        return str(self.name)

    def __repr__(self):
        keys = self.__keys__.difference(
                set(['type', 'reference', 'mpi', 'omp']))
        extras = ', '.join(['%s=%s' % (k, getattr(self, k)) for k in keys])
        if extras:
            extras = ', ' + extras
        return 'Target({0}, type={1}, reference={2}, mpi={3}, omp={4}{5})'\
                .format(self.name, self.type, self.reference, self.mpi,
                        self.omp, extras)

    def echo(self):
        print('Target: {0}'.format(str(self)))
        print('  type=' + str(self.type))
        print('  reference=' + str(self.reference))
        print('  MPI=' + str(self.mpi))
        print('  OpenMP=' + str(self.omp))
        keys = self.__keys__.difference(
                set(['type', 'reference', 'mpi', 'omp']))
        for key in keys:
            print('  {0}={1}'.format(key, getattr(self, key)))

    def isdir(self):
        return os.path.isdir(self.path())

    def isfile(self):
        return os.path.isfile(self.path())

    def language(self):
        if self.isdir():
            if os.path.exists(self.path() + '/Makefile'):
                return 'make'
        if self.isfile():
            if str(self).lower().endswith(('.c')):
                return 'c'
            if str(self).lower().endswith(('.f', '.f90', '.f77')):
                return 'fortran'
        return None

    def workdir(self):
        if self.isdir():
            return self.path()
        return os.path.dirname(self.path())
