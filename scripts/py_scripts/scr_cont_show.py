#!/usr/bin/env python
import sys
import os
import subprocess
import pexpect

def main():
    #Gets xtc file from command line.
    if len(sys.argv) == 1 or  sys.argv[1].endswith('.xtc') is False:
        print("Which trajectory (.xtc) file?")
        return 1
    xtc_file = str(sys.argv[1])
    file_name = xtc_file.rsplit('.', 1)[0]
    print("##"+file_name+"##\n")

    #Find gro, tpr.
    #Opens a pipe to take the output, shell = true is needed because of the *.
    grolist = subprocess.Popen('ls -1t *gro', stdout = subprocess.PIPE, shell=True)
    grofile_list, err = grolist.communicate()
    tprlist = subprocess.Popen('ls -1t *tpr', stdout = subprocess.PIPE, shell = True)
    tprfile_list, err = tprlist.communicate()

    #Only takes the first item, need decode because the list is in bytes not str.
    grofile = grofile_list.decode('utf8').split('\n', 1)[0]
    tprfile = tprfile_list.decode('utf8').split('\n', 1)[0]
    print('Using '+grofile+' and '+tprfile+'..\n')

    #Set start and end points for centering.
    start = '1'
    end = '166'
#    pwd = 'pwd'

    #Make index file for centering on the first monomer
    print('Making index file from resid '+start+'-'+end+'.')

    #Opens the log file.
    ndx_log = open('ndx.log','wb+')
    ndx = pexpect.spawn('make_ndx -f '+grofile, logfile=ndx_log)
    #Wait for input token and then applies input.
    ndx.expect(['\n>'])
    ndx.send('keep 0\n')
    ndx.expect(['\n>'])
    ndx.send(str('0&ri'+start+'-'+end+'&aCA\n'))
    ndx.expect(['\n>'])
    ndx.send('q\n')

    #Wait for the programm to finish.
    ndx.expect(pexpect.EOF, timeout=None)
    ndx_log.close()

    #Runs the sequence of trjconv with different inputs
    prev = file_name

    #Declaring input for trjconv.
    for i in ['nojump','whole','center','compact','fit','dump']:
        print('Running trjconv of '+i+'.')
        trj_log = open(i+'.log','wb+')

        if i == 'dump':
            prev = 'vis-'+file_name

        new_input = ['trjconv','-f',prev+'.xtc','-s',tprfile,'-o',i+'.xtc']

        if i == 'nojump' or i == 'whole':new_input.extend(['-pbc',i])
        if i == 'center':new_input.extend(['-n','index.ndx','-'+i])
        if i == 'compact':new_input.extend(['-ur',i,'-pbc','res'])
        if i == 'dump':
            new_input[-1]='vis-'+file_name+'.pdb'
            new_input.extend(['-dump','100100'])
        if i == 'fit':
            new_input[-1] = 'vis-'+file_name+'.xtc'
            new_input.extend(['-fit','rot+trans','-n','index.ndx'])
        new_input2 = ' '.join(new_input)
#        print(new_input2)
        #Call trjconv with the input and set the read output to the logfile.
        trj = pexpect.spawn(new_input2)
        trj.logfile_read = trj_log

        #Selects protein for centering
        if i == 'center' or i == 'fit':
            trj.expect('Select a group:')
            trj.send('1\n')

        #Selects system for output.
        trj.expect('Select a group:')
        trj.send('0\n')

        #Waits for the programm to end and closes the log.
        trj.expect(pexpect.EOF, timeout=None)
        trj_log.close()

        #Sets previous step to i.
        prev = i

    #Checks if vis-*.gro and vis-*.xtc exist and delete the other files
    if os.path.isfile('vis-'+file_name+'.pdb') and os.path.isfile('vis-'+file_name+'.xtc'):
        subprocess.Popen(['rm','nojump.xtc','whole.xtc','center.xtc','compact.xtc'])
    else:
        print('No vis-'+file_name+'.pdb or vis-'+file_name+'.xtc, check log files!\n')

def pipe_write(proc,string):
    #Gets an open subprocess(proc) and flushes a string to its input.
    coded = string.encode()
    proc.stdin.write(coded)
    #Needed because of block-buffering issues.
    proc.stdin.flush()

#Only calls main when this is the main script.
if __name__ == "__main__":main()

