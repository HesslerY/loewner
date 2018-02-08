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

module Constants
implicit none

   real(8), parameter :: pi = 4. * atan(1.)
   real(8) :: sqrt_param = 0.0
   complex, parameter :: i = complex(0,1)
   complex(8), parameter :: ZERO = complex(0,0)
   complex(8), parameter :: a = 1

end module Constants

module CubicSolver
  implicit none
  public :: CubicRoot
  real :: PI = 3.14159265359
  real :: EPS = 1e-3
  real :: DELTA = 1e-5

contains
  function CubicRoot(polym_coeffs)
    implicit none

    complex(8), dimension(4) :: polym_coeffs
    complex(8), dimension(3) :: poly3zeros, As, Bs
    complex(8) :: a, b, c, a1, b1, c1, d, p, q, qu, z, alpha, CubicRoot
    real(8) :: AA, BB
    integer :: i, j

    a = polym_coeffs(1)
    b = polym_coeffs(2)
    c = polym_coeffs(3)

    p = -a*a/3 + b
    q = 2*((a/3)**3) - a*b/3 + c

    qu = (p/3)**3 + (q/2)**2

    CubicRoot = poly3zeros(1)

    do i = 2, 3
        if (imag(poly3zeros(i)) > imag(CubicRoot)) then
            CubicRoot = poly3zeros(i)
        endif
    enddo

    print *, "Is this zero?"
    print *, CubicRoot**3 + polym_coeffs(2)*CubicRoot**2 + polym_coeffs(3)*CubicRoot + polym_coeffs(4)

    ! print *, "All roots: " , poly3zeros
    ! print *, "Returned root: ", CubicRoot

  end function

end module CubicSolver

pure function square(x) result(y)

    ! Argument
    complex(8), intent(in) :: x

    ! Return value
    complex(8) :: y

    y = x ** 2

end function square

function driving_function(t) result(driving_value)
use constants

    ! Argument
    real(8), intent(in) :: t

    ! Return value
    real(8) :: driving_value

#if CASE == 0
    driving_value = 0.0

#elif CASE == 1
    driving_value = t

#elif CASE == 2
    driving_value = cos(t)

#elif CASE == 3
    driving_value = t * cos(t)

#elif CASE == 4
    driving_value = cos(t * pi)

#elif CASE == 5
    driving_value = t * cos(t * pi)

#elif CASE == 6
    driving_value = sin(t)

#elif CASE == 7
    driving_value = t * sin(t)

#elif CASE == 8
    driving_value = sin(t * pi)

#elif CASE == 9
    driving_value = t * sin(t * pi)

#elif CASE == 10
    driving_value = 2 * dsqrt(sqrt_param * (1 - t))

#elif CASE == 11
    driving_value = dsqrt(t) * sqrt_param

#elif CASE == 12
    driving_value = floor(t)

#elif CASE == 13
    driving_value = mod(floor(t), 2)

#else
    stop "Error: Driving function not recognised."

#endif

end function driving_function

subroutine loewners_equation(start_time, final_time, outer_n, inner_n, g_arr, sqrt_driving)
use constants
implicit none

    ! Argument declarations
    real(8) :: start_time
    real(8) :: final_time
    integer :: outer_n
    integer :: inner_n
    complex(8) :: g_arr(outer_n)
    real(8), optional :: sqrt_driving

    ! Local variable declarations
    integer :: j = 0
    integer :: k = 0

    real(8) :: delta_t = 0
    real(8) :: two_delta_t = 0
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
    complex(8) :: square
    real(8) :: driving_function

    if (present(sqrt_driving)) then
#if CASE == 10
        sqrt_param  = sqrt_driving
#elif CASE == 11
        sqrt_param = (2 - 4 * sqrt_driving) / cdsqrt(sqrt_driving - square(sqrt_driving))
#endif
    endif

    ! Find the difference between start time and final time
    total_change = final_time - start_time

#if CASE == 10
    ! Find the value by which max_t is incremented after each iteration
    max_t_incr = total_change / (outer_n)
#else
    max_t_incr = total_change / (outer_n - 1)
