!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!                                                                              !
! Program: NumericalLoewner.F90                                                !
! Purpose: Obtain numerical solutions for solving the quadratic and cubic form !
!          of Loewner's equation for a variety of driving functions.           !
! Author:  Dolica Akello-Egwel                                                 !
!                                                                              !
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

! Module for defining constants
module Constants
implicit none

   ! Define pi
   real(8), parameter :: PI = 4.*atan(1.)

   ! 'Empty' parameter used for setting constant driving value
   real(8) :: constantParam = 0.0

   ! 'Empty' parameter used for setting alpha/kappa
   real(8) :: sqrtParam = 0.0

   ! Define imaginary unit
   complex, parameter :: IMUNIT = complex(0,1)

end module Constants

! Function for finding the base^expn with a real base
function RealPower(base,expn)
implicit none

    ! Argument declarations
    real(8) :: base
    integer :: expn

    ! Return value declaration
    real(8) :: RealPower

    ! Find the square of x
    RealPower = base ** expn

end function RealPower

! Function for finding the base^expn with a complex base
function ComplexPower(base,expn)
implicit none

    ! Argument declarations
    complex(8) :: base
    integer :: expn

    ! Return value declaration
    complex(8) :: ComplexPower

    ! Find the square of x
    ComplexPower = base ** expn

end function ComplexPower

! Module for solving cubic functions
module CubicSolver
use Constants
implicit none

  ! Function for finding a cube root
  public :: CubicRoot

  ! Function for seeing if a complex number is close to zero
  public :: ComplexZero

  ! Tolerance for float comparisons
  real(8), parameter :: TOL = 1e-9

contains

! Function for evaluating f(z) = z^3 + a*z^2 + b*z + c
function f(z,a,b,c)
implicit none

    ! Argument declarations
    complex(8) :: z
    complex(8) :: a
    complex(8) :: b
    complex(8) :: c

    ! Return value declaration
    complex(8) :: f
    
    ! Function declaration
    complex(8) :: ComplexPower

    ! Find the value of the function at z
    f = ComplexPower(z,3) + a*ComplexPower(z,2) + b*z + c

end function f

! Function for evaluating derivative of f'(z)
function df(z,a,b)
implicit none

    ! Argument declarations
    complex(8) :: z
    complex(8) :: a
    complex(8) :: b

    ! Return value declaration
    complex(8) :: df

    ! Function declarations
    complex(8) :: ComplexPower

    ! Find the value of the derivative at z
    df = 3*ComplexPower(z,2) + 2*a*z + b

end function df

! Function for seeing if a real number is close to zero within a certain tolerance
function RealZero(x)
implicit none

    ! Argument declaration
    real(8) :: x

    ! Return value declaration
    logical :: RealZero

    ! Check if the absolute value of the number is beneath the tolerance
    if (abs(x) < TOL) then
        RealZero = .true.
    else
        RealZero = .false.
    endif

end function RealZero

! Function for seeing if a complex number is close to zero within a certain tolerance
function ComplexZero(z)
implicit none

    ! Argument declaration
    complex(8) :: z
    
    ! Return value declarations
    logical :: ComplexZero

    ! Check if the absolute values of both the real and imaginary components are beneath the tolerance
    if (abs(real(z)) < TOL .and. abs(imag(z)) < TOL) then
        ComplexZero = .true.
    else
        ComplexZero = .false.
    endif

end function ComplexZero

