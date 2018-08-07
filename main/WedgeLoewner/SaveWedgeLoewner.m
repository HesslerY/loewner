function SaveWedgeLoewner(index,z_result,start_time,final_time,inner_points,outer_points,wedge_alpha,kappa,drive_alpha)

    % Set the output directory
    output_directory = '../Output/Data/WedgeGrowth/';

    % Convert the wedge angle to a string
    alpha_string = string(wedge_alpha);
    alpha_string = strrep(alpha_string,".","point");

    % Place the index and alpha-string in an array
    properties_arr = [index alpha_string];

    if index == 10

        % Convert the kappa value to a string
        kappa_string = string(kappa);
        kappa_string = strrep(kappa_string,".","point");

        % Place the kappa-string in the properties array
        properties_arr = [properties_arr kappa_string];

    end

    % Convert the elements in the properties array to strings
    properties_arr = string([properties_arr start_time final_time outer_points inner_points]);

    % Join the elements in the properties array bydashes
    partial_filename = strjoin(properties_arr,'-');

    % Add the directory and file extension
    full_filename = strjoin([output_directory partial_filename '.dat'],'');

    % Convert the complex values to a 2D array
    result_array = [real(z_result); imag(z_result)]';

    % Save the array to the filesystem
    dlmwrite(full_filename,result_array,'delimiter',' ','precision','%.18f')

end
