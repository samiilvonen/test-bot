import os
import re
from target import Target

ro_target = re.compile('\[\s*(?P<target>[^]]+)\s*\](?P<definition>[^[]*)')
ro_assign = re.compile('(?P<all>(?P<key>[a-zA-Z0-9_.-]+)='
        + '''(?P<value>["'].*["']|[a-zA-Z0-9_./-]+))''')
ro_tag = re.compile('(^|\s+)\+(?P<tag>\w+)')
ro_word = re.compile('''["'](.*)["']|(\w+)''')

class Manifest(object):
    def __init__(self, filename=None):
        self.targets = []
        self.read(filename)

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
                snippet.replace(tag, '', 1)
            # find all arguments in long-form ...
            for m in ro_assign.finditer(snippet):
                args[m.group('key')] = m.group('value')
                snippet.replace(m.group('all'), '', 1)
            # ... and in short-form
            snippet.strip()
            if snippet:
                words = []
                for word in ro_word.finditer(snippet):
                    words.append(word[0] or word[1])
                if len(words) == 2:
                    args['type'] = words[0]
                    args['reference'] = words[1]
            self.add_target(path, args)

    def add_target(path, args={}):
        if path not in self.targets:
            self.targets.append(Target(path, **args))
        else:
            i = self.targets.index(path)
            self.targets[i].define(**args)

    def __repr__(self):
        print('Manifest({0})'.format(self.__filename__))

    def echo(self):
        for target in self.targets:
            target.echo()
            print('')
