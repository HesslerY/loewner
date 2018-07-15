function z = FileReader(N,df,start_time,end_time,info)

    inputdir='/home/dolica/Documents/writeuploewner/finalreport/data/';
    extension='.csv';

    if exist('info','var')
        fileinfo=[df start_time end_time N string(info)];
    else
        fileinfo=[df start_time end_time N];
    end

    fileinfo = string(fileinfo);
    fullfilename=strcat(inputdir,join(fileinfo,'-'),extension);

    M = dlmread(fullfilename);
    z = complex(M(:,1), M(:,2));

end

