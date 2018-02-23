#!/bin/bash
if [ "$1" == "list-txt" ]; then
   ./data/generator.py --token="$(< token)" --list_txt_out=data/list_data.txt --sort_by=stars
elif [ "$1" == "list-js" ]; then
   ./data/generator.py --token="$(< token)" --list_txt_in=data/list_data.txt --list_js_out=data/list_data.js
elif [ "$1" == "ui-js" ]; then
   ./data/generator.py --token="$(< token)" --ui_js_out=data/ui_data.js
fi