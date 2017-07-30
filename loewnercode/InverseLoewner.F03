pure function compute_h(z,lower_delta,upper_delta) result(h)

    complex(8), intent(in) :: z ! Argument
    real(8), intent(in) :: lower_delta ! Argument
    real(8), intent(in) :: upper_delta ! Argument
    complex(8) :: h ! Return value

    h = cdsqrt((z - lower_delta) ** 2 + (4 * upper_delta))

end function compute_h

program InverseLoewner

    real(8) :: real_part = 0
    real(8) :: imag_part = 0

    integer :: line_no = 0
    integer :: max_lines = 100
    integer :: n = 0

    ! complex(8) :: h = 0

    complex(8), dimension(100) :: points
    complex(8), dimension(100) :: h_values
    real(8), dimension(100) :: lower_delta
    real(8), dimension(100) :: upper_delta

    real(8) :: lower_delta_sum = 0
    real(8) :: upper_delta_sum = 0

    complex(8) :: compute_h

    open(unit = 1, file = "result.txt")
    open(unit = 2, file = "output.txt")

    do line_no = 1, max_lines

        read(1, *) real_part, imag_part

        points(line_no) = complex(real_part, imag_part)
        ! print *, points(line_no)

    enddo

    lower_delta(1) = realpart(points(1))
    upper_delta(1) = (imagpart(points(1)) ** 2) * 0.25
    h_values(1) = compute_h(points(n + 1),lower_delta(1),upper_delta(1))

    do line_no = 2, max_lines

        lower_delta(line_no) = realpart(h_values(line_no - 1))
        upper_delta(line_no) = (realpart(h_values(line_no - 1)) ** 2) * 0.25

        h_values(line_no) = compute_h(points(line_no),lower_delta(1),upper_delta(1))

        do n = 2, line_no

            h_values(line_no) = compute_h(h_values(line_no),lower_delta(n),upper_delta(n))
            ! print *, line_no

        enddo

        print *, h_values(line_no)

    enddo

    lower_delta(max_lines) = realpart(h_values(max_lines - 1))
    upper_delta(max_lines) = (realpart(h_values(max_lines - 1)) ** 2) * 0.25

    do n = 1, max_lines

        lower_delta_sum = lower_delta_sum + lower_delta(n)
        upper_delta_sum = upper_delta_sum + upper_delta(n)

        write (2,*) lower_delta_sum, upper_delta_sum

    enddo

    print *, "Finished iteration."

    close(1)
    close(2)

end program InverseLoewner
