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
    real(8) :: lower_delta(total_points)
    real(8) :: upper_delta(total_points)

    complex(8) :: h
    complex(8) :: w

    ! Function declarations
    complex(8) :: compute_h

    ! Obtain the initial values for lower delta and upper delta
    lower_delta(1) = realpart(g_arr(1))
    upper_delta(1) = (imagpart(g_arr(1)) ** 2) * 0.25

    ! Obtain the initial values for the driving function and time
    driving_arr(1) = lower_delta(1)
    time_arr(1) = upper_delta(1)

    ! Iterate from 2 to the total number of g-values
    do i = 2, total_points

        ! Assign the current g-value to h
        h = g_arr(i)

        if (i < total_points) then
            w = g_arr(i + 1)
        endif

        ! Repeatedly call the h function on itself
        do j = 1, i - 1

            h = compute_h(h,lower_delta(j),upper_delta(j))
            w = compute_h(w,lower_delta(j),upper_delta(j))

        enddo

        ! Obtain the most recent value for lower delta and upper delta
        lower_delta(i) = realpart(h)
        upper_delta(i) = (imagpart(h) ** 2) * 0.25

        ! Obtain the most recently value for the driving function and time
        driving_arr(i) = driving_arr(i - 1) + lower_delta(i)
        time_arr(i) = time_arr(i - 1) + upper_delta(i)

        write (*,*) "-ve w" , compute_h((-1 * w),( -1 * lower_delta(i)), upper_delta(i))
        write (*,*) "+ve w" , compute_h(w, lower_delta(i), upper_delta(i))
        write (*,*) "-ve h" , compute_h((-1 * h),( -1 * lower_delta(i)), upper_delta(i))
        write (*,*) "+ve h" , compute_h(h, lower_delta(i), upper_delta(i))
        write (*,*)

    enddo

end subroutine inverse_loewner
