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

subroutine asymptotic_linear_driving(final_time,n_points,g_arr)
use constants
implicit none

    ! Argument declarations
    integer :: n_points
    complex(8) :: g_arr(n_points)
    real(8) :: final_time
    real(8) :: time_incr = 0
    real(8) :: t_j = 0

    ! Local variable declarations
    integer :: j = 0

    time_incr = final_time / (n_points - 1)

    ! Compute g_0 M times
    do j = 1, n_points

        t_j = (j - 1) * time_incr
        g_arr(j) = 2 * dlog((t_j - 2) * 0.5) + 2 * pi * i
        print *, g_arr(j)

    end do

end subroutine asymptotic_linear_driving
