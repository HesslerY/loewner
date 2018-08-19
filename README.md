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

### Usage Instructions

#### Using the Command-Line-Interface

From the main directory enter ``python Start.py`` to launch the CLI. This will initialise the "main" menu. From here you can enter the following commands:

* `` forsin `` - Start forward single-trace mode
* `` invsin `` - Start inverse single-trace mode
* `` invsin `` - Start two-trace mode
* `` wedge `` - Start wedge trace mode

##### Driving Function Indices

To run the program in for the various driving functions you have to use the following index system:

| Index        | Driving Function  | Extra Arguments?  |
| ------------- |:-------------:| -----:|
| 0      | ![](https://github.com/ucapdak/loewner/blob/master/readmeimages/01df.png) | The constant value: 1, 0, etc |
| 1      | centered      |   $12 |
| 2 | are neat      |    $1 |


##### Compilation

Using much of the program within the CLI requires compiling certain files as Python modules.

For most driving functions, using the forward and two-trace modes requires compiling at least once for *each* of the different driving functions. If this isn't done then the program will fail. For subsequent runs, you won't have to recompile the modules so long as  ``ForwardLoewner.F90`` isn't changed.

For the kappa, calpha, and constant driving functions you have to recompile the module every time these values are changed.

##### Compilation

##### Forward Single-Trace Runs

This mode allows you to run one or more driving functions with the option to save and/or plot the results.



## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

