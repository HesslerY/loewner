!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!                                                                              !
! Program: ApproxLoewner.F03                                                   !
! Purpose:                                                                     !
!                                                                              !
! Author:  Dolica Akello-Egwel                                                 !
!                                                                              !
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

pure function square(i) result(j)

    complex(8), intent(in) :: i ! Argument
    complex(8) :: j ! Return value

    j = i ** 2

end function square

pure function driving_function(t) result(drive)

    real(8), parameter :: pi = 4. * atan(1.)
    real(8), intent(in) :: t ! Argument
    real(8) :: drive ! Return value

    drive = 2 * sqrt(3.5 * (1 - t))

end function driving_function

pure function g_bar(z, prev_drive, delta_t) result(val)

    complex(8), intent(in) :: z
    real(8), intent(in) :: prev_drive
    real(8), intent(in) :: delta_t
    complex(8) :: val
    complex(8) :: diff
    complex, parameter :: i = complex(0,1)
    
    diff = z - prev_drive
    val = (cdsqrt(4 * delta_t - (diff ** 2)) * i) + prev_drive
  
end function g_bar

program Loewner
implicit none

    ! Variables
    character (len = 32) :: arg

    integer :: NN = 0
    integer :: j = 0
    integer :: k = 0
    integer :: M = 0
    integer :: final_time = 0

    real(8) :: delta_t = 0
    real(8) :: two_delta_t = 0
    real(8) :: t = 0
    real(8) :: max_t = 0
    real(8) :: max_t_incr = 0
    real(8) :: drive_value = 0
    real(8) :: prev_drive_value = 0
    real(8) :: start_time = 0
    real(8) :: total_change = 0
    real(8) :: prev_drive = 0

    complex(8) :: g_t1 = 0
    complex(8) :: g_t2 = 0

    complex, parameter :: i = complex(0,1)

    ! Functions
    complex(8) :: square
    real(8) :: driving_function
    complex(8) :: g_bar

    ! Find the value for the final value of max_t
    call get_command_argument(1, arg)
    read(arg,*) max_t

    ! Find the value for the the number of g_0 values
    call get_command_argument(2, arg)
    read(arg,*) M

    ! Open the output file
    open(unit = 1, file = "exact_result.txt")
    
    delta_t = max_t / (M * 1.0)

    g_t1 = driving_function(max_t)

    ! Compute g_0 M times
    do j = 0, M

        t = max_t - (j * delta_t)
        drive_value = driving_function(t)
        prev_drive = driving_function(t - delta_t)

        g_t1 = g_bar(g_t1,prev_drive,delta_t)

        
        ! Write the value of g_0 to the file
        write (1,*) real(g_t1), imag(g_t1)

    end do

    close(1)

end program Loewner
