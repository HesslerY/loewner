function [g_result_a, g_result_b] = SolveWedgeLoewner(index,start_time,final_time,inner_points,outer_points,wedge_alpha,constant,kappa,drive_alpha)

    my_cluster = parcluster('local');
    my_cluster.NumWorkers = 15;

    time_sol = linspace(double(start_time),double(final_time),(outer_points-1)*inner_points);
    delta_t = time_sol(2);

    pi_over_alpha = pi/wedge_alpha;

    xi_sol = zeros(1,length(time_sol));

    % Select a driving function
    df = DrivingFunction(index,constant,kappa,drive_alpha);

    for i = 1:length(time_sol)
        xi_sol(i) = df.xi(time_sol(i));
    end

    % Set 'original' Loewner equation
    orig_loewner = @(g_current,g_previous,xi_t) LoewnersEquation(g_current,g_previous,xi_t,pi_over_alpha,delta_t);

    % Set g_0 to driving function at time 0
    g_result_a = zeros(1,outer_points);
    g_result_b = zeros(1,outer_points);

    % Set g_0 to driving function at time 0
    g_result_a(1) = xi_sol(1);
    g_result_b(1) = -xi_sol(1);

    % Disable print out every time fsolve finds a solution
    options = optimset('Display','off','UseParallel',true,'Jacobian','on');

    % Iterate to find solutions from g_tFinal-1 to g_0
    for i=1:outer_points-1

        % Obtain the current value for max time
        g_current_a = xi_sol(i*inner_points);
        g_current_b = -g_current_a;

        % Iterate from max time to 0
        for j = i*inner_points:-1:1

            % Set Loewner to be a function of g at current time value
            new_loewner_a = @(g_previous) orig_loewner(g_current_a,g_previous,xi_sol(j));
            new_loewner_b = @(g_previous) orig_loewner(g_current_b,g_previous,-xi_sol(j));

            % Solve equation for g at previous time value
            [g_current_a,fval,exitflag,output] = fsolve(new_loewner_a,g_current_a + 0.5j,options);
            [g_current_b,fval,exitflag,output] = fsolve(new_loewner_b,g_current_b + 0.5j,options);

        end

        % Add latest solution to solution array
        g_result_a(i + 1) = g_current_a;
        g_result_b(i + 1) = g_current_b;

        fprintf('\rProgress: %d/%d',i+1,outer_points);

    end

    fprintf('\nCompleted.');
end
