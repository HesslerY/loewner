% Add the ExactSolution path in order to use the NegativeReal function
addpath('../ExactSolutions')

% Discretise time interval
outerN = 200
innerN = 5
tStart = 0
tFinal = 10
tRange = linspace(tStart,tFinal,(outerN-1)*innerN);
deltaT = tRange(2);

% Set a value for alpha
alphas = [pi/2];

totalDrivingFunctions = 11;
imageCounter = 1;

N = 1000;

for i = 1:totalDrivingFunctions-1

    % Set the value of alpha
    alpha = alphas(1);

    % Set the value for pi/alpha
    piOverAlpha = pi/alpha;

    % Set 'original' Loewner equation
    origLoewner = @(gt,gdt,drivingFunction) (gt - gdt)/deltaT - ((2*gdt)/(gdt^piOverAlpha - drivingFunction^piOverAlpha)); 

    % Select a driving function
    df = DrivingFunction(i);

    % Solve the Wedge Loewner function for the first trace
    gResultA = SolveWedgeLoewner(tRange,innerN,outerN,df,origLoewner);

    % Change the sign of the driving function
    df.xi = @(t) -df.xi(t); 

    % Solve the Wedge Loewner function for the second trace
    gResultB = SolveWedgeLoewner(tRange,innerN,outerN,df,origLoewner);

    % Open the files corresponding to the cubic solution
    if i == 1
        gCubicA = FileReader(N,i - 1,tStart,tFinal,'1-Cubic-10');
        gCubicB = FileReader(N,i - 1,tStart,tFinal,'2-Cubic-10');
    else
        gCubicA = FileReader(N,i - 1,tStart,tFinal,'1-Cubic');
        gCubicB = FileReader(N,i - 1,tStart,tFinal,'2-Cubic');
    end

    % Plot the wedge solution alongside the cubic solution
    WedgePlot(gResultA,gResultB,gCubicA,gCubicB,'Cubic');

    title(strcat(strcat(df.name,{' / \alpha = '},num2str(alpha))))
    filename = strcat(num2str(imageCounter),'Compare','.pdf')
    saveas(gcf,filename)

    imageCounter = imageCounter + 1;

end

