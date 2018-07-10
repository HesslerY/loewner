% Discretise time interval
N = 1000
tStart = 0
tFinal = 25
tRange = linspace(tStart,tFinal,N+1);
deltaT = tFinal/N;

% Set a value for alpha
alphas = [2 3 4 5];

imageCounter = 1;

for i = 3:10

    for j = 1:length(alphas)

        alpha = alphas(j);

        % Configure pi / alpha
        piOverAlpha = pi/alpha;

        % piOverAlpha = 1;

        % Set 'original' Loewner equation
        origLoewner = @(gt,gdt,drivingFunction) gt * gdt^(piOverAlpha) - gt * drivingFunction^(piOverAlpha) - gdt*gdt^(piOverAlpha) + gdt*drivingFunction^(piOverAlpha) - 2*gdt*deltaT;

        % origLoewner = @(gt,gdt,drivingFunction) gdt * gt^(piOverAlpha) - gdt * drivingFunction^(piOverAlpha) - gt*gt^(piOverAlpha) + gt*drivingFunction^(piOverAlpha) - 2*gt*deltaT;

        % origLoewner = @(gt,gdt,drivingFunction) gdt*gdt^(piOverAlpha) - gdt*drivingFunction^piOverAlpha - gt*gdt^piOverAlpha + gt*drivingFunction^piOverAlpha - 2*deltaT*gdt;

        % origLoewner = @(gt,gdt,drivingFunction) (gdt - gt)*(gt^piOverAlpha - drivingFunction^piOverAlpha) - 2*gt*deltaT;

        % Select a driving function
        df = DrivingFunction(i);

        % Solve the Wedge Loewner Function
        gResult = SolveWedgeLoewner(tRange,df,origLoewner);

        % Plot result
        figure
        hold on
        plot(NegativeReal(gResult)+2)
        AddWedgeAngle(gResult,alpha)
        title(strcat(strcat(df.name,{' / \alpha = '},num2str(alpha))))
        filename = strcat(num2str(imageCounter),'.pdf')
        saveas(gcf,filename)
        hold off

        imageCounter = imageCounter + 1;

    end

end

