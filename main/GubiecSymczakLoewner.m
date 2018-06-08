drivingFunction = 0.5
d = 1
halfPi = pi/2

N = 500
tStart = 0
tFinal = 2
tRange = linspace(tStart,tFinal,N);
deltaT = tRange(2);

origLoewner = @(gt,gdt) deltaT * d * halfPi * cos(halfPi * gdt) + (gdt - gt)*(sin(halfPi * gdt) - sin(halfPi * drivingFunction));

gResult = zeros(1,N);
gResult(1) = drivingFunction;

for i = 2:N

    loewner = @(gdt) origLoewner(gResult(i - 1),gdt);
    gResult(i) = fsolve(loewner,gResult(i - 1));

end

gResult