#endif

    ! Determine the delta values
    delta_t = max_t_incr /  inner_n
    two_delta_t = delta_t * 2

    ! Compute g_0 outer_n times
    do j = 1, outer_n

        ! Set max_t
        max_t = start_time + ((j - 1) * max_t_incr)

        ! Find the initial value for g_1
        g_t1 = complex(driving_function(max_t),0)

        ! Reset the counter for the inner loop
        k = 0

        ! Determine the initial value for the driving function argument
        driving_arg = max_t

        do while (driving_arg > 0)

            ! Obtain the driving value
            driving_value = driving_function(driving_arg)

            ! Solve Loewner's equation
            b_term = (driving_value + g_t1) * 0.5
            c_term = (driving_value * g_t1) + two_delta_t
            g_t2 = b_term + cdsqrt(c_term - square(b_term)) * i

            ! S
            g_t1 = g_t2

            k = k + 1
            driving_arg = (max_t - (k * delta_t)) - delta_t

        end do

        ! Place the latest value in the array
        g_arr(j) = g_t1

    end do

end subroutine loewners_equation

subroutine cubic_loewner(start_time, final_time, outer_n, inner_n, first_g_arr, secnd_g_arr, sqrt_driving)
    use constants
    use poly3zerosmodule
    implicit none

    ! Argument declarations
    real(8) :: start_time
    real(8) :: final_time
    integer :: outer_n
    integer :: inner_n
    complex(8) :: first_g_arr(outer_n)
    complex(8) :: secnd_g_arr(outer_n)
    real(8), optional :: sqrt_driving

    ! Local variable declarations
    integer :: j = 0
    integer :: k = 0

    real(8) :: delta_t = 0
    real(8) :: two_delta_t = 0
    real(8) :: max_t = 0
    real(8) :: max_t_incr = 0
    real(8) :: g1_driving_value = 0
    real(8) :: g2_driving_value = 0
    real(8) :: total_change = 0
    real(8) :: driving_arg = 0

    complex(8) :: c = 0
    complex(8) :: first_g_t1 = 0
    complex(8) :: first_g_t2 = 0
    complex(8) :: secnd_g_t1 = 0
    complex(8) :: secnd_g_t2 = 0

    complex(8), dimension(4) :: first_polym_coeffs
    complex(8), dimension(4) :: secnd_polym_coeffs

    complex(8), dimension(3) :: first_polym_roots
    complex(8), dimension(3) :: secnd_polym_roots

    ! Function declarations
    complex(8) :: square
    real(8) :: driving_function

    if (present(sqrt_driving)) then
#if CASE == 10
        sqrt_param  = sqrt_driving
#elif CASE == 11
        sqrt_param = (2 - 4 * sqrt_driving) / cdsqrt(sqrt_driving - square(sqrt_driving))
#endif
    endif

    ! Find the difference between start time and final time
    total_change = final_time - start_time

#if CASE == 10
    ! Find the value by which max_t is incremented after each iteration
    max_t_incr = total_change / (outer_n)
#else
    max_t_incr = total_change / (outer_n - 1)
#endif

    ! Determine the delta values
    delta_t = max_t_incr /  inner_n
    two_delta_t = delta_t * 2

    first_polym_coeffs(1) = a
    secnd_polym_coeffs(1) = a

    ! Compute g_0 outer_n times
    do j = 1, outer_n

        ! Set max time
        max_t = start_time + ((j - 1) * max_t_incr)

        ! Find the initial values for g
        first_g_t1 = complex(driving_function(max_t),0)
        secnd_g_t1 = -first_g_t1

        ! Reset the counter for the inner loop
        k = 0

        ! Determine the initial value for the driving function argument
        driving_arg = max_t

        do while (driving_arg > 0)

            ! Obtain the driving value
            g1_driving_value = driving_function(driving_arg)
            g2_driving_value = -g1_driving_value

            c = two_delta_t * g1_driving_value**2

            first_polym_coeffs(2) = -first_g_t1
            first_polym_coeffs(3) = c
            first_polym_coeffs(4) = first_g_t1 * g1_driving_value**2

            secnd_polym_coeffs(2) = -secnd_g_t1
            secnd_polym_coeffs(3) = c
            secnd_polym_coeffs(4) = secnd_g_t1 * g2_driving_value**2

            first_g_t1 = CubicRoot(first_polym_coeffs)
            secnd_g_t1 = CubicRoot(secnd_polym_coeffs)

            ! Increment counter
            k = k + 1

            ! Check driving value argument for next interation
            driving_arg = (max_t - (k * delta_t)) - delta_t

        end do

        print *, ""
        print *, "Final value g1:", first_g_t1
        print *, "Final value g2:", secnd_g_t1

        ! Place the latest value in the arrays
        first_g_arr(j) = first_g_t1
        secnd_g_arr(j) = secnd_g_t1

    end do

end subroutine cubic_loewner
