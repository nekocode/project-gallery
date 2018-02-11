#!/bin/bash
if [ "$1" == "txt" ]; then
   ./data/generator.py --token="$(< token)" --txt_out=data/data.txt --sort_by=stars
elif [ "$1" == "js" ]; then
   ./data/generator.py --token="$(< token)" --txt_in=data/data.txt --js_out=data/data.js
fi