% Add the ExactSolution path in order to use the NegativeReal function
addpath('../ExactSolutions')

% Discretise time interval
outerN = 200
innerN = 1
tStart = 0
tFinal = 25
tRange = linspace(tStart,tFinal,(outerN-1)*innerN);
deltaT = tRange(2);

% Set a value for alpha
alphas = [pi/2];

totalDrivingFunctions = 6;
imageCounter = 1;

drivingFunctions = [1,3,7,11];

for i = 1:length(drivingFunctions)

    for j = 1:length(alphas)

        piOverAlpha = pi/alphas(j);
        alpha = alphas(j);

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

        % Plot result
        figure
        hold on
        plot(gResultA)
        plot(gResultB)
        AddWedgeAngle(gResult,alpha)
        title(strcat(strcat(df.name,{' / \alpha = '},num2str(alpha))))
        filename = strcat(num2str(imageCounter),'.pdf')
        saveas(gcf,filename)
        hold off

        imageCounter = imageCounter + 1;

    end

end

