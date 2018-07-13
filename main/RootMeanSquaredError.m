function rms = RootMeanSquaredError(exactSol,numericalSol)

    rms = 0;
    nPoints = length(exactSol);

    for i = 1:nPoints

        diff = (abs(exactSol(i)) - abs(numericalSol(i)))
        rms = rms + diff^2

    end

    rms = (1/nPoints) * sqrt(rms)

end
