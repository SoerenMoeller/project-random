#!/bin/zsh

if [ -z ${1+x} ]; then 
    echo "Usage: ./run_example.sh [scene-name]";
    echo "Available scene names: "
    ./get_scene_names.sh
    exit 1
fi

python3 -m manim -p -ql example.py ${1} 
