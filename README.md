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

| Index  | Driving Function                                                          | Extra Arguments?   | Frd. Single    | Inv. Single (and Exact Inverse) | Frd. Two-Trace | Wedge           | Exact Solution  |
| ------ |:--------------------------------------------------------------------------| :------------------|:--------------:|:-------------------------------:|:--------------:|:---------------:|:----------------|
| 0      | ![](https://github.com/ucapdak/loewner/blob/master/readmeimages/00df.png) | C                  | Yes            | Yes                             | Yes            | Yes (for C = 1) | Two-Trace       |
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



| Index | Forward Single  | Inverse Single | Forward Cubic | Wedge  |
|-------|:---------------:|:--------------:|:-------------:|:------:|
| 0     |                 |                |               |        |

##### Compilation

Using much of the program within the CLI requires compiling certain files as Python modules.

For most driving functions, using the forward and two-trace modes requires compiling at least once for *each* of the different driving functions. If this isn't done then the program will fail. For subsequent runs, you won't have to recompile the modules so long as  ``ForwardLoewner.F90`` isn't changed.

For the kappa, calpha, and constant driving functions you have to recompile the module every time these values are changed.

##### Compilation

##### Forward Single-Trace Runs

This mode allows you to run one or more driving functions with the option to save and/or plot the results.



## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

