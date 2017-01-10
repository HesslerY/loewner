#!/bin/bash

# Line where drive_func assignment takes place
drive_line=44

# Partial string for drive_func assignment code
drive_code="        drive_func ="

# Array of possible driving functions
drive_options=("0" "T" "cos(T)" "cos(T * pi)" "T * cos(T)" "T * cos(T * pi)" "sin(T)" "T * sin(T)" "sin(T * pi)" "T * sin(T * pi)")

# Ask for drive function selection
for (( i=0; i<${#drive_options[*]}; i++ )) do

	echo "[$i] ${drive_options[$i]}"
	
done

echo "Select a driving function:"

# Store user input as variable
read drive_selection

# Print to verify read worked correctly
# echo "${drive_options[$drive_selection]}"

# Copy file just in case
cp loewner.f90 loewner_backup.f90

# Change file in light of user selection
sed -i "$drive_line s/.*/$drive_code ${drive_options[$drive_selection]}/" loewner.f90

# Compile and execute Loewner code
gfortran loewner.f90 -o loewner.out
./loewner.out

# Plot results with Python
python plot.py
