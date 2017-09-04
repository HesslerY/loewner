!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!                                                                              !
! Program: InverseLoewner.F90                                                  !
! Purpose:                                                                     !
! Author:  Dolica Akello-Egwel                                                 !
!                                                                              !
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

program test
end program test

pure function compute_h(z,lower_delta,upper_delta) result(h)

    complex(8), intent(in) :: z ! Argument
    real(8), intent(in) :: lower_delta ! Argument
    real(8), intent(in) :: upper_delta ! Argument
    complex(8) :: h ! Return value

    h = cdsqrt((z - lower_delta) ** 2 + (4 * upper_delta))

end function compute_h

subroutine inverse_loewner(g_arr, total_points, driving_arr, time_arr)

    ! Argument declarations
    complex(8) :: g_arr(:)
    integer :: total_points
    real(8) :: driving_arr(total_points)
    real(8) :: time_arr(total_points)

    ! Local variable declarations
    integer :: i = 0
    integer :: n = 0

    real(8) :: lower_delta(total_points)
    real(8) :: upper_delta(total_points)
    
    real(8) :: lower_delta_sum = 0
    real(8) :: upper_delta_sum = 0

    complex(8) :: h

    ! Function declarations
    complex(8) :: compute_h

    lower_delta(1) = realpart(g_arr(1))
    upper_delta(1) = (imagpart(g_arr(1)) ** 2) * 0.25
    
    do i = 2, total_points

        h = g_arr(i)

        do j = 1, i - 1

            h = compute_h(h,lower_delta(j),upper_delta(j))

        enddo

        lower_delta(i) = realpart(h)
        upper_delta(i) = (imagpart(h) ** 2) * 0.25

    enddo

    do i = 1, total_points

        lower_delta_sum = lower_delta_sum + lower_delta(i)
        upper_delta_sum = upper_delta_sum + upper_delta(i)

        driving_arr(i) = lower_delta_sum
        time_arr(i) = upper_delta_sum

    enddo

end subroutine inverse_loewner
