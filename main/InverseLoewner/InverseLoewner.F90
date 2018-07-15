!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!                                                                              !
! Program: InverseLoewner.F90                                                  !
! Purpose: Take an array of trace-points for the quadratic Loewner's equation  !
!          and derive the change in driving function value with respect to     !
!          time                                                                !
! Author:  Dolica Akello-Egwel                                                 !
!                                                                              !
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

! Module for defining constants
module Constants
implicit none

   ! Define 0.25
   real(8), parameter :: QUARTER = 0.25

end module Constants

! Function for finding the square of a real value
function RealSquare(base)
implicit none

    ! Argument declarations
    real(8) :: base

    ! Return value declaration
    real(8) :: RealSquare

    ! Find the square of the base
    RealSquare = base ** 2

end function RealSquare

! Function for finding the square of a complex value
function ComplexSquare(base)
implicit none

    ! Argument declarations
    complex(8) :: base

    ! Return value declaration
    complex(8) :: ComplexSquare

    ! Find the square of the base
    ComplexSquare = base ** 2

end function ComplexSquare

! Function for computing H from which the driving function values are derived
function ComputeH(z,lowerDelta,upperDelta)
implicit none

    ! Argument declarations
    complex(8), intent(in) :: z
    real(8), intent(in) :: lowerDelta
    real(8), intent(in) :: upperDelta
    
    ! Return value declaration
    complex(8) :: ComputeH

    ! Function declaration
    complex(8) :: ComplexSquare

    ! Obtain the value of h
    ComputeH = cdsqrt(ComplexSquare(z - lowerDelta) + (4 * upperDelta))

    ! Change sign of the imaginary component of h is negative
    if (imagpart(ComputeH) < 0) then
        ComputeH = ComputeH * (-1)
    endif

end function ComputeH

! Function for deriving the driving function curve from the trace-points of the quadratic Loewner's equation
subroutine InverseLoewner(gCurve, numPoints, drivingFunctionValues, timeValues)
use Constants
implicit none

    ! Argument declarations
    integer :: numPoints
    real(8) :: drivingFunctionValues(numPoints)
    real(8) :: timeValues(numPoints)
    complex(8) :: gCurve(:)

    ! Local variable declarations
    integer :: i
    integer :: j
    real(8) :: lowerDelta(numPoints)
    real(8) :: upperDelta(numPoints)
    complex(8) :: h

    ! Function declarations
    real(8) :: RealSquare
    complex(8) :: ComputeH

    ! Obtain the initial values for lower delta and upper delta
    lowerDelta(1) = realpart(gCurve(1))
    upperDelta(1) = RealSquare(imagpart(gCurve(1))) * QUARTER 

    ! Obtain the initial values for the driving function and time
    drivingFunctionValues(1) = lowerDelta(1)
    timeValues(1) = upperDelta(1)

    ! Iterate from 2 to the total number of g-values
    do i = 2, numPoints

        ! Assign the current g-value to h
        h = gCurve(i)

        ! Repeatedly call the compute_h function on the previous value of h
        do j = 1, i - 1

            h = ComputeH(h,lowerDelta(j),upperDelta(j))

        enddo

        ! Computer lower and upper delta
        lowerDelta(i) = realpart(h)
        upperDelta(i) = RealSquare(imagpart(h)) * QUARTER 

        ! Obtain the most recently value for the driving function and time
        drivingFunctionValues(i) = drivingFunctionValues(i - 1) + lowerDelta(i)
        timeValues(i) = timeValues(i - 1) + upperDelta(i)

    enddo

end subroutine InverseLoewner

! Test program for identifying compilation problems
program test
end program test

