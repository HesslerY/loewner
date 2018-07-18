function gResult = SolveWedgeLoewner(tRange,innerN,outerN,df,origLoewner)

    % Set g_0 to driving function at time 0
    gResult = [df.xi(0)];

    % Disable print out every time fsolve finds a solution
    options = optimset('Display','off');

    % Iterate to find solutions from g_tFinal-1 to g_0
    for i=1:outerN-1

        % Obtain the current value for max time
        gCurrent = df.xi(tRange(i*innerN));

        % Iterate from max time to 0
        for j = i*innerN:-1:1

            % Obtain the value of the driving function for current value of t
            drivingFunction = df.xi(tRange(j));

            % Set Loewner to be a function of g at current time value
            newLoewner = @(gdt) origLoewner(gCurrent,gdt,drivingFunction);

            % Solve equation for g at previous time value
            [gCurrent,fval,exitflag,output] = fsolve(newLoewner,gCurrent + 0.5j,options);

            % Break if fsolve fails (trace hits real axis)
            if exitflag < 0
                break;
            end

        end

        % Add latest solution to solution array
        gResult = [gResult gCurrent];
        fprintf('\rProgress: %d/%d',i+1,outerN); 
    end

end
