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

    real, parameter :: pi = 3.1415927
    real :: t ! Argument
    real :: drive ! Return value
    
    drive = 2 * sqrt(8 * (1 - t))

end function driving_function

program Loewner
implicit none
    
    integer :: max_t
    character (len = 32) :: arg
    integer :: NN
    real, parameter :: step = 0.1               !
    real :: two_delta                           !
    integer :: j = 0                            ! Loop counter
    integer :: k = 0                            !
    real :: t = 0                               !
    complex(8) :: g_t1 = complex(0,0)                          ! 
    complex(8) :: g_t2 = complex(0,0)
    complex(8) :: term
    complex, parameter :: i = complex(0,1)      ! Imaginary unit
    real :: drive_func                          ! Driving function
    complex(8) :: square                        ! Compute x^2
    real :: driving_function
    
    call get_command_argument(1, arg)
    read(arg,*) max_t
    
    NN = nint(max_t / step)
    
    g_t1 = driving_function(0.0)
    two_delta = 2.0 * step
    
    ! Open the output file
    open(unit = 1, file = "result.txt")

    do while (t < max_t)

        t = step * j
        drive_func = driving_function(t - step)

        do k = 1, NN
        
            term = ((g_t1 + drive_func) / 2.0)
            g_t2 = term + i * cdsqrt(two_delta + (g_t1 * drive_func) - square(term))
            g_t1 = g_t2

        end do

        write (1,*) real(g_t2), imag(g_t2)
        j = j + 1

    end do ! This loop is off by one

    close(1)

end program Loewner
