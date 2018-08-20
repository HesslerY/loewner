# Single and Two-Trace Loewner Evolutions

<p align="center">
  <img src="https://github.com/ucapdak/loewner/blob/master/example.png" 
  width="500" alt="Forward Single Trace Output - xi(t) = t * cos(t * pi)"/>
</p>

## Setup

### Prerequisites

#### Essential
* Matlab R2017b or later 
* Python3 

#### Python Libraries
* f2py - Required for using Fortran programs (forward/inverse single-trace and two-trace) within interface.
* Matlab Engine for Python - Required for using Wedge program within interface.
* numpy - Essential for handling complex arrays.
* mpmath - Required for computing exact solutions.
* cmath - Required for computing exact solutions.
* prompt_toolkit - Required for using CLI interface.
* importlib - Essential for loading Fortran modules.
* matplotlib - Required for saving plots.

#### Matlab Toolboxes
* Parallel Computing Toolbox - Reccomended for using Wedge program.
* Optimization Toolbox - Essential for using Wedge program.

### Installing

SSH:
```
git clone git@github.com:ucapdak/loewner.git
```

HTTPS:
```
git clone https://github.com/ucapdak/loewner.git
```

## Usage Instructions

### Using the Command-Line-Interface

From the main directory enter ``python Start.py`` to launch the CLI. This will initialise the "main" menu. From here you can enter the following commands:

* `` forsin `` - Start forward single-trace mode
* `` invsin `` - Start inverse single-trace mode
* `` two `` - Start two-trace mode
* `` wedge `` - Start wedge trace mode
* `` exact `` - Exact forward or single-trace mode
* ``exactinv`` - Start exact inverse solution mode.

Other Important Commands:

* `` df `` - Print a list of driving functions
* `` q `` or  `` quit `` - Exit the program
* `` h `` or  `` help `` - Display a help message
* `` b `` or  `` back `` - Return to the main menu

### Driving Function Indices

To run the program in for the various driving functions you have to use the following index system:

| Index  | Driving Function                                                          | Extra Arguments?   | Frd. Single    | Inv. Single (and Exact Inverse) | Frd. Two-Trace | Wedge           | Exact Solution  |
| ------ |:--------------------------------------------------------------------------| :------------------|:--------------:|:-------------------------------:|:--------------:|:---------------:|:----------------|
| 0      | ![](https://github.com/ucapdak/loewner/blob/master/readmeimages/00df.png) | C                  | Yes            | Yes                             | Yes            | Yes (C = 1)     | Two-Trace (C=1) |
| 1      | ![](https://github.com/ucapdak/loewner/blob/master/readmeimages/01df.png) | None               | Yes            | Yes                             | Yes            | No              | Single-Trace    |
| 2      | ![](https://github.com/ucapdak/loewner/blob/master/readmeimages/02df.png) | None               | Yes            | Yes                             | Yes            | No              | None            |
| 3      | ![](https://github.com/ucapdak/loewner/blob/master/readmeimages/03df.png) | None               | Yes            | Yes                             | Yes            | No              | None            |
| 4      | ![](https://github.com/ucapdak/loewner/blob/master/readmeimages/04df.png) | None               | Yes            | Yes                             | Yes            | No              | None            |
| 5      | ![](https://github.com/ucapdak/loewner/blob/master/readmeimages/05df.png) | None               | Yes            | Yes                             | Yes            | No              | None            |
| 6      | ![](https://github.com/ucapdak/loewner/blob/master/readmeimages/06df.png) | None               | Yes            | Yes                             | Yes            | No              | None            |
| 7      | ![](https://github.com/ucapdak/loewner/blob/master/readmeimages/07df.png) | None               | Yes            | Yes                             | Yes            | No              | None            |
| 8      | ![](https://github.com/ucapdak/loewner/blob/master/readmeimages/08df.png) | None               | Yes            | Yes                             | Yes            | No              | None            |
| 9      | ![](https://github.com/ucapdak/loewner/blob/master/readmeimages/09df.png) | None               | Yes            | Yes                             | Yes            | No              | None            |
| 10     | ![](https://github.com/ucapdak/loewner/blob/master/readmeimages/10df.png) | Kappa              | Yes            | Yes                             | Yes            | No              | None            |
| 11     | ![](https://github.com/ucapdak/loewner/blob/master/readmeimages/11df.png) | Alpha              | Yes            | Yes                             | Yes            | No              | None            |
| 12     | ![](https://github.com/ucapdak/loewner/blob/master/readmeimages/12df.png) | None               | Yes            | Yes                             | Yes            | No              | None            |
| 13     | ![](https://github.com/ucapdak/loewner/blob/master/readmeimages/13df.png) | None               | Yes            | Yes                             | Yes            | No              | None            |
| 14     | ![](https://github.com/ucapdak/loewner/blob/master/readmeimages/14df.png) | None               | Yes            | Yes                             | Yes            | Yes             | Two-Trace       |

### Compilation

Using much of the program within the CLI requires compiling certain files as Python modules.

For most driving functions, using the forward and two-trace modes requires compiling at least once for *each* of the different driving functions. If this isn't done then the program will fail. For subsequent runs, you won't have to recompile the modules so long as  ``ForwardLoewner.F90`` isn't changed.

For the kappa, calpha, and constant driving functions you have to recompile the module every time these values are changed.

### Preparing One or More Runs

After selecting a mode you have to set certain parameters for the driving functions you wish to run. This is done by entering `` [parameter] [value] `` in the CLI.

* `` starttime `` - Start time for the runs. Must be greater than zero.
* `` finaltime `` - Final time for the runs. Must be greater than the start time.
* `` outerres `` - Outer resolution. Must be greater than zero.
* `` innerres `` - Inner resolution. Must be greater than zero.
* `` compile `` - Whether or not to compile modules. Typically only has to be done on the first execution of the program, or not at all, depending on the algorithm. See [more](https://github.com/ucapdak/loewner#compilation).
* `` savedata `` - Save the output as .dat files. These are seperated by a space.
* `` saveplots `` - Save the output as .pdf plots.

e.g. ``Loewner >> starttime 0 `` to use a start time of zero. For compilation and saving data your response must be given in the form of `` y `` or `` n ``, e.g. `` Loewner >>saveplots y ``. In the case of kappa-driving any final time greater than 1 will be automatically changed to 1.

Alternative arguments:  
  
* `` times [start time] [final time] `` - Quicker way for entering times values.
* `` res [outer res] [inner res] `` - Quicker way for enterting resolution values.

Extra parameters:  
  
* `` wedgealpha `` - Only required for wedge mode.
* `` constant `` - Only required if you intend to run constant-driving.
* `` kappa `` - Only required if you intend to run kappa-driving.
* `` drivealpha `` - Only required if you intend to run c-alpha-driving.

Additional commands:  
* `` run `` - Enter the list of driving functions you wish to use for a certain algorithm in the form ``run INDEX1 INDEX2``
* `` start `` Executes the algotihm once parameters and driving functions have been chosen.
* `` cleardriving `` - Clear the driving function selection and start over.  
* `` printdriving `` - Print the current driving function selection.  
* `` error `` - Displays information on why enterting ``start`` failed and algorithm could not be performed. This will be caused when parameters haven't been set or have bad values.
  
### Forward/Inverse Single-Trace + Forward Two-Trace Runs - `` forsin``/``invsin``/``two`` Mode

This mode allows you to run one or more driving functions with the option to save and/or plot the results. This can only run constant, kappa, and c-alpha runs once.

1. Enter `` forsin ``/`` invsin ``/``two`` from the main menu
2. Enter the run-parameters.
3. Enter ``run`` with a list of driving functions you wish to use seperated by a space.
4. Enter `` start ``.
5. If the parameters are successfully validated, then the program will execute these runs and save the output. 
  
Upon completion, the forward single-trace results will be saved to:  
  
Data:  
```
[LOEWNER DIRECTORY]/main/Output/Data/SingleTrace/Forward/  
```
Plots:
```
[LOEWNER DIRECTORY]/main/Output/Plots/SingleTrace/Forward/  

```
  
The numerical inverse single-trace results will be saved to:  
  
Data:  
```
[LOEWNER DIRECTORY]/main/Output/Data/SingleTrace/Inverse/  
```
Plots:
```
[LOEWNER DIRECTORY]/main/Output/Plots/SingleTrace/Inverse/  
```

The two-trace results will be saved to:  
  
Data:  
```
[LOEWNER DIRECTORY]/main/Output/Data/TwoTrace/Forward/  
```
Plots:
```
[LOEWNER DIRECTORY]/main/Output/Plots/TwoTrace/Forward/  
```
  
### Exact Inverse Runs - `` exactinv `` Mode
  
This mode allows you to run one or more driving functions with the option to save and/or plot the results. This can only run constant, kappa, and c-alpha runs once.  
  
1. Enter `` exactinv `` from the main menu
2. Enter the run-parameters. The only resolution argument required is ``outerres``. There is no need to set the ``compile`` value as this isn't required for the exact inverse procedure.
3. Enter ``run`` followed by a list of driving functions you wish to use seperated by a space.
4. Enter `` start `` to carry out the algorithm.
5. If the parameters are successfully validated, then the program will execute these runs and save the output. 
  
Upon completion, the results will be saved to:  
  
Data:  
```
[LOEWNER DIRECTORY]/main/Output/Data/ExactInverse/  
```
Plots:
```
[LOEWNER DIRECTORY]/main/Output/Plots/ExactInverse/  
```
### Wedge Runs - `` wedge `` Mode
  
This mode allows you to run one or more driving functions with the option to save and/or plot the results. This can only run constant, kappa, and c-alpha runs once.  
  
1. Enter `` wedge `` from the main menu
2. Enter the run-parameters. Also enter a ``wedgealpha`` argument in the form of radians.
3. Enter ``run`` followed by a list of driving functions you wish to use seperated by a space, e.g. ``Loewner >> run INDEX1 INDEX2 INDEX3 ``. This can allow 'standard' driving functions more than once, but cannot be used to run the driving functions that require extra arguments more than once.
4. Enter `` start `` to carry out the algorithm.
5. If the parameters are successfully validated, then the program will execute these runs and save the output. 
  
Upon completion, the results will be saved to:  
  
Data:  
```
[LOEWNER DIRECTORY]/main/Output/Data/WedgeGrowth/Forward/  
```
Plots:
```
[LOEWNER DIRECTORY]/main/Output/Plots/WedgeGrowth/Forward/  
```
### Exact Single or Two-Trace Forward Runs - `` exact `` Mode
  
This mode allows you to run exact forward solutions for constant, linear, and xi(t) = sqrt(1 + t) driving functions. For linear drviving there is the option to use two different equations.

1. Enter `` exact `` from the main menu

#### Exact Solution - Constant Driving - Two Trace Evolution
  
2. Enter the run-parameters: start time, final time, outer resolution, save plots, save data. The constant parmater is automatically set to 1.
3. Enter ``run 0`` 
4. Enter `` start `` to carry out the algorithm.
5. If the parameters are successfully validated, then the program will execute these runs and save the output. 
  
Upon completion, the results will be saved to:  
  
Data:  
```
[LOEWNER DIRECTORY]/main/Output/Data/TwoTrace/ExactSolutions/  
```
Plots:
```
[LOEWNER DIRECTORY]/main/Output/Plots/TwoTrace/ExactSolutions/  
```
#### Exact Solution - Linear Driving - Single-Trace Evolution - Explicit 

For linear driving there is the optoo
  
2. Enter the run-parameters: outer resolution, save plots, save data. 
3. Set the paramters ``startphi`` and ``finalphi``. These must be greater than zero. Any final value greater than pi will be automatically be set to pi.
4. Set ``linearexplicit`` to True.
5. Set ``linearimplicit`` to False. (if not desired)
6. Enter ``run 1`` 
7. Enter `` start `` to carry out the algorithm.
8. If the parameters are successfully validated, then the program will execute these runs and save the output. 
  
Upon completion, the results will be saved to:  
  
Data:  
```
[LOEWNER DIRECTORY]/main/Output/Data/SingleTrace/ExactForward/  
```
Plots:
```
[LOEWNER DIRECTORY]/main/Output/Plots/SingleTrace/ExactForward/  
```
#### Exact Solution - Linear Driving - Single-Trace Evolution - Implicit
  
2. Enter the run-parameters: start time, final time, outer resolution, save plots, save data. 
4. Set ``linearexplicit`` to False (if not desired).
5. Set ``linearimplicit`` to True. 
6. Enter ``run 1`` 
7. Enter `` start `` to carry out the algorithm.
8. If the parameters are successfully validated, then the program will execute these runs and save the output. 
  
Upon completion, the results will be saved to:  
  
Data:  
```
[LOEWNER DIRECTORY]/main/Output/Data/SingleTrace/ExactForward/  
```
Plots:
```
[LOEWNER DIRECTORY]/main/Output/Plots/SingleTrace/ExactForward/  
```
#### Exact Solution - xi(t) = sqrt(1 + t) Drving - Two-Trace Evolution
  
2. Enter the run-parameters: start time, final time, outer resolution, save plots, save data. 
6. Enter ``run 14`` 
7. Enter `` start `` to carry out the algorithm.
8. If the parameters are successfully validated, then the program will execute these runs and save the output. 
  
Upon completion, the results will be saved to:  
  
Data:  
```
[LOEWNER DIRECTORY]/main/Output/Data/TwoTrace/ExactSolutions/  
```
Plots:
```
[LOEWNER DIRECTORY]/main/Output/Plots/TwoTrace/ExactSolutions/  
```
### Multipe Kappa Runs - `` kappa `` Mode
  
This mode allows you to run multiple kappa-driving forward single-trace evolutions for a range of driving functions.

1. Enter `` kappa `` from the main menu
2. Enter the run-parameters: start time, final time, outer resolution, inner resolution, save plots, save data. Final time will be set to set to 1 if you enter a value larger than 1. Compile is automatically set to true.
3. Enter kappas in the form of ``kappas [start kappa] [final kappa] step [step value]`` or ``kappas [start kappa] [final kappa] num [number of kappa runs]``
4. Enter `` start `` to carry out the algorithm.
5. If the parameters are successfully validated, then the program will execute these runs and save the output. 
  
Upon completion, the results will be saved to:  
  
Data:  
```
[LOEWNER DIRECTORY]/main/Output/Data/SingleTrace/Forward/  
[LOEWNER DIRECTORY]/main/Output/Data/SingleTrace/TranslatedForward/  
```
Plots:
```
[LOEWNER DIRECTORY]/main/Output/Plots/SingleTrace/Forward/  
[LOEWNER DIRECTORY]/main/Output/Plots/SingleTrace/TranslatedForward/  
```
### Output Formats

Plots are saved as PDFs, data is saved in DAT files. The DAT files have 18 decimal places of precision and the columns are seperated by a space. The time/kappa/wegde angle/alpha parameters are represented in the filename with 5 decimal places of precision, so there is a risk of ovewritting results for near-identical results where certain parameters are rounded to the same value.

#### Numerical Single-Trace Forward and Inverse + Two-Trace Forward Results

For numerical single-trace forward and inverse, the output filename will take the form:  
  
``[INDEX]-[START TIME]-[FINAL TIME]-[OUTER RESOLUTION]-[INNER RESOLUTION].EXT`` where ``.EXT`` is either .dat or .pdf depending on the output type.  
  
For kappa and c-alpha the files are saved in the format:  
  
``[INDEX]-[KAPPA OR ALPHA VALUE]-[START TIME]-[FINAL TIME]-[OUTER RESOLUTION]-[INNER RESOLUTION].EXT``  
  
#### Wedge Results

For the wedge algorithm, the output filename will take the form:  
  
``[INDEX]-[WEDGE ANGLE]-[FINAL TIME]-[OUTER RESOLUTION]-[INNER RESOLUTION].EXT``

#### Exact Solution - Linear Driving - Single-Trace Evolution - Explicit Results

For the explicit linear exact solution, the output filename will take the form:  
  
``[INDEX]-PHI-[START PHI]-[FINAL PHI]-[OUTER RESOLUTION].EXT``

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

