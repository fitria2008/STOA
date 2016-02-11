#!/bin/sh
for FILE in $(find $1 ! -name "*.*" ! -name "." ! -name ".*" -type f)
do
 echo "$FILE"
 python get_apsp.py $FILE
done 
