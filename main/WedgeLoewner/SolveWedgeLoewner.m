function [wedge_result_a, wedge_result_b] = WedgeLoewner(index, start_time, final_time, outer_points, inner_points, wedge_alpha, const, kappa, drive_alpha)

    % Declare empty arrays for the results
    wedge_result_a = zeros(1, outer_points);
    wedge_result_b = zeros(1, outer_points);

    % Obtain the time solution and the value of delta_t
    time_sol = linspace(start_time,final_time,(outer_points-1)*inner_points);
    delta_t = time_sol(2);
    increment = delta_t * 1j;

    % Obtain the value for pi/alpha
    pi_over_alpha = pi/alpha;

    % Set 'original' Loewner equation
    orig_loewner = @(g_current,g_previous,xi_t) (g_current - g_previous)/delta_t - ((2*g_previous)/(g_previous^pi_over_alpha - xi_t^pi_over_alpha));

    % Select a driving function
    df = DrivingFunction(index,constant,kappa,drive_alpha);

    % Set g_0 to driving function at time 0
    wedge_result_a(1) = df.xi(time_sol(1));
    wedge_result_b(1) = -df.xi(time_sol(1));

    % Disable print out every time fsolve finds a solution
    options = optimset('Display','off','UseParallel',true);

    % Iterate to find solutions from g_tFinal-1 to g_0
    for i=1:outer_points-1

        % Obtain the current value for max time
        temp_sol_a = df.xi(time_sol(i*inner_points));
        temp_sol_a = df.xi(time_sol(i*inner_points));

        % Find the latest value for the driving function
        xi_t_a = time_sol(i*inner_points)

        % Solve equation for g at previous time value (with kick for imaginary solution)
        [temp_sol_a,fval,exitflag,output] = fsolve(@(g_previous) orig_loewner(temp_sol_a,g_previous,xi_t_a), temp_sol_a + increment,options);
        [temp_sol_b,fval,exitflag,output] = fsolve(@(g_previous) orig_loewner(temp_sol_b,g_previous,-xi_t_a),temp_sol_b + increment,options);

        % Iterate from max time to 0
        for j = (i*inner_points)-1:-1:1

            % Obtain the value of the driving function for current value of t
            xi_t_a = df.xi(time_sol(j));

            % Solve equation for g at previous time value
            [temp_sol_a,fval,exitflag,output] = fsolve(@(g_previous) orig_loewner(temp_sol_a,g_previous,xi_t_a), temp_sol_a,options);
            [temp_sol_b,fval,exitflag,output] = fsolve(@(g_previous) orig_loewner(temp_sol_b,g_previous,-xi_t_a),temp_sol_b,options);

            % Break if fsolve fails (trace hits real axis)
            if exitflag < 0
                break;
            end

        end

        % Add latest solution to solution array
        wedge_result_a(i) = temp_sol_a;
        wedge_result_b(i) = temp_sol_b;

    end

end
