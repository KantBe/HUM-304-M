#!/bin/bash
##

filename=metacritic.csv
i=2
j=1
lines=$(wc -l $filename | awk '{print $1}')

touch meta_genres.csv
echo "Index,URL,Metascore,User Score,Genres" > meta_genres.csv

while (( i <= lines )); do
	meta_url=$(sed "${i}q;d" $filename | cut -d, -f1)

	if [ "$meta_url" != "$old_url" ]; then
		links -dump -codepage UTF-8 -force-html -width 512 $meta_url/details > meta_dump_details.txt
		sleep 0.05
		genres="\"$(grep Genre\(s\) meta_dump_details.txt | cut -d: -f2 | awk '{$1=$1;print}')\""
		metascoreline=$(($(grep -n Metascore meta_dump_details.txt | head -1 | cut -d: -f1)+1))
		metascore=$(sed "${metascoreline}q;d" meta_dump_details.txt | awk '{print $1}')
		userscoreline=$(($(grep -n "User Score" meta_dump_details.txt | head -1 | cut -d: -f1)+1))
		userscore=$(sed "${userscoreline}q;d" meta_dump_details.txt | awk '{print $1}')

		echo -e "$j, $meta_url, $metascore, $userscore, $genres\033[K\r\c"
		echo -e "$j,$meta_url,$metascore,$userscore,$genres" >> meta_genres.csv

		old_url="$meta_url"
		j=$(($j+1))
	fi

	i=$(($i+1))
done