! Function for identifying the roots of a cubic function
function CubicRoot(PolynCoeffs)
implicit none

    ! Argument declaration
    complex(8), dimension(3) :: PolynCoeffs
    
    ! Local variable declarations
    integer :: i
    real(8) :: signCheck
    complex(8) :: a, b, c, Q, R, rootRQ, upperA, upperB, CubicRoot
    complex(8), dimension(3) :: PolynRoots

    ! Function declaration
    complex(8) :: ComplexPower

    ! Set initial value for root
    CubicRoot = 0

    ! Assign polynomial coefficients
    a = PolynCoeffs(1)
    b = PolynCoeffs(2)
    c = PolynCoeffs(3)

    Q = (a*a - 3*b)/9
    R = (2*ComplexPower(a,3) - 9*a*b + 27*c)/54.

    rootRQ = cdsqrt(ComplexPower(R,2) - ComplexPower(Q,3))

    signCheck = real(conjg(R)*rootRQ)

    if (RealZero(signCheck)) then
        upperA = -(R + rootRQ)**(1./3)
    else
        upperA = -(R - rootRQ)**(1./3)
    endif

    if (ComplexZero(upperA)) then
        upperB = 0
    else
        upperB = Q/upperA
    endif

    ! Assign the roots
    PolynRoots(1) = (upperA + upperB) - (a/3)
    PolynRoots(2) = -0.5*(upperA + upperB) - (a/3) + IMUNIT*sqrt(3.0)*0.5*(upperA - upperB)
    PolynRoots(3) = -0.5*(upperA + upperB) - (a/3) - IMUNIT*sqrt(3.0)*0.5*(upperA - upperB)

    ! Iterate until the root with the largest imaginary part is found
    do i = 1, 3
        if (imag(PolynRoots(i)) > imag(CubicRoot)) then
            CubicRoot = PolynRoots(i)
        endif
    enddo

    ! Use Newton's method to enhance accuracy of solution
    CubicRoot = NewtonRoot(CubicRoot,a,b,c)

#if TESTCUBIC == 1
    print *, "Returning ", CubicRoot
    print *, "f(z) = ", f(CubicRoot,a,b,c)
#endif

end function CubicRoot

! Perform Newton's method to refine the accuracy of the cubic root
function NewtonRoot(z,a,b,c)
implicit none

    ! Argument declaration
    complex(8) :: z
    complex(8) :: a
    complex(8) :: b
    complex(8) :: c

    ! Return value declaration
    complex(8) :: NewtonRoot

    ! Carry out Newton's method until desired tolerance is achieved
    do while (.not. ComplexZero(f(z,a,b,c)))
        z = z - f(z,a,b,c)/df(z,a,b)
    end do

    ! Return more accurate root
    NewtonRoot = z

end function NewtonRoot
end module CubicSolver

! Find the value of a particular driving function at time t
function DrivingFunction(t)
use Constants
implicit none

    ! Argument declaration
    real(8) :: t

    ! Return value declaration
    real(8) :: DrivingFunction

#if CASE == 0
    DrivingFunction = constantParam

#elif CASE == 1
    DrivingFunction = t

#elif CASE == 2
    DrivingFunction = cos(t)

#elif CASE == 3
    DrivingFunction = t * cos(t)

#elif CASE == 4
    DrivingFunction = cos(t * PI)

#elif CASE == 5
    DrivingFunction = t * cos(t * PI)

#elif CASE == 6
    DrivingFunction = sin(t)

#elif CASE == 7
    DrivingFunction = t * sin(t)

#elif CASE == 8
    DrivingFunction = sin(t * PI)

#elif CASE == 9
    DrivingFunction = t * sin(t * PI)

#elif CASE == 10
    DrivingFunction = 2 * dsqrt(sqrtParam * (1 - t))

#elif CASE == 11
    DrivingFunction = dsqrt(t) * sqrtParam

#elif CASE == 12
    DrivingFunction = floor(t)

#elif CASE == 13
    DrivingFunction = mod(floor(t), 2)

#elif CASE == 14
    DrivingFunction = dsqrt(1 + t)

#else
    stop "Error: Driving function not recognised."

#endif

end function DrivingFunction

! Find the value for the c_alpha parameter
function ComputeCAlpha(alpha)
implicit none

    ! Argument declaration
    real(8) :: alpha

    ! Return value declaration
    real(8) :: ComputeCAlpha

    ! Function declaration
    real(8) :: RealPower

    ComputeCAlpha = (2 - 4 * alpha) / dsqrt(alpha - RealPower(alpha,2))

