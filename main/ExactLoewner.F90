program test
end program test

pure function cotan(phi) result(cotan_phi)

    ! Argument
    real(8), intent(in) :: phi

    ! Return value
    real(8) :: cotan_phi

    cotan_phi = 1.0 / dtan(phi)

end function cotan

subroutine linear_driving(n_points, g_arr)
use constants
implicit none

    ! Argument declarations
    integer :: n_points
    complex(8) :: g_arr(n_points)

    ! Local variable declarations
    integer :: j = 0
    real(8) :: phi = 0
    real(8) :: two_phi = 0
    real(8) :: phi_incr = 0

    ! Functions
    real(8) :: cotan

    phi_incr = pi / n_points

    ! Compute g_0 M times
    do j = 1, n_points

        phi = j * phi_incr
        two_phi = phi * 2

        g_arr(j) = 2 - (two_phi * cotan(phi)) + i * two_phi

    end do

    print *, phi

end subroutine linear_driving
