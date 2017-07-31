!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!                                                                              !
! Program: NumericalLoewner.F03                                                !
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

program loewner
use constants
implicit none

    ! variables
    character (len = 32) :: arg

    integer :: NN = 0
    integer :: j = 0
    integer :: k = 0
    integer :: m = 0

    real(8) :: delta_t = 0
    real(8) :: two_delta_t = 0
    real(8) :: t = 0
    real(8) :: max_t = 0
    real(8) :: max_t_incr = 0
    real(8) :: driving_value = 0
    real(8) :: start_time = 0
    real(8) :: final_time = 0
    real(8) :: total_change = 0
    real(8) :: driving_arg = 0

    complex(8) :: g_t1 = 0
    complex(8) :: g_t2 = 0
    complex(8) :: b_term = 0
    complex(8) :: c_term = 0

    ! Functions
    complex(8) :: square
    real(8) :: driving_function

    ! Find the value for the starting time
    call get_command_argument(1, arg)
    read(arg,*) start_time

    ! Find the value for max_t
    call get_command_argument(2, arg)
    read(arg,*) final_time

    ! Find the value for the the number of g_0 values
    call get_command_argument(3, arg)
    read(arg,*) M

    ! Open the output file
    open(unit = 1, file = "result.txt")

    total_change = final_time - start_time
    max_t_incr = total_change / M
    delta_t = max_t_incr /  100
    two_delta_t = delta_t * 2

    ! Compute g_0 M times
    do j = 1, M

        max_t = start_time + (j * max_t_incr)
        g_t1 = complex(driving_value,0)
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

        ! Write the value of g_0 to the file
        write (1,*) real(g_t2), imag(g_t2)

    end do

    close(1)

end program Loewner
