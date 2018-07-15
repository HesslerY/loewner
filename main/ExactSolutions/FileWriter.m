function FileWriter(N,z_sol,df,start_time,end_time,info)

    outputdir='/home/dolica/Documents/writeuploewner/finalreport/data/'
    extension='.csv'

    if exist('info','var')
        fileinfo=[df start_time end_time N string(info)];
    else
        fileinfo=[df start_time end_time N];
    end

    fileinfo = string(fileinfo);
    fullfilename=strcat(outputdir,join(fileinfo,'-'),extension);

    fileID = fopen(fullfilename,'w');

    for i=1:N
        fprintf(fileID,'%.18f %.18f\n',real(z_sol(i)), imag(z_sol(i)));
    end

    fclose(fileID);

end
