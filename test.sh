#!/bin/bash

echo "Content-type: text/html"
echo ""

read delim

while read nextInput; do
	if [ "$nextInput" ]; then
		name=$(cut -d';' -f2 <<< "$nextInput" | sed 's/ name="\(.*\)"/\1/')
		read _
		unset data
		while read dataLine && [[ ! "$dataLine" =~ ^$delim ]]; do
			data="$data"$'\n'"$dataLine"
		done
		eval $name=\$data
		echo ${!name}
	fi
done

echo "text1 = $text1"
echo "text2 = $text2"
echo "file = $file"
