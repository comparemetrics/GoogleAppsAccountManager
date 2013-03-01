import os
import os.path
import sys
import time
import signal
import random

def credentialDaemon(data=None):

    try:
        pid = os.fork()
    except OSError:
        sys.stderr.write("Cannot be a daemon.\n")
        return False
    
    if pid > 0:
        return True
    print pid
    
    try:
        os.setpgid(pid, 0)
    except OSError:
        sys.stderr.write("Cannot be a member of init process id group.\n")
        return False
    
    # Set credential FIXME
    with open("/tmp/

    # Function for signale handler
    def _exit(signum, frame):
        sys.exit(0)

    # Set Signal handler
    signal.signal(signal.SIGALRM, _exit)

    # Time limit
    signal.alarm(300)

    # Daemonize
    signal.pause()

