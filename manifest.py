import os
import re
from target import Target
import core

ro_target = re.compile('\[\s*(?P<target>[^]]+)\s*\](?P<definition>[^[]*)')
ro_assign = re.compile('(?P<all>(?P<key>[a-zA-Z0-9_.-]+)='
        + '''(?P<value>["'].*["']|[a-zA-Z0-9_./-]+))''')
ro_tag = re.compile('(^|\s+)\+(?P<tag>\w+)')
ro_word = re.compile('''["'](.*)["']|(\w+)''')

class Manifest(object):
    def __init__(self, filename):
        self.targets = []
        self.read(filename)

    def __iter__(self):
        return iter(self.targets)

    def read(self, filename):
        if not os.path.isfile(filename):
            raise ValueError, 'File does not exist: %s' % str(filename)
        self.__filename__ = filename
        with open(filename) as fp:
            txt = fp.read()
        for match in ro_target.finditer(txt):
            path = match.group('target')
            snippet = match.group('definition')
            args = {}
            # find all tags
            for m in ro_tag.finditer(snippet):
                tag = m.group('tag')
                args[tag] = True
                snippet = snippet.replace(tag, '', 1)
            # find all arguments in long-form ...
            for m in ro_assign.finditer(snippet):
                args[m.group('key')] = m.group('value')
                snippet = snippet.replace(m.group('all'), '', 1)
            # ... and in short-form
            snippet.strip()
            if snippet:
                words = []
                for word in ro_word.finditer(snippet):
                    words.append(word.group(0) or word.group(1))
                if len(words) == 2:
                    args['type'] = words[0]
                    args['reference'] = words[1]
            self.add_target(path, args)

    def add_target(self, path, args={}):
        if path not in self.targets:
            self.targets.append(Target(path, **args))
        else:
            i = self.targets.index(path)
            self.targets[i].define(**args)

    def __repr__(self):
        return "Manifest('{0}')".format(self.__filename__)

    def echo(self):
        for target in self.targets:
            target.echo()
            print('')

    def update(self, source):
        new = []
        for root, dirs, files in os.walk(source):
            root = os.path.realpath(root)
            for name in files:
                path = root + '/' + name
                if path not in self:
                    new.append(os.path.relpath(path))
            prune = []
            for name in dirs:
                if name.startswith(core.botdir):
                    prune.append(name)
                    continue
                path = os.path.realpath(root + '/' + name)
                makefile = path + '/Makefile'
                if os.path.exists(makefile):
                    if path not in self:
                        new.append(os.path.relpath(path))
                    prune.append(name)
            for x in prune:
                dirs.remove(x)
        if new:
            print('New targets:')
            for target in new:
                print('  ' + target)
        with open(self.__filename__, 'a') as fp:
            for target in new:
                fp.write('\n[{0}]\n  type=pass\n'.format(target))
