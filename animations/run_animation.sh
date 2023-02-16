#!/bin/bash

if [ -z ${1+x} ]; then 
    echo "Usage: ./run_animation.sh [scene-name]";
    echo "Available scene names: "
    ./get_scene_names.sh
    exit 1
fi

python3 -m manim -p -ql animations.py ${1} 
