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
echo "Enter the max time:"

# Store user input as variable
read max_time

# Ask for the number of intervals
echo "Enter the number of intervals:"

# Store the user input as a variable
read n_intervals


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
    ./loewner.out "$max_time" "$n_intervals"

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

echo "Enter a comment:"
read comment

echo "Max Time: $max_time" >> Parameters.txt
echo "Intervals: $n_intervals" >> Parameters.txt
echo "Comment: $comment" >> Parameters.txt
