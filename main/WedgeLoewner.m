% Discretise time interval
N = 20
tStart = 0
tFinal = 25
tRange = linspace(tFinal,tStart,N+1);
deltaT = tRange(end-1);

% Configure pi / alpha
piOverAlpha = pi/2;

% Set 'original' Loewner equation
origLoewner = @(gt,gdt,drivingFunction) gt * gdt^(piOverAlpha) - gt * drivingFunction^(piOverAlpha) - gdt^(1 + piOverAlpha) + gdt*drivingFunction^(piOverAlpha) - 2*gdt*deltaT;

% Define driving function
xi = @(t) t;

% Set g_0 to driving function
gResult = [xi(tRange(1))];

for i=2:length(tRange)-1

    drivingFunction = xi(tRange(i + 1));
    newLoewner = @(gdt) origLoewner(gResult(end),gdt,drivingFunction);
    gResult = [gResult fsolve(newLoewner,gResult(end) + 5j)];

end

plot(gResult)

