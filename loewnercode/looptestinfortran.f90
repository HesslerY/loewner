!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!                                                                      !
! Program: Loewner Equation                                            !
! Purpose:                                                             !
! Author: Dolica Akello-Egwel                                          !
!                                                                      !
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
program Loewner
implicit none

    real, parameter :: T = 1.0       !
    integer, parameter :: NN = 500   !
    real :: two_delta = 2 * (T / NN) !
    integer :: j                     ! Loop counter
    complex :: g_T1 = 0.             ! 
    complex :: g_T2 = 0.             !
    complex :: i = complex(0,1)      ! Imaginary unit
    
    do j = 1, NN
    
        g_T2 = (g_T1 / 2) + i * sqrt(two_delta - ((g_T1 ** 2) / 4))
        print *, g_T2
        g_T1 = g_T2
        
    end do

end program Loewner
