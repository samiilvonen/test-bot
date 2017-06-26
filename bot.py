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
    elif cmd == 'run':
        failed = []
        # build
        print('BUILD')
        for target in core.manifest:
            if target.language == 'make':
                ok = core.make(target)
            else:
                ok = core.build(target, options.compiler)
            if ok:
                print('[ OK ]  ' + str(target))
            else:
                print('[FAIL]  ' + str(target))
                failed.append(target)
        # run
        print('\nRUN')
        for target in core.manifest:
            if target in failed:
                print('[SKIP]  ' + str(target))
            if core.run(target):
                print('[ OK ]  ' + str(target))
            else:
                print('[FAIL]  ' + str(target))
                failed.append(target)
        if failed:
            print('Oops. {0} targets failed:'.format(len(failed)))
            for target in failed:
                print('  ' + str(target))
        else:
            print('Yippee. All is good.')

    # the end.

