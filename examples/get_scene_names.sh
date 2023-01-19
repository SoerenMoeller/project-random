#!/bin/zsh

grep -E "class" example.py | while read -r line ; do
    echo "    - $line" | sed -e "s/class //"  | sed "s/(.*)://"
done
