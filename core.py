import subprocess
from manifest import Manifest
from config import Config

manifest = Manifest('.bot/manifest')
config = Config('.bot/config')

def make(target):
    try:
        subprocess.check_call('make', stdout=None, stderr=subprocess.STDOUT,
                shell=True)
        return True
    except subprocess.CalledProcessError:
        return False

def build(target, family):
    flavours = []
    if target.mpi:
        flavours.append('mpi')
    if target.omp:
        flavours.append('omp')
    cc = config.compiler(family, target.language(), flavours)
    link = config.linker(family, target.language(), flavours)
    if hasattr(target, 'output'):
        cc.output = target.output
    cc.compile(target)
    return True

def run(target):
    binary = './a.out'
    if hasattr(target, 'output'):
        binary = './' + target.output
    if target.mpi and target.omp:
        tasks = config.mpi_tasks or 4
        threads = config.omp_threads or 4
        return execute.parallel(binary, tasks, threads)
    elif target.mpi:
        tasks = config.mpi_tasks or 4
        return execute.parallel(binary, tasks)
    elif target.omp:
        threads = config.omp_threads or 4
        return execute.serial(binary, threads)
    else:
        return execute.serial(binary)

