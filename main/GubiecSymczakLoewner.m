% Set the weight to 1
d = 1

% Set pi/2
halfPi = pi/2

% Discretise time interval
N = 1000
tStart = 0
tFinal = 25
tRange = linspace(tStart,tFinal,N+1);
deltaT = tFinal/N;

% Define Loewner's Equation
origLoewner = @(gt,gdt,drivingFunction) deltaT * d * halfPi * cos(halfPi * gdt) + (gdt - gt)*(sin(halfPi * gdt) - sin(halfPi * drivingFunction));

for i = 1:10

    % Define a driving function
    df = DrivingFunction(i);

    % Solve for the trace with a positive driving function
    firstGResult = GubiecSzymczakEquation32(df,N,origLoewner,tRange);

    % Change sign of driving function
    df.xi = @(t) -df.xi(t);

    % Solve for the trace with a negative driving function
    secondGResult = GubiecSzymczakEquation32(df,N,origLoewner,tRange);

    % Plot the result
    figure
    plot(firstGResult)
    hold on
    plot(secondGResult)
    hold off

end
