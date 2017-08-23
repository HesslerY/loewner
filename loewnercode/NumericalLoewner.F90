!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!                                                                              !
! Program: NumericalLoewner.F90                                                !
! Purpose: Obtain numerlical solutions for Loewner's equation with a variety   !
!          of driving functions.                                               !
! Author:  Dolica Akello-Egwel                                                 !
!                                                                              !
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

module constants
implicit none

   real, parameter :: pi = 3.1415926536
   complex, parameter :: i = complex(0,1)
 
end module constants

pure function square(x) result(j)

    complex(8), intent(in) :: x ! Argument
    complex(8) :: j ! Return value

    j = x ** 2

end function square

function driving_function(t) result(driving_value)
use constants

    real(8), intent(in) :: t ! argument
    real(8) :: driving_value ! return value
 
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
#ifdef KAPPA
    driving_value = 2 * dsqrt(KAPPA * (1 - t))
#else
    stop "Error: Square-root driving selected but KAPPA is undefined."
#endif

#elif CASE == 11
#ifdef C_ALPHA
    driving_value = dsqrt(t) * C_ALPHA
#else
    stop "Error: Square-root driving selected but C_ALPHA is undefined."
#endif

#else
    stop "Error: Driving function selection not recognised."

#endif

end function driving_function

subroutine loewners_equation(start_time, final_time, n_points, g_arr)
use constants
implicit none

    ! Argument declerations
    real(8) :: start_time
    real(8) :: final_time
    integer :: n_points 

    ! Local variable declerations
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

    ! Functions
    complex(8) :: square
    real(8) :: driving_function

    ! Return value decleration
    complex(8) :: g_arr(n_points)
    
    total_change = final_time - start_time
    max_t_incr = total_change / n_points
    delta_t = max_t_incr /  100
    two_delta_t = delta_t * 2

    ! Compute g_0 n_points times
    do j = 1, n_points

        max_t = start_time + (j * max_t_incr)
        g_t1 = complex(driving_function(max_t),0)
        k = 0
        driving_arg = max_t

        do while (driving_arg > 0)

            driving_value = driving_function(driving_arg)
            
            b_term = (driving_value + g_t1) * 0.5
            c_term = (driving_value * g_t1) + two_delta_t
            g_t2 = b_term + cdsqrt(c_term - square(b_term)) * i
            g_t1 = g_t2

            k = k + 1
            driving_arg = (max_t - (k * delta_t)) - delta_t

        end do

        g_arr(j) = g_t1

    end do

end subroutine loewners_equation
