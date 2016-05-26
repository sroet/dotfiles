#!/usr/bin/env python
import sys
import os
import pexpect
import getpass
def main():
    user = getpass.getuser()
    pwd = getpass.getpass()
    log = open('temp.log','bw+')
    # Get current running jobs carbon
    carbon_name = user + '@carbon.science.uva.nl'
    carbon = pexpect.spawn('ssh ' + carbon_name)
    carbon.logfile_read = log
    carbon.expect('Password:')
    carbon.send(pwd + '\n')
    carbon.expect('$')
    carbon.send('qstat | grep -B 1 '+user+'\n')
    carbon.expect('$')
    carbon.send('logout\n')
    carbon.expect(pexpect.EOF)
    carbon.close()
    log.seek(0, 0)
    for line in log:
        if (user.encode() in line or 'compute'.encode() in line) and \
            ('grep'.encode() not in line):
            print(line.decode())
    log.truncate(0)
    log.close
    child = pexpect.spawn('rm temp.log')
    child.expect(pexpect.EOF)

#Only calls main when this is the main script.
if __name__ == "__main__":main()

