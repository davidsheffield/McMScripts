#!/bin/bash

################################
#
# copyPrivateLHEs.py
#
#  Script to copy privately produced LHE files to EOS and store their article
#  in a CSV file to be used by manageRequests.py.
#
#  author: David G. Sheffield (Rutgers)
#
################################

IFS=,

inputFile=""
outputFile=""
force=0
add=0
rename=0
while [ "$1" != "" ]; do
    case $1 in
	-o) shift
	    outputFile=$1
	    ;;
	-f) force=1
	    ;;
	-a) add=1
	    ;;
	-r) rename=1
	    ;;
	-h | --help) echo "Usage: sh copyPrivateLHEs.sh inputFile [-o outputFile] [-f]"
	    echo "        inputFile    CSV file with location of LHE files."
	    echo "    -o outputFile    CSV file to store EOS article numbers and values from inputFile."
	    echo "                     Default: inputFile=file.lhe produces outputFile=file_EOS.lhe."
	    echo "               -f    Force outputFile to be overwritten."
	    echo "               -a    Add new rows to outputFile if it already exists."
	    echo "               -r    Rename LHE files to dataset name."
	    exit
	    ;;
	*) inputFile=$1
	    ;;
    esac
    shift
done

if [ "${inputFile}" == "" ]; then
    echo "Error: No input file provided."
    exit 1
fi

if [ ! -f $inputFile ]; then
    echo "Error: The file ${inputFile} does not exist."
    exit 1
fi

if [ "${outputFile}" == "" ]; then
    outputFile=$(echo $inputFile | sed 's/\.csv$/_EOS.csv/')
elif [ "${inputFile}" == "${outputFile}" ]; then
    echo "Error: Cannot have both output and input files be ${inputFile}"
    exit 1
fi

if [ -f $outputFile ]; then
    if  [ $force == 1 ]; then
	rm $outputFile
    elif [ $add != 1 ]; then
	echo "Error: The output file ${outputFile} already exists."
	echo "       Use the flag -f to force overwrite it or -a to add to it."
	exit 1
    fi
elif [ $add == 1 ]; then
    echo "Error: The output file ${outputFile} does not exist. Cannot add to it."
    exit 1
fi

echo "Copying $(($(wc -l < ${inputFile}) - 1)) LHE files to EOS"

home_dir=$PWD
inputFile="${home_dir}/${inputFile}"
outputFile="${home_dir}/${outputFile}"
work_dir="tmp_pLHE_work"
mkdir ${work_dir}
cd ${work_dir}

ind=-1
ind_dataset=-1
failures=0

isFirstLine=1
while read -a line; do
    if [ $isFirstLine == 1 ]; then
	for i in "${!line[@]}"; do
	    if [ "${line[i]}" == "LHE" ]; then
		ind=$i
	    elif [ "${line[i]}" == "Dataset name" ]; then
		ind_dataset=$i
	    fi

	    if [ $add != 1 ]; then
		echo -n "${line[i]}," >> $outputFile
	    fi
	done
	if [ $add != 1 ]; then
	    echo "EOS" >> $outputFile
	fi

	if [ $ind == -1 ]; then
	    echo 'Error: Could not find "LHE" in ${inputFile}.'
	    exit 2
	fi
	if [ $rename == 1 ] && [ $ind_dataset == -1 ]; then
	    echo 'Error: Could not find "Dataset name" in ${inputFile}.'
	fi

	isFirstLine=0
	continue
    fi

    for i in "${!line[@]}"; do
	echo -n "${line[i]}," >> $outputFile
    done

    file=${line[ind]}
    name=$(basename $file)
    if [ $rename == 1 ]; then
	name="${line[ind_dataset]}.lhe"
    fi

    cp $file $name

    copy_output="tmpoutput"
    cmsLHEtoEOSManager.py -n -c -f $name > $copy_output

    article_id=$(grep -Po "(?<=Creating new article with identifier )\d*" $copy_output)

    if [ "${article_id}" == "" ]; then
	echo -e "\033[1;31mFailed to copy ${name}.\033[1;m"
	echo "" >> $outputFile
	failures=$((failures + 1))
    else
	if [ $(grep "Checksum OK" $copy_output) ]; then
	    echo -e "\033[1;32mCopied ${name} to ${article_id}.\033[1;m"
	    echo "${article_id}" >> $outputFile
	else
	    echo -e "\033[1;31mFailed to correctly copy ${name} to ${article_id}. Checksums do not match.\033[1;m"
	    echo "BAD${article_id}CHECKSUM" >> $outputFile
	    failures=$((failures + 1))
	fi
    fi

    name_xz="${name}.xz"
    rm $name_xz

done < $inputFile

cd $home_dir
rm -r ${work_dir}

if [ $failures == 0 ]; then
    echo "Successfully copied all LHE files."
else
    echo "Failed to copy ${failures} LHE files."
fi
