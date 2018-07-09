% Discretise time interval
N = 1000
tStart = 0
tFinal = 25
tRange = linspace(tStart,tFinal,N+1);
deltaT = tFinal/N;

% Set a value for alpha
alpha = 3;

% Configure pi / alpha
piOverAlpha = pi/alpha;

% Set 'original' Loewner equation
origLoewner = @(gt,gdt,drivingFunction) gt * gdt^(piOverAlpha) - gt * drivingFunction^(piOverAlpha) - gdt^(1 + piOverAlpha) + gdt*drivingFunction^(piOverAlpha) - 2*gdt*deltaT;

% Define driving function
xi = @(t) t;

% Set g_tFinal to driving function
gResult = [xi(0)];

% Iterate to find solutions from g_tFinal-1 to g_0
for i=2:length(tRange)

    % Obtain driving function for current value of t
    drivingFunction = xi(tRange(i));

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

% Plot result
plot(gResult)
title(strcat(strcat({'\xi(t) = 1 / \alpha = '},num2str(alpha))))
