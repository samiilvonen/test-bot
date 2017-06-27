import subprocess
import config
import core

def serial(command, out=None, err=subprocess.STDOUT):
    if config.compute_node:
        if config.runner == 'aprun':
            command = aprun(command, tasks=1)
        elif config.runner == 'mpirun':
            command = mpirun(command, tasks=1)
        else:
            raise ValueError, 'Unknown runner: %s' % config.runner
    core.log_line(command)
    try:
        subprocess.check_call(command, stdout=out, stderr=err, shell=True)
        return True
    except subprocess.CalledProcessError:
        return False

def parallel(command, tasks=4, threads=None, out=None, err=subprocess.STDOUT):
    if config.runner == 'aprun':
        cmd = aprun(command, tasks, threads)
    elif config.runner == 'mpirun':
        cmd = mpirun(command, tasks, threads)
    else:
        raise ValueError, 'Unknown runner: %s' % config.runner
    core.log_line(cmd)
    try:
        subprocess.check_call(cmd, stdout=out, stderr=err, shell=True)
        return True
    except subprocess.CalledProcessError:
        return False

def aprun(command, tasks=4, threads=None):
    runner = 'aprun -n %d ' % tasks
    if threads:
        runner += '-d %d -e OMP_NUM_THREADS=%d ' % (threads, threads)
    return runner + command

def mpirun(command, tasks=4, threads=None):
    runner = ''
    if tasks and tasks > 1:
        runner = 'mpirun -np %d ' % tasks
    if threads:
        runner = 'OMP_NUM_THREADS=%d ' % threads + runner
    return runner + command
