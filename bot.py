#!/usr/bin/python
# -*- coding: ISO-8859-1 -*-
#---------------------------------------------------------------------------#
# Function: Test bot.                                                       #
# Usage: bot.py [options] [command] {[options]}                             #
# Help: run bot.py --help                                                   #
#---------------------------------------------------------------------------#
from optparse import OptionParser
import logging
import sys
import os
import core

if __name__ == '__main__':
    usage = 'usage: %prog [command] {[options]}'
    desc = 'Test bot.'
    parser = OptionParser(usage=usage, description=desc)
    parser.add_option('--compiler', action='store', default='cray',
            help='compile environment in use (default: %default)')
    parser.add_option('--verbose', action='store_true', default=False,
            help='display additional information while running')
    parser.add_option('--debug', action='store_true', default=False,
            help='run in debug mode, i.e. maximum information')

    options, args = parser.parse_args()

    # set logger format etc.
    logging.basicConfig(level=logging.WARNING, format='%(levelname)s ' + \
            '%(message)s @ %(asctime)s %(module)s line %(lineno)s',
            datefmt='%H:%M:%S')
    # set logging thresholds
    if options.debug:
        logging.getLogger('').setLevel(logging.DEBUG)
    elif options.verbose:
        logging.getLogger('').setLevel(logging.WARNING)
    else:
        logging.getLogger('').setLevel(logging.CRITICAL)
    logging.debug('options: %s' % repr(options))
    logging.debug('args: %s' % repr(args))

    # too few arguments?
    if len(args) < 1:
        parser.error('too few arguments')

    cmd = args.pop(0)
    if cmd == 'manifest':
        core.manifest.echo()
    elif cmd == 'add':
        core.manifest.update(args[0])
    elif cmd == 'init':
        if not os.path.exists(core.botdir):
            os.mkdir(core.botdir)
            with open(core.botdir + '/config', 'w') as fp:
                fp.write('# Configuration for\n')
                fp.write('#   github.com/mlouhivu/test-bot.git\n')
            with open(core.botdir + '/manifest', 'w') as fp:
                fp.write('# Manifest of test targets for\n')
                fp.write('#   github.com/mlouhivu/test-bot.git\n')
    elif cmd == 'run':
        core.init_log()
        failed = []
        pwd = os.path.realpath('.')
        result = {True: '[ OK ]', False: '[FAIL]', 'skip': '[SKIP]'}
        print('BUILD   RUN    Target')
        for target in core.manifest:
            os.chdir(target.workdir())
            if target.language() == 'make':
                build = core.make(target)
            elif hasattr(target, 'do_not_link') and target.do_not_link:
                build = core.build(target, options.compiler, link=False)
            else:
                build = core.build(target, options.compiler)
            if not build:
                failed.append(target)
                run = 'skip'
            elif (hasattr(target, 'do_not_link') and target.do_not_link) or \
                    (hasattr(target, 'skip_run') and target.skip_run):
                run = 'skip'
            else:
                run = core.run(target)
            if not run:
                failed.append(target)
            print('{0}  {1}'.format(
                ' '.join([result[x] for x in (build, run)]), str(target)))
            os.chdir(pwd)
        print('')
        if failed:
            print('Oops. {0} targets failed:'.format(len(failed)))
            for target in failed:
                print('  ' + str(target))
        else:
            print('Yippee. All is good.')
    else:
        print('Unknown command: ' + cmd)

    # the end.

