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

PlotCubic(z_sol)
title('Exact Cubic Solution for \xi(t) = t','Interpreter','tex')
FileWriter(N,z_sol,df,start_time,end_time,info)

N = 500;
start_time = 0;
end_time = 10;
t_arr = linspace(start_time,end_time,N);
df = 14;

initial_guess = @(t) 1 + 1i * sqrt(2*t) - (1/3) * t;

z_sol = zeros(N,1);

for i = 1:N

    t = t_arr(i);
    f = @(z) z^2 - 2*log(z) - 1 + 4*t;

    z_sol(i) = fsolve(f,initial_guess(t));

end

PlotCubic(z_sol)
title('Exact Cubic Solution for \xi(t) = 1','Interpreter','tex')
info = '1-Cubic-Exact';
FileWriter(N,z_sol,df,start_time,end_time,info)
info = '2-Cubic-Exact';
FileWriter(N,NegativeReal(z_sol),df,start_time,end_time,info)

N = 500;
start_time = 0;
end_time = 10;
t_arr = linspace(start_time,end_time,N);

altz_sol = zeros(N,1);

a0 = 1;
d0 = 2;

num_sol = FileReader(N,df,start_time,end_time,'1-Cubic')
p = [-1, 0, 10*a0^2, 0, -25*a0^4, 0];

for i = 1:N

    t = t_arr(i);
    p(6) = [16*(a0^2 + d0*t)^(5/2)];
    r = roots(p);
    altz_sol(i) = r(4);

end

figure
PlotCubic(altz_sol,num_sol);
title('Exact Cubic Solution for \xi(t) = \surd(1 + 2t) (Gubiec and Symczak)','Interpreter','tex')
PlotCubic(FileReader(N,df,start_time,end_time,'1-Cubic'));
title('Numerical Cubic Solution for \xi(t) = \surd(1 + 2t)','Interpreter','tex')
