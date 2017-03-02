#!/bin/bash

total_lines=$(wc -l < result.txt)

echo "Enter number of iterations:"
read n_iterations

prog=$(echo "print(str($total_lines/$n_iterations * 100)[:5])" | python)

echo "$total_lines/$n_iterations"
echo $prog "%"
