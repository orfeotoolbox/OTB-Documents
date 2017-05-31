#!/bin/bash

exercises=( "ex1_HelloWorld" "ex2_Pipeline" "ex3_Filter" "ex4_CreateApplication")

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
