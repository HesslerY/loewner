function z = FileReader(outerN,innerN,df,start_time,end_time,inputdirB)

    inputdirA='../Output/Data';
    extension='.dat';

    fileinfo=[df start_time end_time outerN innerN];

    fileinfo = string(fileinfo);
    fullfilename=strcat(inputdirA,inputdirB,join(fileinfo,'-'),extension);

    M = dlmread(fullfilename);
    z = complex(M(:,1), M(:,2));

end

