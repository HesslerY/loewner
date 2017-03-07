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
               "ALL")

# Array of different numbers of iterations for resolution mode
res_iterations=("100",
                "1000",
                "10000",
                "100000",
                "200000")

# Array of different values of max_t_incr for resolution mode
res_maxtimeinc=("0.01",
                "0.001",
                "0.0001",
                "0.00001",
                "0.000005")

# Array of different values of delta_t for resolution mode
res_deltatimei=("0.001",
                "0.0001",
                "0.00001",
                "0.000001",
                "0.0000005")

# Copy file just in case
cp loewner.F03 loewner_backup.F03

# Make an output directory if it does not already exist
# Delete all items in directory if it does exist
if [ ! -d "output" ]; then
    mkdir "output"
elif [ "$(ls output)" != "" ]; then
    rm -r output/*
fi

function all_drive()
{
    # Call run_loewner for all but last element in driving function array
    for (( i=0; i<$((${#drive_options[*]} - 1)); i++ )) do

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
    ./loewner.out "$n_g_0" "$max_t_change" "$delta_t"

    echo "Completed execution for ${drive_options[$drive_selection]}"
}

function resolution()
{
    # Iterate over kappa driving functions
    for (( i=10; i<=16; i++)) do
        
        # Set drive_selection variable and modify Loewner file
        drive_selection=i
        change_drive

        # Execute Loewner code for different values of M, delta_t, and max_t_incr
        for (( j=0; j<5; j++)) do

            n_g_0=${res_iterations[$j]}
            max_t_change=${res_maxtimeinc[$j]}
            delta_t=${res_deltatimei[$j]}

            run_loewner
            
            # Move the result file to a different folder
            mv result.txt "multiple/$j.txt"
            
        done

        # Plot the results
        cp multiple/* "backup/$i"
        python multiplot.py "$i"&
        rm -r multiple/*

    done    
}

echo "Vary Resolution? [Y/N]"
read resolution_mode

if [ "$resolution_mode" == "Y" ]; then
    resolution
    exit
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

# Run for all driving functions in case of ALL
if [ "${drive_options[$drive_selection]}" == "ALL" ]; then

    all_drive
    exit
fi

# Run for driving function selection
run_loewner
plot_single
