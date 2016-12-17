!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!                                                                      !
! Program: Loewner Equation                                            !
! Purpose:                                                             !
! Author: Dolica Akello-Egwel                                          !
!                                                                      !
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
function square(i) result(j)
    complex :: i ! input
    complex :: j ! output
    j = i ** 2
end function square
 
program Loewner
implicit none
    
    integer, parameter :: NN = 500              !
    real, parameter :: step = 0.1               !
    real :: two_delta                           !
    integer :: j                                ! Loop counter
    integer :: k                                !
    real :: T                                   !
    complex :: g_T1                             ! 
    complex :: g_T2                             !
    complex, parameter :: i = complex(0,1)      ! Imaginary unit
    real, parameter :: pi = 3.1415927
    real :: driv_func
    complex :: square

    ! Open the output file
    open(unit = 1, file = "result.txt")

    do j = 1,100

        T = T + step
        two_delta = 2 * (T / NN)
        driv_func = 0
        
        do k = 1, NN
    
            g_T2 = ((g_T1 + driv_func) / 2) + i * sqrt(two_delta + (g_T1 * driv_func) - (square(g_T1 - driv_func) / 4))
            g_T1 = g_T2
        
        end do

        write (1,*) g_T2

    end do

    close(1)

end program Loewner
