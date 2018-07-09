% Set the weight to 1
d = 1

% Set pi/2
halfPi = pi/2

% Discretise time interval
N = 2000
tStart = 0
tFinal = 25
tRange = linspace(tStart,tFinal,N);
deltaT = tRange(2);

% Define Loewner's Equation
origLoewner = @(gt,gdt,drivingFunction) deltaT * d * halfPi * cos(halfPi * gdt) + (gdt - gt)*(sin(halfPi * gdt) - sin(halfPi * drivingFunction));

% Define a driving function
drivingFunction = 0.5;

% Solve for the trace with a positive driving function
firstGResult = GubiecSzymczakEquation32(drivingFunction,N,origLoewner);

% Define a driving function
drivingFunction = -0.5;

% Solve for the trace with a negative driving function
secondGResult = GubiecSzymczakEquation32(drivingFunction,N,origLoewner);

% Plot the result
plot(firstGResult)
hold on
plot(secondGResult)
