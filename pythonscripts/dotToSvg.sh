for FILE in $(find -name "*.dot")
do
 echo "$FILE"
 dot -Tsvg -o"${FILE%.dot}.svg" "$FILE"
done 
