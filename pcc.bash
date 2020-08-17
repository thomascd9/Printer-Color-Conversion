#!/bin/bash

tag=""
printer="HP_Deskjet_3900"
printoptions="-o fit-to-page"
pyfile="/Users/thomas/Programming/Python/pcc/pcc.py"
tempname="IJWRJj6pRyay1PlmpGGz"

if [ $# -eq 4 ]; then
	python3 $pyfile $1 $tempname $2 $3 $4
	tag=$4
elif [ $# -eq 3 ]; then
	python3 $pyfile $1 $tempname $2 $3
elif [ $# -eq 2 ]; then
	python3 $pyfile $1 $tempname $2
	tag=$2
elif [ $# -eq 1 ]; then
	python3 $pyfile $1 $tempname
else
	echo "Error with input arguments"
	exit 1
fi

# Actual printing using lp
if [[ $tag == "-d" ]]; then
	file1="${tempname}1.pdf"
	file2="${tempname}2.pdf"
	if test -f $file2; then
		lp -d $printer $file2 $printoptions

		read -p "Ready for reverse pages? " -r
		if [[ $REPLY =~ ^[Yy]$ ]]
		then
    		lp -d $printer $file1 $printoptions
			rm $file1
			rm $file2
		fi
	else
		lp -d $printer $file1 $printoptions
		rm $file1
	fi
else
	file="${tempname}.pdf"
	lp -d $printer $file $printoptions
	rm $file
fi

open ~/Library/Printers/HP\ Deskjet\ 3900.app/
