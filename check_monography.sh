#!/usr/bin/env bash

find ../ -type f -name "chapter_*.tex" -print0 | while read -d $'\0' file
do
    ./check_term_biblio.py $file -g ../author/glossary.tex -b ../bibliography.tex
done
