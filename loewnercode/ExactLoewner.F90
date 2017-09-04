pure function cotan(phi) result(cotan_phi)

    ! Argument
    real(8), intent(in) :: phi

    ! Return value
    real(8) :: cotan_phi

    cotan_phi = 1.0 / dtan(phi)

end function cotan

subroutine linear_driving(start_time, num_intervals)
use constants
implicit none

    ! Argument declarations
    integer :: num_intervals
    real(8) :: start_time

    ! Local variable declarations
    integer :: j = 0

    real(8) :: phi = 0
    real(8) :: phi_incr = 0

    complex(8) :: g_0 = 0

    ! Functions
    real(8) :: cotan

    ! Return value declaration
    complex(8) :: g_arr(num_intervals)

    ! Compute the number of internals for linear driving approximation
    phi_incr = pi / num_intervals

    ! Compute g_0 M times
    do j = 0, num_intervals

        phi = start_time + (j * phi_incr)
        g_0 = 2 - (2 * phi * cotan(phi)) + 2 * i * phi

        ! Place the latest value in the array
        g_arr(j) = g_0

    end do

end subroutine linear_driving