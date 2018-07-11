!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!                                                                              !
! Program: NumericalLoewner.F90                                                !
! Purpose: Obtain numerical solutions for Loewner's equation with a variety    !
!          of driving functions.                                               !
! Author:  Dolica Akello-Egwel                                                 !
!                                                                              !
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

! Empty program to aid with identifying compilation errors should f2py fail
program test
end program test

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

    complex(8) :: f
    complex(8) :: z
    complex(8) :: a
    complex(8) :: b
    complex(8) :: c

    ! Find the value of the function at z
    f = z**3 + a*z**2 + b*z + c

end function f

! Function for evaluating derivative of f'(z)
function df(z,a,b)
implicit none

    complex(8) :: df
    complex(8) :: z
    complex(8) :: a
    complex(8) :: b

    ! Find the value of the derivative at z
    df = 3*z**2 + 2*a*z + b

end function df

! Function for seeing if a real number is close to zero within a certain tolerance
function RealZero(x)
implicit none

    logical :: RealZero
    real(8) :: x

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

    logical :: ComplexZero
    complex(8) :: z

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

    complex(8), dimension(3) :: PolynCoeffs, PolynRoots
    complex(8) :: a, b, c, Q, R, rootRQ, upperA, upperB, CubicRoot
    real(8) :: signCheck
    integer :: i

    ! Set initial value for root
    CubicRoot = 0

    ! Assign polynomial coefficients
    a = PolynCoeffs(1)
    b = PolynCoeffs(2)
    c = PolynCoeffs(3)

    Q = (a*a - 3*b)/9
    R = (2*a**3 - 9*a*b + 27*c)/54.

    rootRQ = cdsqrt(R**2 - Q**3)

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

    ! Use Newton's Iteration to enhance accuracy of solution
    CubicRoot = NewtonRoot(CubicRoot,a,b,c)

#if TESTCUBIC == 1
    print *, "Returning ", CubicRoot
    print *, "f(z) = ", f(CubicRoot,a,b,c)
#endif

! Perform Newton's Iteration to refine the accuracy of the cubic root
end function CubicRoot
function NewtonRoot(z,a,b,c)
implicit none

    ! Argument decleration
    complex(8) :: z
    complex(8) :: a
    complex(8) :: b
    complex(8) :: c

    ! Return value decleration
    complex(8) :: NewtonRoot

    ! Carry out Newton's Iteration until tolerance is achieved
    do while (.not. ComplexZero(f(z,a,b,c)))
        z = z - f(z,a,b,c)/df(z,a,b)
    end do

    ! Return more accurate root
    NewtonRoot = z

end function NewtonRoot
end module CubicSolver

! Function for finding the square of a complex value
function Square(x)

    ! Argument decleration
    complex(8) :: x

    ! Return value decleration
    complex(8) :: Square

    ! Find the square of x
    Square = x ** 2

end function Square

! Find the value of a particular driving function at time t
function DrivingFunction(t)
use Constants

    ! Argument decleration
    real(8), intent(in) :: t

    ! Return value decleration
    real(8) :: DrivingFunction

#if CASE == 0
    DrivingFunction = 1.0

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

subroutine LoewnersEquation(outerStartTime, outerFinalTime, outerN, innerN, g_arr, sqrt_driving)
use Constants
implicit none

    ! Argument declarations
    real(8) :: outerStartTime
    real(8) :: outerFinalTime
    integer :: outerN
    integer :: innerN
    complex(8) :: g_arr(outerN)
    real(8), optional :: sqrt_driving

    ! Local variable declarations
    integer :: j = 0
    integer :: k = 0

    real(8) :: innerDeltaTime = 0
    real(8) :: twoInnerDeltaTime = 0
    real(8) :: max_t = 0
    real(8) :: max_t_incr = 0
    real(8) :: driving_value = 0
    real(8) :: total_change = 0
    real(8) :: driving_arg = 0

    complex(8) :: g_t1 = 0
    complex(8) :: g_t2 = 0
    complex(8) :: b_term = 0
    complex(8) :: c_term = 0

    ! Function declarations
    complex(8) :: Square
    real(8) :: DrivingFunction

    if (present(sqrt_driving)) then
#if CASE == 10
        sqrtParam  = sqrt_driving
#elif CASE == 11
        sqrtParam = (2 - 4 * sqrt_driving) / cdsqrt(sqrt_driving - Square(sqrt_driving))
#endif
    endif

    ! Find the difference between start time and final time
    total_change = outerFinalTime - outerStartTime

#if CASE == 10
    ! Find the value by which max_t is incremented after each iteration
    max_t_incr = total_change / (outerN)
#else
    max_t_incr = total_change / (outerN - 1)
