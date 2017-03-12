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
               "2 * sqrt(2.5 * (1 - t))"
               "2 * sqrt(3.5 * (1 - t))"
               "2 * sqrt(4 * (1 - t))"
               "2 * sqrt(4.5 * (1 - t))"
               "2 * sqrt(6 * (1 - t))"
               "2 * sqrt(8 * (1 - t))"
               "MULTIPLE"
               "ALL")

# Array of different numbers of iterations for resolution mode
declare -a res_iterations

declare -a selection_array

# Copy file just in case
cp loewner.F03 loewner_backup.F03

rm -r output/*

function all_drive()
{
    # Call run_loewner for all but last element in driving function array
    for (( i=0; i<$((${#drive_options[*]} - 2)); i++ )) do

        drive_selection=$i
        run_loewner
        plot_single

    done
}

function change_drive()
{
    # Change Loewner file in light of user selection
    sed -i "$drive_line s/.*/$drive_code ${drive_options[$drive_selection]}/" loewner.F03  
}

function plot_single()
{
    python plot.py "$drive_selection"
}

function run_loewner()
{
    # Change the driving function
    change_drive

    # Compile and execute Loewner code
    gfortran loewner.F03 -o loewner.out
    ./loewner.out "$max_t" "$n_iterations"

    echo "Completed execution for ${drive_options[$drive_selection]}"
}

function multiple_input()
{
    echo "Enter the driving function indexes seperated by a space:"
    read -a selection_array
}

function create_resolution_args()
{
    words=("first" "second" "third" "fourth" "fifth")

    echo "Enter the max time value:"
    read max_t

    for (( i=0; i<5; i++)) do

        echo "Enter the number of g_0 values for the ${words[$i]} iteration:"
        read n_iterations
        res_iterations+=("$n_iterations")

    done
}

function run_resolution()
{
    for selection in ${selection_array[@]}; do

        drive_selection=$selection
        change_drive

        # Execute Loewner code for different values of M, delta_t, and max_t_incr
        for (( i=0; i<5; i++)) do

            n_iterations=${res_iterations[$i]}

            run_loewner
            
            # Move the result file to a different folder
            mv result.txt "multiple/$i.txt"

        done

        # Plot the results
        cp multiple/* "backup/$drive_selection"
        python multiplot.py "$drive_selection"&
        rm -r multiple/*

    done
}

# Ask for drive function selection
echo "Select a driving function:"

# Display all driving function options
for (( i=0; i<${#drive_options[*]}; i++ )) do

    echo "[$i] ${drive_options[$i]}"

done

# Store user input as variable
read drive_selection

# Run for all driving functions in case of ALL
if [ "${drive_options[$drive_selection]}" == "ALL" ]; then
    all_drive
    exit
fi

selection_array+=($drive_selection)

if [ "${drive_options[$drive_selection]}" == "MULTIPLE" ]; then
    multiple_input
fi

# echo "${selection_array[@]}" 

echo "Vary Resolution? [Y/N]"
read resolution_mode

if [ "$resolution_mode" == "Y" ]; then
    create_resolution_args
    run_resolution
    exit
fi

# Ask for drive function selection
echo "Enter the final value of max_t:"

# Store user input as variable
read max_t

# Ask for the number of intervals
echo "Enter the number of g_0 values to be computed:"

# Store the user input as a variable
read n_iterations

# Run for driving function selection
run_loewner
plot_single
