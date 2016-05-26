#!/bin/bash 

# Takes just a job id number. Needs to be in the same directory as the
# *.o$jobid file, but extracts relevant info from that and pulls your data
# off the compute node

jobid=$1

njobf=`ls -1 *.o$jobid | wc -l`
if [ $njobf -gt 1 ]
then
    echo "Huh. We seem to have more than one file fitting that description."
    echo "Here they all are: "
    ls *.o$jobid
    exit 1
elif [ $njobf -lt 1 ]
then
    echo "Can't find the desired job file. Are we in the right directory?"
    exit 1
fi

ofile=`ls *.o$jobid`
echo $ofile

compute_host=`head -n 1 $ofile | awk '{print $3}'`
jobname=`grep "^JOB_NAME\=" $ofile | sed 's/JOB_NAME\=//'`
compute_dir="/state/partition1/${USER}/${jobname}-${jobid}"
local_dir=`grep "^SGE_O_WORKDIR\=" $ofile | sed 's/SGE_O_WORKDIR\=//'`

echo "scp -r ${compute_host}:${compute_dir}/* ${local_dir}/${jobname}-${jobid}/"
scp -r ${compute_host}:${compute_dir}/* ${local_dir}/${jobname}-${jobid}/

