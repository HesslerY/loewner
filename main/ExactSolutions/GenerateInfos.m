function infos = GenerateInfos(filenameBase,innerNs)

    infos = [];
    for i = 1:length(innerNs)
        infos = [infos, strcat(filenameBase,string(innerNs(i)))];
    end

end
