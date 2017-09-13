!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!                                                                              !
! Program: NumericalLoewner.F90                                                !
! Purpose: Obtain numerical solutions for Loewner's equation with a variety    !
!          of driving functions.                                               !
! Author:  Dolica Akello-Egwel                                                 !
!                                                                              !
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

program test
end program test

module constants
implicit none

   real(8), parameter :: pi = 4. * atan(1.)
   real(8) :: sqrt_param = 0.0
   complex, parameter :: i = complex(0,1)

end module constants

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

#else
    stop "Error: Driving function not recognised."

#endif

end function driving_function

subroutine loewners_equation(start_time, final_time, n_points, g_arr, sqrt_driving)
use constants
implicit none

    ! Argument declarations
    real(8) :: start_time
    real(8) :: final_time
    integer :: n_points
    complex(8) :: g_arr(n_points)
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

    ! Find the value by which max_t is incremented after each iteration
    max_t_incr = total_change / n_points

    ! Determine the delta values
    delta_t = max_t_incr /  100
    two_delta_t = delta_t * 2

    ! Compute g_0 n_points times
    do j = 1, n_points

        ! Set max_t
        max_t = start_time + (j * max_t_incr)

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
