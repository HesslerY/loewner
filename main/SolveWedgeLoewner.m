function gResult = SolveWedgeLoewner(tRange,df,origLoewner)

    % Set g_tFinal to driving function at time 0
    gResult = [1];

    % Iterate to find solutions from g_tFinal-1 to g_0
    for i=2:length(tRange)

        % Obtain driving function for current value of t
        drivingFunction = df.xi(tRange(i));

        % Set Loewner to be a function of g at previous time value
        newLoewner = @(gdt) origLoewner(gResult(end),gdt,drivingFunction);

        % Solve equation for g at previous time value
        [x,fval,exitflag,output] = fsolve(newLoewner,gResult(end) + 0.5j);

        % Break if fsolve fails (trace hits real axis)
        if exitflag < 0
            break;
        end

        % Add latest solution to solution array
        gResult = [gResult x];

    end

end
