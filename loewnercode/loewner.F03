!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!                                                                              !
! Program: Loewner Equation                                                    !
! Purpose: Obtain exact solutions for Loewner's equation with a                !
!          variety of driving functions.                                       !
! Author:  Dolica Akello-Egwel                                                 !
!                                                                              !
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

function square(i) result(j)

    complex(8) :: i ! Argument
    complex(8) :: j ! Return value

    j = i ** 2

end function square

function driving_function(t) result(drive)

    real(8), parameter :: pi = 4. * atan(1.)
    real(8) :: t ! Argument
    real(8) :: drive ! Return value

    drive = 2 * sqrt(1 * (1 - t))

end function driving_function

program Loewner
implicit none

    ! Variables
    character (len = 32) :: arg

    integer :: NN = 0
    integer :: j = 0
    integer :: k = 0
    integer :: M = 0

    real(8) :: delta_t = 0
    real(8) :: two_delta_t = 0
    real(8) :: t = 0
    real(8) :: max_t = 0
    real(8) :: max_t_incr = 0
    real(8) :: drive_value = 0

    complex(8) :: g_t1 = 0
    complex(8) :: g_t2 = 0
    complex(8) :: b_term = 0
    complex(8) :: c_term = 0

    complex, parameter :: i = complex(0,1)

    ! Functions
    complex(8) :: square
    real(8) :: driving_function

    ! Find the value for the the number of g_0 values
    call get_command_argument(1, arg)
    read(arg,*) M

    ! Find the value for the max_t increment
    call get_command_argument(2, arg)
    read(arg,*) max_t_incr

    ! Find the value for delta_t and two_delta_t
    call get_command_argument(3, arg)
    read(arg,*) delta_t
    two_delta_t = delta_t * 2

    ! Open the output file
    open(unit = 1, file = "result.txt")

    ! Compute g_0 M times
    do j = 1, M

        max_t = j * max_t_incr
        NN = nint(max_t / delta_t)
        g_t1 = complex(driving_function(max_t),0)

        do k = 0, NN

            t = max_t - (k * delta_t)
            drive_value = driving_function(t - delta_t)
            
            b_term = (drive_value + g_t1) * 0.5
            c_term = (drive_value * g_t1) + two_delta_t
            g_t2 = b_term + cdsqrt(c_term - square(b_term)) * i
            g_t1 = g_t2
            
        end do

        ! Write the value of g_0 to the file
        write (1,*) real(g_t2), imag(g_t2)

    end do

    close(1)

end program Loewner