end function ComputeCAlpha

! Generate an array of numPoints time values between a user-defined starting point and end point
subroutine Linspace(timeRange,startPoint,endPoint,numPoints)
implicit none

    ! Argument declaration
    integer :: numPoints
    real(8) :: startPoint
    real(8) :: endPoint
    real(8), dimension(numPoints) :: timeRange

    ! Local variable declaration
    real(8) :: delta

    ! Compute the value of delta
#if CASE == 10
    ! Make the time range stop short of one for the kappa driving function
    delta  = (endPoint - startPoint)/numPoints
#else
    delta  = (endPoint - startPoint)/(numPoints - 1)
#endif

    ! Create an array that starts at zero and ends at delta*(numPoints - 1) 
    timeRange = (/((i * delta), i = 0, numPoints - 1)/)

    ! Add the starting point to all values in the array
    timeRange = timeRange(:) + startPoint

end subroutine Linspace

! Solve Loewner's equation in the quadratic case
subroutine QuadraticLoewner(outerStartTime, outerFinalTime, outerN, innerN, gResult, sqrtDrivingArg, constantDrivingArg)
use Constants
implicit none

    ! Argument declarations

    integer :: outerN
    integer :: innerN

    real(8) :: outerStartTime
    real(8) :: outerFinalTime

    real(8), optional :: sqrtDrivingArg
    real(8), optional :: constantDrivingArg

    complex(8) :: gResult(outerN)

    ! Local variable declarations

    integer :: totalN
    integer :: i = 0
    integer :: j = 0

    real(8) :: twoInnerDeltaTime = 0
    real(8) :: drivingValue = 0

    real(8), dimension(:), allocatable :: timeRange

    complex(8) :: gCurrent = 0
    complex(8) :: bTerm = 0
    complex(8) :: cTerm = 0

    ! Function declarations

    real(8) :: ComputeCAlpha
    real(8) :: DrivingFunction
    complex(8) :: ComplexPower

    ! Define kappa or c_alpha in the case of square-root driving
    if (present(sqrtDrivingArg)) then
#if CASE == 10
        sqrtParam  = sqrtDrivingArg
#elif CASE == 11
        sqrtParam = ComputeCAlpha(sqrtDrivingArg)
#endif
    endif

    ! Define the constant-value in the case of constant driving
    if (present(constantDrivingArg)) then
        constantParam  = constantDrivingArg
    endif

    ! Find the total number of points in the time interval
    totalN = innerN * (outerN - 1)

    ! Initialise the time-value array
    Allocate(timeRange(1:totalN))

    ! Use Linspace to obtain the time-value array
    call Linspace(timeRange,outerStartTime,outerFinalTime,totalN)

    ! Determine two * delta
    twoInnerDeltaTime = timeRange(2) * 2

    ! Set the first element to be the driving function at t = 0
    gResult(1) = complex(DrivingFunction(timeRange(1)),0)

    ! Compute g_0 outerN - 1 times
    do i = 1, outerN - 1

        ! Find the value of g at t = inner max time
        gCurrent = complex(DrivingFunction(timeRange(i*innerN)),0)

        ! Iterate backwards from the highest time value to zero
        do j = i*innerN,1,-1

            ! Obtain the current driving value
            drivingValue = DrivingFunction(timeRange(j))

            ! Solve Loewner's equation for the previous time value
            bTerm = (drivingValue + gCurrent) * 0.5
            cTerm = (drivingValue * gCurrent) + twoInnerDeltaTime
            gCurrent = bTerm + cdsqrt(cTerm - ComplexPower(bTerm,2)) * IMUNIT

        end do

        ! Place the g_0 value in the array
        gResult(i + 1) = gCurrent

    end do

end subroutine QuadraticLoewner

