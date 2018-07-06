function RMSFileWriter(df,rms,innerNs)

    outputdir='../../writeuploewner/finalreport/data/'
    extension='.csv'
    runs = length(innerNs)

    fileinfo=[string(df) 'RMS'];

    fileinfo = string(fileinfo);
    fullfilename=strcat(outputdir,join(fileinfo,'-'),extension);

    fileID = fopen(fullfilename,'w');

    for i=1:length(innerNs)
        fprintf(fileID,'%d %.18f\n',innerNs(i),rms(i));
    end

    fclose(fileID);

end

