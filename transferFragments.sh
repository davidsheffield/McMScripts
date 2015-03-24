#!/bin/bash

originDirectory=$1
originFiles="${originDirectory}*13TeV*.py"
targetDirectory=$2

echo "Copying from ${originDirectory}"
echo "to ${targetDirectory}"
echo ""

for file in ${originFiles}; do
    name=`basename ${file}`
    modifiedName=`echo ${name} | sed 's/_13TeV/_TuneCUETP8M1_13TeV/g'`
    targetFile=${targetDirectory}${modifiedName}
    cp ${file} ${targetFile}
    echo "copied ${name} -> ${modifiedName}"
done