#endif

    ! Determine the delta values
    innerDeltaTime = max_t_incr /  innerN
    twoInnerDeltaTime = innerDeltaTime * 2

    ! Compute g_0 outerN times
    do j = 1, outerN

        ! Set max_t
        max_t = outerStartTime + ((j - 1) * max_t_incr)

        ! Find the initial value for g_1
        g_t1 = complex(DrivingFunction(max_t),0)

        ! Reset the counter for the inner loop
        k = 0

        ! Determine the initial value for the driving function argument
        driving_arg = max_t

        do while (driving_arg > 0)

            ! Obtain the driving value
            driving_value = DrivingFunction(driving_arg)

            ! Solve Loewner's equation
            b_term = (driving_value + g_t1) * 0.5
            c_term = (driving_value * g_t1) + twoInnerDeltaTime
            g_t2 = b_term + cdsqrt(c_term - Square(b_term)) * IMUNIT

            ! S
            g_t1 = g_t2

            k = k + 1
            driving_arg = (max_t - (k * innerDeltaTime)) - innerDeltaTime

        end do

        ! Place the latest value in the array
        g_arr(j) = g_t1

    end do

end subroutine LoewnersEquation

subroutine cubic_loewner(outerStartTime, outerFinalTime, outerN, innerN, first_g_arr, secnd_g_arr, sqrt_driving)
use constants
use cubicsolver
implicit none

    ! Argument declarations
    real(8) :: outerStartTime
    real(8) :: outerFinalTime
    integer :: outerN
    integer :: innerN
    complex(8) :: first_g_arr(outerN)
    complex(8) :: secnd_g_arr(outerN)
    real(8), optional :: sqrt_driving

    ! Local variable declarations
    integer :: j = 0
    integer :: k = 0

    real(8) :: innerDeltaTime = 0
    real(8) :: twoInnerDeltaTime = 0
    real(8) :: max_t = 0
    real(8) :: max_t_incr = 0
    real(8) :: drivingValue = 0
    real(8) :: total_change = 0
    real(8) :: driving_arg = 0

    complex(8) :: c = 0
    complex(8) :: first_g_t1 = 0
    complex(8) :: first_g_t2 = 0
    complex(8) :: secnd_g_t1 = 0
    complex(8) :: secnd_g_t2 = 0

    complex(8), dimension(3) :: first_polym_coeffs
    complex(8), dimension(3) :: secnd_polym_coeffs

    ! Function declarations
    complex(8) :: Square
    real(8) :: DrivingFunction

    if (present(sqrt_driving)) then
#if CASE == 10
        sqrtParam  = sqrt_driving
#elif CASE == 11
        sqrtParam = (2 - 4 * sqrt_driving) / cdsqrt(sqrt_driving - Square(sqrt_driving))
#endif
    endif

    ! Find the difference between start time and final time
    total_change = outerFinalTime - outerStartTime

#if CASE == 10
    ! Find the value by which max_t is incremented after each iteration
    max_t_incr = total_change / (outerN)
#else
    max_t_incr = total_change / (outerN - 1)
#endif

    ! Determine the delta values
    innerDeltaTime = max_t_incr /  innerN
    twoInnerDeltaTime = innerDeltaTime * 2

    ! Compute g_0 outerN times
    do j = 1, outerN

        ! Set max time
        max_t = outerStartTime + ((j - 1) * max_t_incr)

        ! Find the initial values for g
        first_g_t1 = complex(DrivingFunction(max_t),0)
        secnd_g_t1 = -first_g_t1

        ! Reset the counter for the inner loop
        k = 0

        ! Determine the initial value for the driving function argument
        driving_arg = max_t

        do while (driving_arg > 0)

            ! Obtain the driving value
            drivingValue = DrivingFunction(driving_arg)

            c = twoInnerDeltaTime - drivingValue**2

            first_polym_coeffs(1) = -first_g_t1
            first_polym_coeffs(2) = c
            first_polym_coeffs(3) = first_g_t1 * drivingValue**2

            secnd_polym_coeffs(1) = -secnd_g_t1
            secnd_polym_coeffs(2) = c
            secnd_polym_coeffs(3) = secnd_g_t1 * drivingValue**2

            first_g_t1 = CubicRoot(first_polym_coeffs)
            secnd_g_t1 = CubicRoot(secnd_polym_coeffs)

            ! Increment counter
            k = k + 1

            ! Check driving value argument for next interation
            driving_arg = (max_t - (k * innerDeltaTime)) - innerDeltaTime

        end do

        ! Place the latest value in the arrays
        first_g_arr(j) = first_g_t1
        secnd_g_arr(j) = secnd_g_t1

    end do

end subroutine cubic_loewner