! Solve Loewner's equation in the cubic case
subroutine CubicLoewner(outerStartTime, outerFinalTime, outerN, innerN, first_g_arr, secnd_g_arr, sqrtDrivingArg,constDrivingArg)
use Constants
use CubicSolver
implicit none

    ! Argument declarations

    integer :: outerN
    integer :: innerN

    real(8) :: outerStartTime
    real(8) :: outerFinalTime

    real(8), optional :: sqrtDrivingArg
    real(8), optional :: constDrivingArg

    complex(8) :: first_g_arr(outerN)
    complex(8) :: secnd_g_arr(outerN)

    ! Local variable declarations

    integer :: totalN
    integer :: i = 0
    integer :: j = 0

    real(8) :: twoInnerDeltaTime = 0
    real(8) :: drivingValue = 0

    real(8), dimension(:), allocatable :: timeRange

    complex(8) :: c = 0
    complex(8) :: first_g_t1 = 0
    complex(8) :: first_g_t2 = 0
    complex(8) :: secnd_g_t1 = 0
    complex(8) :: secnd_g_t2 = 0

    complex(8), dimension(3) :: first_polym_coeffs
    complex(8), dimension(3) :: secnd_polym_coeffs

    ! Function declarations

    real(8) :: ComputeCAlpha
    real(8) :: DrivingFunction
    real(8) :: RealPower
    complex(8) :: ComplexPower

    ! Define kappa or calpha in the case of square-root driving
    if (present(sqrtDrivingArg)) then
#if CASE == 10
        sqrtParam  = sqrtDrivingArg
#elif CASE == 11
        sqrtParam = ComputeCAlpha(sqrtDrivingArg)
#endif
    endif

    ! Define the constant-value in the case of constant driving
    if (present(constDrivingArg)) then
        constantParam  = constDrivingArg
    endif

    ! Find the total number of points in the time interval
    totalN = innerN * (outerN - 1)

    ! Initialise the time-value array
    Allocate(timeRange(1:totalN))

    ! Use linspace to obtain the time-value array
    call Linspace(timeRange,outerStartTime,outerFinalTime,totalN)

    ! Determine two * delta
    twoInnerDeltaTime = timeRange(2) * 2

    ! Set the first elements to be +/-ve value of driving function at t = 0
    first_g_arr(1) = complex(DrivingFunction(timeRange(1)),0)
    secnd_g_arr(1) = -first_g_arr(1)

    ! Compute g_0 outerN times
    do i = 1, outerN - 1

        ! Find the value of g at t = inner max time
        first_g_t1 = complex(DrivingFunction(timeRange(i*innerN)),0)
        secnd_g_t1 = -first_g_t1

        ! Iterate backwards from the highest time value to zero
        do j = i*innerN,1,-1

            ! Obtain the current driving value
            drivingValue = DrivingFunction(timeRange(j))

            ! Obtain the value of the second coefficient
            c = twoInnerDeltaTime - RealPower(drivingValue,2)

            ! Define the coefficients of the cubic equation for the first trace
            first_polym_coeffs(1) = -first_g_t1
            first_polym_coeffs(2) = c
            first_polym_coeffs(3) = first_g_t1 * RealPower(drivingValue,2)

            ! Define the coefficients of the cubic equation for the second trace
            secnd_polym_coeffs(1) = -secnd_g_t1
            secnd_polym_coeffs(2) = c
            secnd_polym_coeffs(3) = secnd_g_t1 * RealPower(drivingValue,2)

            ! Use the Cubic Solver to find the cube roots for both traces
            first_g_t1 = CubicRoot(first_polym_coeffs)
            secnd_g_t1 = CubicRoot(secnd_polym_coeffs)

        end do

        ! Place the g_0 values in the arrays
        first_g_arr(i + 1) = first_g_t1
        secnd_g_arr(i + 1) = secnd_g_t1

    end do

end subroutine CubicLoewner

! Empty program to aid with identifying compilation errors should f2py fail
program test
end program test

