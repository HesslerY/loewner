function drivingFunction = DrivingFunction(drivingNumber)

    switch drivingNumber
        case 1
            drivingFunction.xi = @(t) 1;
            drivingFunction.name = '\xi(t) = 1';
        case 2
            drivingFunction.xi = @(t) t;
            drivingFunction.name = '\xi(t) = t';
        case 3
            drivingFunction.xi = @(t) 1;
            drivingFunction.name = '\xi(t) = 1';
        otherwise
            disp('other value')
    end

end
