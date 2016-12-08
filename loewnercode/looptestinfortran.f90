!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!                                                                      !
! Program: Loewner Equation                                            !
! Purpose:                                                             !
! Author: Dolica Akello-Egwel                                          !
!                                                                      !
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
program Loewner
implicit none

    real, parameter :: T = 1.0      !
    integer, parameter :: NN = 500  !
    real :: delta = T / NN          !
    integer :: j                    ! Loop counter
    complex :: g_T1 = 0.            ! 
    complex :: g_T2 = 0.            !
    complex :: i = complex(0,1)     ! Imaginary number
    
    do j = 1, NN
    
        g_T2 = (g_T1 / 2) + i * sqrt((2 * delta) - ((g_T1 ** 2) / 4))
        print *, g_T2
        g_T1 = g_T2
        
    end do

end program Loewner
