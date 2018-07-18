function drivingFunction = DrivingFunction(drivingNumber)

    switch drivingNumber
        case 1
            drivingFunction.xi = @(t) 1;
            drivingFunction.name = '\xi(t) = 1';
        case 2
            drivingFunction.xi = @(t) t;
            drivingFunction.name = '\xi(t) = t';
        case 3
            drivingFunction.xi = @(t) cos(t);
            drivingFunction.name = '\xi(t) = cos(t)';
        case 4
            drivingFunction.xi = @(t) t * cos(t);
            drivingFunction.name = '\xi(t) = t * cos(t)';
        case 5
            drivingFunction.xi = @(t) cos(t * pi);
            drivingFunction.name = '\xi(t) = cos(t * \pi)';
        case 6
            drivingFunction.xi = @(t) t * cos(t * pi);
            drivingFunction.name = '\xi(t) = t * cos(t * \pi)';
        case 7
            drivingFunction.xi = @(t) sin(t);
            drivingFunction.name = '\xi(t) = sin(t)';
        case 8
            drivingFunction.xi = @(t) t * sin(t);
            drivingFunction.name = '\xi(t) = t * sin(t)';
        case 9
            drivingFunction.xi = @(t) sin(t * pi);
            drivingFunction.name = '\xi(t) = sin(t * \pi)';
        case 10
            drivingFunction.xi = @(t) t * sin(t * pi);
            drivingFunction.name = '\xi(t) = t * sin(t * \pi)';
        case 11
            drivingFunction.xi = @(t) sqrt(t + 0.01)
            drivingFunction.name = '\xi(t) = \surd(t + 0.01)';
        otherwise
            disp('other value')
    end

end
