function RMSFileWriter(df,rms,innerNs)

    extension='.dat'
    runs = length(innerNs)

    if df == 1
        outputdir='../Output/Data/Quadratic/RootMeanSquared/';
    else
        outputdir='../Output/Data/Cubic/RootMeanSquared/';
    end

    fileinfo=[string(df) 'RMS'];

    fileinfo = string(fileinfo);
    fullfilename=strcat(outputdir,join(fileinfo,'-'),extension)

    fileID = fopen(fullfilename,'w');

    for i=1:length(innerNs)
        fprintf(fileID,'%d %.18f\n',innerNs(i),rms(i));
    end

    fclose(fileID);

end

