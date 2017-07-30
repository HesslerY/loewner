!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!                                                                              !
! Program: exact_loewner.F03                                                   !
! Purpose: Compare the exact solution for linear driving with the numerical    !
!          solution.                                                           !
! Author:  Dolica Akello-Egwel                                                 !
!                                                                              !
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

pure function cotan(phi) result(cotan_phi)

  real(8), intent(in) :: phi
  real(8) :: cotan_phi

  cotan_phi = 1.0 / dtan(phi)

end function cotan  

program ExactLoewner
implicit none

    ! Variables
    character (len = 32) :: arg

    integer :: j = 0
    integer :: M = 0
    integer :: final_time = 0

    real(8) :: t = 0
    real(8) :: phi = 0
    real(8) :: phi_incr = 0

    complex(8) :: g_0 = 0
    
    complex, parameter :: i = complex(0,1)
    real(8), parameter :: pi = 4. * atan(1.)

    real(8) :: cotan

    ! Find the value for the the number of pi intervals
    call get_command_argument(1, arg)
    read(arg,*) M

    ! Open the output file
    open(unit = 1, file = "exact/exact_result.txt")

    phi_incr = pi / M

    ! Compute g_0 M times
    do j = 0, M

        phi = start_time + (j * phi_incr)
        g_0 = 2 - (2 * phi * cotan(phi)) + 2 * i * phi
        
        ! Write the value of g_0 to the file
        write (1,*) real(g_0), imag(g_0)

    end do

    close(1)

end program ExactLoewner
