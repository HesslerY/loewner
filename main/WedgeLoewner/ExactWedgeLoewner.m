% Add the ExactSolution path in order to use the NegativeReal function
addpath('../ExactSolutions')

% Discretise time interval
outerN = 100
innerN = 15
tStart = 0
tFinal = 10
tRange = linspace(tStart,tFinal,(outerN-1)*innerN);
deltaT = tRange(2);

alpha = pi/2;

% Set the value for pi/alpha
piOverAlpha = pi/alpha;

totalDrivingFunctions = 11;
drivingFunctions = [1,15];
imageCounter = 1;

N = 1000;

a0 = 1;
d0 = 1;

for i = 1:length(drivingFunctions)

    % Set 'original' Loewner equation
    origLoewner = @(gt,gdt,drivingFunction) (gt - gdt)/deltaT - ((2*gdt)/(gdt^piOverAlpha - drivingFunction^piOverAlpha));

    % Select a driving function
    df = DrivingFunction(drivingFunctions(i));

    % Solve the Wedge Loewner function for the first trace
    gResultA = SolveWedgeLoewner(tRange,innerN,outerN,df,origLoewner);

    % Change the sign of the driving function
    df.xi = @(t) -df.xi(t);

    % Solve the Wedge Loewner function for the second trace
    gResultB = SolveWedgeLoewner(tRange,innerN,outerN,df,origLoewner);

    if drivingFunctions(i) == 1
        gExactA = df.cubic_exact(N,tStart,tFinal);
    else
        gExactA = df.cubic_exact(N,tStart,tFinal,a0,d0);
    end

    gExactB = NegativeReal(gExactA);

    % Plot the wedge solution alongside the cubic solution
    WedgePlot(gResultA,gResultB,gExactA,gExactB,'Exact');

    title(strcat(strcat(df.name,{' / \alpha = '},num2str(alpha))))
    filename = strcat(num2str(imageCounter),'ExactCompare','.pdf')
    saveas(gcf,filename)

    imageCounter = imageCounter + 1;

end

