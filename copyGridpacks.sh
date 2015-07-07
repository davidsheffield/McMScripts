#!/bin/bash

################################
#
# copyGridpacks.sh
#
#  Script to copy gridpacks from CSV file to EOS. Gridpacks will be
#  automatically copied to the cvmfs respository.
#
#  author: David G. Sheffield (Rutgers)
#
################################

source  /afs/cern.ch/cms/cmsset_default.sh

IFS=,

csvfile=""

while [ "$1" != "" ]; do
    case $1 in
	-h | --help) echo "Usage: sh copyGridpacks.sh file.csv"
	    exit
	    ;;
	*) csvfile=$1
	    ;;
    esac
    shift
done

if [ ! -f $csvfile ]; then
    echo "Error: File ${csvfile} does not exist"
    echo "Usage: sh copyGridpacks.sh file.csv"
    exit 1
fi

echo "Copying $(($(wc -l < ${csvfile}) - 1)) gridpacks to /store/group/phys_generator/cvmfs/gridpacks/"

ind_local=-1
ind_final=-1

isFirstLine=1
while read -a line; do
    if [ $isFirstLine == 1 ]; then
	for i in "${!line[@]}"; do
	    if [ "${line[i]}" == "Local gridpack location" ]; then
		ind_local=$i
	    fi
	    if [ "${line[i]}" == "Gridpack location" ]; then
		ind_final=$i
	    fi
	done

	if [ $ind_local == -1 ] && [ $ind_final == -1 ]; then
	    echo 'Error: Could not find "Gridpack location" or "Local gridpack location" in ${csvfile}.'
	    exit 2
	elif [ $ind_local == -1 ]; then
	    echo 'Error: Could not find "Local gridpack location" in ${csvfile}.'
	    exit 2
	elif [ $ind_final == -1 ]; then
	    echo 'Error: Could not find "Gridpack location" in ${csvfile}.'
	    exit2
	fi

	isFirstLine=0
	continue
    fi

    local_file=${line[ind_local]}
    final_file=${line[ind_final]}
    final_file_eos=$(sed 's/cvmfs\/cms\.cern\.ch\/phys_generator/store\/group\/phys_generator\/cvmfs/'\
	    <<< $final_file)
    final_dir_eos=$(dirname "${final_file_eos}")
    name=$(basename $local_file)

    eos ls -s $final_dir_eos 2> /dev/null
    if [ $? != 0 ]; then
	echo "${final_dir_eos} does not exist. Creating it."
	eos mkdir -p $final_dir_eos
    fi

    cmsStage $local_file $final_dir_eos

    if [ $? == 0 ]; then
	echo -e "\033[0;32m${name}\033[0m"
    else
	echo -e "\033[0;31mFailed to copy ${local_file}\033[0m"
    fi
done < $csvfile