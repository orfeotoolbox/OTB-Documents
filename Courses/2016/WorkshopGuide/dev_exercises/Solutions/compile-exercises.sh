#!/bin/bash

exercises=( "ex1_HelloWorld" "ex2_Pipeline" "ex3_Filter" "ex4_CreateApplication")

source ~/tools/load_otb_develop.sh

for exo in "${exercises[@]}"
do
    echo "Build $exo..."
    cd $exo
    mkdir -p bin
    cd bin
    cmake ..
    make
    cd ../..
done
