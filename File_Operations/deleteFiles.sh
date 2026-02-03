#!/bin/bash

grep -o "18may.*" deleteHidden.donedict > filesToModify.txt

sed 's/.$//' filesToModify.txt > filesModified.txt

sed 's/$/.mrc/' filesModified.txt > filesToDelete.txt

for i in $(cat filesToDelete.txt)
do
   rm "$i"
done

rm files*
