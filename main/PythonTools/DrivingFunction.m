function df = DrivingFunction(index,constant,kappa,drive_alpha)

    switch index

        case 0

            df.xi = @(t) constant;
            df.cubic_exact = @(N,start_time,end_time) CubicLinearExact(N,start_time,end_time)

        case 1

            df.xi = @(t) t;

        case 2

            df.xi = @(t) cos(t);

        case 3

            df.xi = @(t) t * cos(t);

        case 4

            df.xi = @(t) cos(t * pi);

        case 5

            df.xi = @(t) t * cos(t * pi);

        case 6

            df.xi = @(t) sin(t);

        case 7

            df.xi = @(t) t * sin(t);

        case 8

            df.xi = @(t) sin(t * pi);

        case 9

            df.xi = @(t) t * sin(t * pi);

        case 10

            driving_function.xi = @(t) 2 * sqrt(kappa * (1 - t));

        case 11

            calpha = (2 - 4*drive_alpha) / sqrt(drive_alpha - drive_alpha^2)
            driving_function.xi = @(t) sqrt(t) * calpha;

        case 12

            df.xi = @(t) sqrt(t + 0.01)

        case 11

            df.xi = @(t) sqrt(1 + t)
            df.cubic_exact = @(N,start_time,end_time,a0,d0) CubicSqrtOnePlusTExact(N,start_time,end_time,a0,d0);

        otherwise

            disp('Error')
    end

end
