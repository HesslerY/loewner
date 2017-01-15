#!/bin/bash

# Line where drive_func assignment takes place in loewner.f90 file
drive_line=25

# Partial string for drive_func assignment code
drive_code="    drive ="

# Array of possible driving functions
drive_options=("0"
               "T"
               "cos(T)"
               "cos(T * pi)"
               "T * cos(T)"
               "T * cos(T * pi)"
               "sin(T)"
               "sin(T * pi)"
               "T * sin(T)"
               "T * sin(T * pi)"
               "2 * sqrt(K * (1 - T))"
               "2 * sqrt(1 * (1 - T))"
               "2 * sqrt(3.5 * (1 - T))"
               "2 * sqrt(4 * (1 - T))"
               "2 * sqrt(6 * (1 - T))"
               "2 * sqrt(8 * (1 - T))"
               "ALL")
               
# Copy file just in case
cp loewner.F90 loewner_backup.F90

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
}


function all_drive()
{
    # Call run_loewner for all but last element in driving function array
    for (( i=0; i<$((${#drive_options[*]} - 1)); i++ )) do

	    run_loewner "${drive_options[$i]}" "$i"
	
    done
}

function run_loewner()
{
    # Change file in light of user selection
    sed -i "$drive_line s/.*/$drive_code $1/" loewner.F90
    
    # Compile and execute Loewner code
    gfortran loewner.F90 -o loewner.out
    ./loewner.out
    
    # Plot results with Python
    python plot.py "$2"
    
    echo "Completed execution for $1"
}

# Ask for user input
read_input

# Run for all driving functions in case of ALL
if [ "${drive_options[$drive_selection]}" == "ALL" ]; then

    all_drive
    exit
fi

# Run for driving function selection
run_loewner "${drive_options[$drive_selection]}" "$drive_selection"

