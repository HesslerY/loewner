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

function driving_function(T) result(drive)

    real, parameter :: pi = 3.1415927
    real :: T ! Argument
    real :: drive ! Return value
    
    drive = 2 * sqrt(8 * (1 - T))

end function driving_function

program Loewner
implicit none
    
    integer :: max_t
    get_command_argument(1,max_t)
    integer, parameter :: NN = 500              !
    real, parameter :: step = 0.1               !
    real :: two_delta                           !
    integer :: j = 0                            ! Loop counter
    integer :: k = 0                            !
    real :: t = 0                               !
    complex(8) :: g_t1                          ! 
    complex(8) :: g_t2                          !
    complex(8) :: term
    complex, parameter :: i = complex(0,1)      ! Imaginary unit
    real :: drive_func                          ! Driving function
    complex(8) :: square                        ! Compute x^2
    real :: driving_function
    real :: delta
    
    ! Open the output file
    open(unit = 1, file = "result.txt")

    do while (t < max_t)

        t = step * j
        two_delta = 2 * ( t / NN )
        drive_func = driving_function(t)

        do k = 1, NN
        
            term = ((g_t1 + drive_func) / 2)
            g_t2 = term + i * cdsqrt(two_delta + (g_t1 * drive_func) - square(term))
            g_t1 = g_t2
        
        end do

        write (1,*) real(g_t2), imag(g_t2)
        j = j + 1

    end do

    close(1)

end program Loewner
