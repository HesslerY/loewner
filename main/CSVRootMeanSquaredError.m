function CSVRootMeanSquaredError(exactSol,N,df,start_time,end_time,innerNs,infos)

    nSols = length(infos);
    rms = zeros(1,nSols);

    for i = 1:nSols

        numericalSol = FileReader(N,df,start_time,end_time,infos(i));
        rms(i) = RootMeanSquaredError(exactSol,numericalSol);

    end

    RMSFileWriter(df,rms,innerNs)

end
