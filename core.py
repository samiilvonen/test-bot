import subprocess
import commands
import os
import time
from manifest import Manifest
from config import Config
import execute

botdir = '.bot'
if os.path.exists(botdir):
    manifest = Manifest(botdir + '/manifest')
    config = Config(botdir + '/config')
    log = open(botdir + '/loki', 'a')
basedir = os.path.realpath('.')

def guess_binary(pre, post):
    files = list(post.difference(pre))
    prune = []
    for name in files:
        if name.endswith(('.o', '.mod', '.MOD')):
            prune.append(name)
    files = [x for x in files if x not in prune]
    if not len(files):
        return None
    return files[0]

def make(target):
    pre_log(target, 'make')
    if hasattr(target, 'makefile') and target.makefile:
        cmd = 'make -f ' + target.filename()
    else:
        cmd = 'make'
    pre = set([x for x in os.listdir('.') if os.path.isfile(x)])
    try:
        subprocess.check_call(cmd, stdout=log, stderr=subprocess.STDOUT,
                shell=True)
        post = set([x for x in os.listdir('.') if os.path.isfile(x)])
        binary = guess_binary(pre, post)
        if binary and not hasattr(target, 'binary'):
            target.binary = str(binary)
        return True
    except subprocess.CalledProcessError:
        return False
    finally:
        post_log(target)

def build(target, family, output=None, link=True):
    pre_log(target, 'build')
    flavours = []
    if target.mpi:
        flavours.append('mpi')
    if target.omp:
        flavours.append('omp')
    cc = config.compiler(family, target.language(), flavours, link=link)
    link = config.linker(family, target.language(), flavours)
    if output:
        cc.output = output
    elif hasattr(target, 'binary'):
        cc.output = target.binary
    if not link:
        cc.output = None
    cc.stdout = log
    cc.stderr = log
    cc.compile(target.filename())
    post_log(target)
    return True

def run(target):
    pre_log(target, 'run')
    binary = './a.out'
    try:
        if hasattr(target, 'binary'):
            binary = './' + target.binary
        if target.mpi and target.omp:
            tasks = config.mpi_tasks or 4
            threads = config.omp_threads or 4
            return execute.parallel(binary, tasks, threads, out=log)
        elif target.mpi:
            tasks = config.mpi_tasks or 4
            return execute.parallel(binary, tasks, out=log)
        elif target.omp:
            tasks = 1
            threads = config.omp_threads or 4
            return execute.parallel(binary, tasks, threads, out=log)
        else:
            return execute.serial(binary, out=log)
    finally:
        post_log(target)

def init_log():
    log.write('\n' + '#'*80 + '\n')
    log.write('Run started at {0}\n'.format(time.asctime()))
    log_modules()
    log.flush()

def pre_log(target, mode):
    line = '[-- Start of ' + str(mode).upper() + ' ' + str(target) + ' '
    while len(line) < 78:
        line += '-'
    line += ']'
    log.write('\n' + line + '\n')
    log.flush()

def post_log(target):
    line = '[-- End of ' + str(target) + ' '
    while len(line) < 78:
        line += '-'
    line += ']'
    log.write('\n' + line + '\n')
    log.flush()

def log_line(txt):
    log.write(txt + '\n')
    log.flush()

def log_modules():
    status, out = commands.getstatusoutput('module list')
    log_line('')
    log.write(out.rstrip('\n') + '\n')
