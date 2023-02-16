#!/bin/bash

grep -E "class" animations.py | while read -r line ; do
    echo "    - $line" | sed -e "s/class //"  | sed "s/(.*)://"
done
