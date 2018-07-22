function CSVRootMeanSquaredError(exactSol,outerN,df,start_time,end_time,innerNs,inputdirB)

    nSols = length(innerNs);
    rms = zeros(1,nSols);

    for i = 1:nSols

        numericalSol = FileReader(outerN,innerNs(i),df,start_time,end_time,inputdirB);
        rms(i) = RootMeanSquaredError(exactSol,numericalSol);

    end

    RMSFileWriter(df,rms,innerNs)

end
