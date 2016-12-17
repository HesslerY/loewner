!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!                                                                      !
! Program: Loewner Equation                                            !
! Purpose:                                                             !
! Author: Dolica Akello-Egwel                                          !
!                                                                      !
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
program Loewner
implicit none

    real, parameter :: step = 0.1               !
    real, parameter :: final_T = 10             !
    
    integer, parameter :: NN = 500              !
    real :: two_delta  = 0.0                    !
    integer :: j                                ! Loop counter
    integer :: k                                !
    real :: T                                   !
    complex :: g_T1 = 0.                        ! 
    complex :: g_T2 = 0.                        !
    complex, parameter :: i = complex(0,1)      ! Imaginary unit

    ! Open the output file
    open(unit = 1, file = "result.txt")

    do j = 1,100

        T = j * step
        two_delta = 2 * (T / NN)
        ! print *, T
    
        do k = 1, NN
    
            g_T2 = (g_T1 / 2) + i * sqrt(two_delta - ((g_T1 ** 2) / 4))
            g_T1 = g_T2
        
        end do

        write (1,*) g_T2

    end do

    close(1)

end program Loewner
