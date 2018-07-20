%
% xi(t) = t
%

N = 1000;
start_time = 0;
end_time = 25;
t_arr = linspace(start_time,end_time,N);
df = 1;

num_sol = FileReader(N,df,start_time,end_time,'10')
z_sol = zeros(N,1);

initial_guess = @(t) 2 * 1i * sqrt(t) + (2/3) * t;

for i = 1:N

    f = @(z) z + 2 * log(2 - z) - 2 * log(2) - t_arr(i);
    z_sol(i) = fsolve(f,initial_guess(t_arr(i)));

end

info = 'Exact';
PlotRegular(z_sol,num_sol,'Exact','Numerical')
title('Solution for \xi(t) = t','Interpreter','tex')
FileWriter(N,z_sol,df,start_time,end_time,info)

innerNs = [5 10 50 100 200 300 400 500];
filenameBase = ''
infos = GenerateInfos(filenameBase,innerNs)
CSVRootMeanSquaredError(z_sol,N,df,start_time,end_time,innerNs,infos)

%
% xi(t) = 1 (Cubic)
%

end_time = 10
N = 1000;
df = 0;
num_sol = FileReader(N,df,start_time,end_time,'1-Cubic-10');
z_sol = CubicLinearExact(N,start_time,end_time);

PlotCubic(z_sol,num_sol,'Exact','Numerical')
title('Cubic Solution for \xi(t) = 1','Interpreter','tex')
info = '1-Cubic-Exact';
FileWriter(N,z_sol,df,start_time,end_time,info)
info = '2-Cubic-Exact';
FileWriter(N,NegativeReal(z_sol),df,start_time,end_time,info)

innerNs = [5 10 50 100 200 300 400 500];
filenameBase = '1-Cubic-'
infos = GenerateInfos(filenameBase,innerNs)
CSVRootMeanSquaredError(z_sol,N,df,start_time,end_time,innerNs,infos)

%
% xi(t) = sqrt(1 + t) (Cubic)
%

df = 14;
N = 1000;

a0 = 1;
d0 = 1;

num_sol = FileReader(N,df,start_time,end_time,'1-Cubic-10')
p = [-1, 0, 10*a0^2, 0, -25*a0^4, 0];
exactSol = CubicSqrtOnePlusTExact(N,start_time,end_time,a0,d0)

label1 = 'Exact (Gubiec and Symczak)'
label2 = 'Numerical'
PlotCubic(exactSol,num_sol,label1,label2);
title('Cubic Solution for \xi(t) = \surd(1 + t)','Interpreter','tex')

exact_ang = FindAngle(exactSol,NegativeReal(exactSol))
nume_ang = FindAngle(num_sol,NegativeReal(num_sol))

info = '1-Cubic-Exact';
FileWriter(N,exactSol,df,start_time,end_time,info);
info = '2-Cubic-Exact';
FileWriter(N,NegativeReal(exactSol),df,start_time,end_time,info);

% Find Root Mean Squared Error

innerNs = [5 10 50 100 200 300 400 500];
filenameBase = '1-Cubic-'
infos = GenerateInfos(filenameBase,innerNs)
CSVRootMeanSquaredError(exactSol,N,df,start_time,end_time,innerNs,infos)
