function rms = RootMeanSquaredError(exactSol,numericalSol)

    rms = 0;
    nPoints = length(exactSol);

    for i = 1:nPoints-1

        diff = (abs(exactSol(i+1)) - abs(numericalSol(i)))
        rms = rms + diff^2

    end

    rms = (1/(nPoints-1)) * sqrt(rms)

end
