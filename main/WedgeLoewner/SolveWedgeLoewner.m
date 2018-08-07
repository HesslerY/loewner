function z_result = SolveWedgeLoewner(index,start_time,final_time,inner_points,outer_points,wedge_alpha,fast,constant,kappa)

    % Create an array of time steps
    time_sol = linspace(double(start_time),double(final_time),(outer_points-1)*inner_points);

    % Set the value of delta_t
    delta_t = time_sol(2);

    % Compute pi / alpha
    pi_over_alpha = pi/wedge_alpha;

    % Select a driving function
    df = DrivingFunction(index,constant,kappa);

    % Create an array of driving function values
    xi_sol = zeros(1,length(time_sol));

    % Solve the driving function for each of the time steps
    for i = 1:length(time_sol)
        xi_sol(i) = df.xi(time_sol(i));
    end

    % Set 'original' Loewner equation
    orig_loewner = @(g_current,g_previous,xi_t) WedgeLoewnersEquation(g_current,g_previous,xi_t,pi_over_alpha,delta_t);

    % Initialise an array for the results
    z_result = zeros(1,outer_points);

    % Set z_0 to driving function at time 0
    z_result(1) = xi_sol(1);

    % Define number of loop iterations
    N = outer_points-1;

    % Set a variable to store the total number of calls to fsolve that are required
    numFSolveCalls = 0;
    for i = 1:N
        for j = i*inner_points:-1:1
            numFSolveCalls = numFSolveCalls + 1;
        end
    end

    % Declare number of fsolve calls that have been made so far
    callsSoFar = 0;

    switch fast

        case 0 % 'Slow' Setting - Uses fsolve with parallel set to true

            % Configure the behaviour of fsolve
            options = optimset('Display','off','UseParallel',true,'Jacobian','on');

            % Iterate to find solutions from g_tFinal-1 to g_0
            for i=1:N

                % Set the initial values of g to the driving function values
                g_current = xi_sol(i*inner_points);

                % Iterate backwards from the 'inner' max time to 0
                for j = i*inner_points:-1:1

                    % Set Loewner to be a function of g at current time value
                    new_loewner = @(g_previous) orig_loewner(g_current,g_previous,xi_sol(j));

                    % Solve equation for g at previous time value
                    [g_current,fval,exitflag,output] = fsolve(new_loewner,g_current + 0.5j,options);

                    % Increment calls to fsolve counter
                    callsSoFar = callsSoFar + 1;

                end

                % Add latest solution to solution array
                z_result(i + 1) = g_current;

                % Print the message once a point has been found
                fprintf('\rCompleted: %d/%d (%.2f%%)',callsSoFar,numFSolveCalls,(callsSoFar*100)/numFSolveCalls);
                fprintf('\n');

            end

        case 1 % 'Fast' Setting - Uses parfor loop

            % Configure the behaviour of fsolve
            options = optimset('Display','off','Jacobian','on');

            % Prepare a wait bar
            dq = parallel.pool.DataQueue;
            wb = waitbar(0, 'Please wait...');

            % Initialise the wait bar function
            wb.UserData = [0 0 numFSolveCalls];
            afterEach(dq, @(varargin) IncrementWaitBar(wb,inner_points));

            % Iterate to find solutions from g_tFinal-1 to g_0
            parfor i=1:N

                % Set the initial values of g to the driving function values
                g_current = xi_sol(i*inner_points);

                % Iterate backwards from the 'inner' max time to 0
                for j = i*inner_points:-1:1

                    % Set Loewner to be a function of g at current time value
                    new_loewner = @(g_previous) orig_loewner(g_current,g_previous,xi_sol(j));

                    % Solve equation for g at previous time value
                    [g_current,fval,exitflag,output] = fsolve(new_loewner,g_current + 0.5j,options);

                end

                % Add latest solution to solution array
                z_result(i + 1) = g_current;

                % Update the wait bar
                send(dq, i);

            end

            % Close the wait bar
            close(wb);
    end

    % Print a message when the algorithm is complete
    fprintf('Completed.\n');

end
