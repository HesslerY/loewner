#!/bin/bash

# Line where drive_func assignment takes place in loewner.f90 file
drive_line=25

# Partial string for drive_func assignment code
drive_code="    drive ="

# Array of possible driving functions
drive_options=("0.0"
               "t"
               "cos(t)"
               "cos(t * pi)"
               "t * cos(t)"
               "t * cos(t * pi)"
               "sin(t)"
               "sin(t * pi)"
               "t * sin(t)"
               "t * sin(t * pi)"
               "2 * sqrt(1 * (1 - t))"
               "2 * sqrt(3.5 * (1 - t))"
               "2 * sqrt(4 * (1 - t))"
               "2 * sqrt(6 * (1 - t))"
               "2 * sqrt(8 * (1 - t))"
               "ALL")
               
# Copy file just in case
cp loewner.F03 loewner_backup.F03

# Make an output directory if it does not already exist
# Delete all items in directory if it does exist
if [ ! -d "output" ]; then
    mkdir "output"
elif [ "$(ls output)" != "" ]; then
    rm -r output/*
fi

function read_input()
{   
    # Ask for drive function selection
    echo "Select a driving function:"
    
    # Display all driving function options
    for (( i=0; i<${#drive_options[*]}; i++ )) do

	    echo "[$i] ${drive_options[$i]}"
	
    done
    
    # Store user input as variable
    read drive_selection
    
    # Ask for drive function selection
    echo "Enter the max time:"
    
    # Store user input as variable
    read max_time
}


function all_drive()
{
    # Call run_loewner for all but last element in driving function array
    for (( i=0; i<$((${#drive_options[*]} - 1)); i++ )) do

        run_loewner "${drive_options[$i]}" "$max_time" "$i"
	
    done
}

function run_loewner()
{
    # Change file in light of user selection
    sed -i "$drive_line s/.*/$drive_code $1/" loewner.F03
    
    # Compile and execute Loewner code
    gfortran loewner.F03 -o loewner.out
    ./loewner.out "$2"
    
    # Plot results with Python
    python plot.py "$3"
    
    rm -r result.txt
    
    # echo "Completed execution for $1"
}

# Ask for user input
read_input

# Run for all driving functions in case of ALL
if [ "${drive_options[$drive_selection]}" == "ALL" ]; then

    all_drive
    nemo "output"
    exit
fi

# Run for driving function selection
run_loewner "${drive_options[$drive_selection]}" "$max_time" "$drive_selection"
nemo "output"

