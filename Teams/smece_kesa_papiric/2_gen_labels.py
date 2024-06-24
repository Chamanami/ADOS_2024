#!/usr/bin/env python3

cfg = '/home/bazina/ADOS_2024/Teams/smece_kesa_papiric/HSV_Thresholds.cfg.yaml'
labeler = '/home/bazina/ADOS_2024/Teams/smece_kesa_papiric/hsv_labeler.py'
images_dir = '/home/bazina/ADOS_2024/Teams/smece_kesa_papiric/dataset/images/'
labels_dir = '/home/bazina/ADOS_2024/Teams/smece_kesa_papiric/dataset/gen_labels/'

import os
import glob
import subprocess
import shutil
from os.path import *

def run_cmd(cmd):
    print(f'Executing command: {cmd}')
    r = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if r.returncode != 0:
        print(f'Failed cmd: {cmd}')
        print(f'Stdout: {r.stdout.decode()}')
        print(f'Stderr: {r.stderr.decode()}')


for subdir in ['train', 'val', 'trash']:
    images_subdir = join(images_dir, subdir)
    labels_subdir = join(labels_dir, subdir)
    os.makedirs(labels_subdir, exist_ok = True)
    
    print(f'Processing images in directory: {images_subdir}')
    
    for img in glob.glob(join(images_subdir, '*.jpg')):
        b = basename(img)
        c, e = splitext(b)
        label = join(labels_subdir, c + ".txt")
        
        print(f'Generating labels for image: {img}')
        run_cmd(f'python3 {labeler} {cfg} {img} {label}')

