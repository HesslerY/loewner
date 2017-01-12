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

function driving_function(a) result(r)

    real, parameter :: pi = 3.1415927
    real :: a ! Argument
    real :: r ! Return value
    
    r = a * sin(a * pi)

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
    complex, parameter :: i = complex(0,1)      ! Imaginary unit
    real :: drive_func                    ! Driving function
    complex(8) :: square                        ! Compute x^2
    real :: driving_function
    real :: delta
    
    ! Open the output file
    open(unit = 1, file = "result.txt")

    do j = 0,101

        delta = T / NN
        two_delta = 2 * delta
        drive_func = driving_function(T - delta)

        do k = 1, NN
    
            g_T2 = ((g_T1 + drive_func) / 2) + i * cdsqrt(two_delta + (g_T1 * drive_func) - ((square(g_T1 + drive_func)) / 4))
            g_T1 = g_T2
        
        end do
        
        T = T + step

        write (1,*) real(g_T2), imag(g_T2)

    end do

    close(1)

end program Loewner
