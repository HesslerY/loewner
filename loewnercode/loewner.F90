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
    
    drive = T * cos(T)

end function driving_function

program Loewner
implicit none
    
    integer, parameter :: NN = 500              !
    real, parameter :: step = 0.1               !
    real :: two_delta                           !
    integer :: j = 0                            ! Loop counter
    integer :: k = 0                            !
    real :: T = 0                               !
    complex(8) :: g_T1                          ! 
    complex(8) :: g_T2                          !
    complex(8) :: term
    complex, parameter :: i = complex(0,1)      ! Imaginary unit
    real :: drive_func                          ! Driving function
    complex(8) :: square                        ! Compute x^2
    real :: driving_function
    real :: delta
    
    ! Open the output file
    open(unit = 1, file = "result.txt")

    do j = 0,100

        T = step * j
        delta = T / NN
        two_delta = 2 * delta
        drive_func = driving_function(T)

        do k = 1, NN
        
            term = ((g_T1 + drive_func) / 2)
            g_T2 = term + i * cdsqrt(two_delta + (g_T1 * drive_func) - square(term))
            g_T1 = g_T2
        
        end do

        write (1,*) real(g_T2), imag(g_T2)

    end do

    close(1)

end program Loewner
