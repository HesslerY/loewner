drivingFunction = 0.5;
d = 1
halfPi = pi/2

N = 500
tStart = 0
tFinal = 2
tRange = linspace(tStart,tFinal,N);
deltaT = tRange(2);

origLoewner = @(gt,gdt,drivingFunction) deltaT * d * halfPi * cos(halfPi * gdt) + (gdt - gt)*(sin(halfPi * gdt) - sin(halfPi * drivingFunction));

drivingFunction = 0.5;
firstGResult = GubiecSzymczakEquation32(drivingFunction,N,origLoewner);

drivingFunction = -0.5;
secondGResult = GubiecSzymczakEquation32(drivingFunction,N,origLoewner);

plot(firstGResult)
hold on
plot(secondGResult)
