#!/bin/bash

# Line where drive_func assignment takes place in loewner.F03 file
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


# Ask for drive function selection
echo "Select a driving function:"

# Display all driving function options
for (( i=0; i<${#drive_options[*]}; i++ )) do

    echo "[$i] ${drive_options[$i]}"

done

# Store user input as variable
read drive_selection

# Ask for drive function selection
echo "Enter number of g_0 values:"

# Store user input as variable
read n_g_0

# Ask for the number of intervals
echo "Enter the change in max_t:"

# Store the user input as a variable
read max_t_change

# Ask for the number of intervals
echo "Enter delta_t:"

# Store the user input as a variable
read delta_t


function all_drive()
{
    # Call run_loewner for all but last element in driving function array
    for (( i=0; i<$((${#drive_options[*]} - 1)); i++ )) do

        drive_selection=$i
        run_loewner

    done
}

function run_loewner()
{
    # Change file in light of user selection
    sed -i "$drive_line s/.*/$drive_code ${drive_options[$drive_selection]}/" loewner.F03

    # Compile and execute Loewner code
    gfortran loewner.F03 -o loewner.out
    ./loewner.out "$n_g_0" "$max_t_change" "$delta_t"

    # Plot results with Python
    python plot.py "$drive_selection"

    rm -r result.txt

    echo "Completed execution for ${drive_options[$drive_selection]}"

}

# Run for all driving functions in case of ALL
if [ "${drive_options[$drive_selection]}" == "ALL" ]; then

    all_drive
    exit
fi

# Run for driving function selection
run_loewner
