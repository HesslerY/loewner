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

    j = i * i

end function square

function driving_function(t) result(drive)

    real(8), parameter :: pi = 3.1415927
    real(8) :: t ! Argument
    complex(8) :: drive ! Return value

    drive = t * sin(t * pi)

end function driving_function

program Loewner
implicit none

    ! Variables
    character (len = 32) :: arg

    integer :: NN = 0
    integer :: j = 1
    integer :: k = 0

    real(8) :: delta_t
    real(8) :: two_delta_t
    real(8) :: t = 0
    real(8) :: init_g_arg = 0
    real(8) :: n_intervals = 0
    real(8) :: max_t = 0

    !! Test !!
    real(8) :: step = 0.01

    complex(8) :: g_t1 = 0
    complex(8) :: g_t2 = 0
    complex(8) :: term = 0
    complex(8) :: drive_value = 0

    complex, parameter :: i = complex(0,1)

    ! Functions
    complex(8) :: square
    complex(8) :: driving_function

    ! Find the value for the maximum time
    call get_command_argument(1, arg)
    read(arg,*) max_t

    ! Find the value for the number of intervals
    call get_command_argument(2, arg)
    read(arg,*) n_intervals

    ! Determine delta_t and convert the number of intervals to an integer
    delta_t = ( max_t / n_intervals )
    NN = nint( n_intervals )

    print *, "delta_t:", delta_t
    print *, "NN:", NN

    ! Obtain the initial value for g
    g_t1 = driving_function(init_g_arg)
    two_delta_t = 2.0 * delta_t

    t = delta_t

    ! Open the output file
    open(unit = 1, file = "result.txt")

    ! Compute g_0 NN times
    do while (t < max_t)

        ! Compute the driving value for the updated time
        drive_value = driving_function(t - delta_t)
        ! g_t1 = driving_function(t)

        do k = 1, NN

            term = ((g_t1 + drive_value) / 2)
            g_t2 = term + cdsqrt(square(term) - two_delta_t - (g_t1 * drive_value))
            g_t1 = g_t2

        end do

        j = j + 1
        t = delta_t * j
        ! Write the value of g_0 to the file
        write (1,*) real(g_t2), imag(g_t2)

    end do

    close(1)

end program Loewner
