#!/bin/bash

index_file=$(dirname "$0")/SUMMARY.md
template_file==$(dirname "$0")/template/eisvogel.tex
md_files=$(grep -Poz "\(.*md" $index_file  | tr '(' " "| tr -d '\0')
tex_files=graphics.tex
file_name=EBcL_SDK.pdf

while [[ "$#" -gt 0 ]]; do
    case $1 in
        -md) md_files="$2"; shift ;;
        -tex) tex_files="$2"; shift ;;
        -o) file_name="$2"; shift ;;
        *) echo "Unknown parameter passed: $1"; exit 1 ;;
    esac
    shift
done

pandoc $tex_files $md_files -o $file_name --pdf-engine=lualatex --from markdown \
 --template $template_file --listings --resource-path=assets
