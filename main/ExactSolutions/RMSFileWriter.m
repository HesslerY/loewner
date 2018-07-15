function RMSFileWriter(df,rms,innerNs)

    extension='.csv'
    runs = length(innerNs)

    if df == 1
        outputdir='/home/dolica/Documents/writeuploewner/finalreport/data/RMS/Quadratic/';
    else
        outputdir='/home/dolica/Documents/writeuploewner/finalreport/data/RMS/Cubic/';
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

