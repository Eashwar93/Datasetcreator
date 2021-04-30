#!/bin/bash
python python_scripts/labelme2cityscapes.py --json_input_dir ~/Dataset/Rexroth/labels/train/ --output_dir ~/Dataset/Rexroth/labels/train/
python python_scripts/labelme2cityscapes.py --json_input_dir ~/Dataset/Rexroth/labels/test/ --output_dir ~/Dataset/Rexroth/labels/test/