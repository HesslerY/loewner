N = 1000;
start_time = 0;
end_time = 25;
t_arr = linspace(start_time,end_time,N);
df = 1;
info = 'exact';
initial_guess = @(t) 2 * 1i * sqrt(t) + (2/3) * t;

z_sol = zeros(N,1);

for i = 1:N

    t = t_arr(i);
    f = @(z) z + 2 * log(2 - z) - 2 * log(2) - t;

    z_sol(i) = fsolve(f,initial_guess(t));

end

plot(z_sol);

FileWriter(N,z_sol,df,start_time,end_time,info)

pause

N = 500;
t_arr = linspace(0,10,N);

initial_guess = @(t) 1 + 1i * sqrt(2*t) - (1/3) * t;

z_sol = zeros(N,1);

for i = 1:N

    t = t_arr(i);
    f = @(z) z^2 - 2*log(z) - 1 + 4*t;

    z_sol(i) = fsolve(f,initial_guess(t));

end

plot(z_sol);

fileID1 = fopen('../../writeuploewner/finalreport/data/14-0-10-500-1-Cubic-exact.csv','w');
fileID2 = fopen('../../writeuploewner/finalreport/data/14-0-10-500-2-Cubic-exact.csv','w');

for i=1:N
    fprintf(fileID1,'%.18f %.18f\n',real(z_sol(i)), imag(z_sol(i)));
    fprintf(fileID2,'%.18f %.18f\n',-real(z_sol(i)), imag(z_sol(i)));
end

fclose(fileID1);
fclose(fileID2);

N = 10;
t_arr = linspace(0,10,N);

% initial_guess = csvread(filename)

altz_sol = zeros(N,1);

a0 = 1;
d0 = 2;

for i = 1:N

    t = t_arr(i);
    f = @(z) 25*a0^4*z - 10*a0^2*z^3 + z^5 - 16*(a0^2 + d0*t)^(5/2);

    altz_sol(i) = fsolve(f,z_sol(i));

end

figure
plot(altz_sol);
title('Gubiec and Symczak')
