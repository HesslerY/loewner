%
% xi(t) = t
%

outerN = 1000;
start_time = 0;
end_time = 25;
innerN = 10;
t_arr = linspace(start_time,end_time,outerN);
df = 1;

num_sol = FileReader(outerN,innerN,df,start_time,end_time,'/Quadratic/Forward/')
z_sol = zeros(outerN,1);

initial_guess = @(t) 2 * 1i * sqrt(t) + (2/3) * t;

for i = 1:outerN

    f = @(z) z + 2 * log(2 - z) - 2 * log(2) - t_arr(i);
    z_sol(i) = fsolve(f,initial_guess(t_arr(i)));

end

info = 'Exact';
PlotRegular(z_sol,num_sol,'Exact','Numerical')
title('Solution for \xi(t) = t','Interpreter','tex')
FileWriter(outerN,z_sol,df,start_time,end_time,info,'/Quadratic/ExactSolutions/')

innerNs = [5 10 50 100 200 300 400 500];
CSVRootMeanSquaredError(z_sol,outerN,df,start_time,end_time,innerNs,'/Quadratic/Forward/')

%
% xi(t) = 1 (Cubic)
%

end_time = 10
df = 0;
num_sol = FileReader(outerN,innerN,df,start_time,end_time,'/Cubic/Forward/');
z_sol = CubicLinearExact(outerN,start_time,end_time);

PlotCubic(z_sol,num_sol,'Exact','Numerical')
title('Cubic Solution for \xi(t) = 1','Interpreter','tex')
info = 'A';
FileWriter(outerN,z_sol,df,start_time,end_time,info)
info = 'B';
FileWriter(outerN,NegativeReal(z_sol),df,start_time,end_time,info,'/Cubic/ExactSolutions/')

innerNs = [5 10 50 100 200 300 400 500];
filenameBase = '1-Cubic-'
infos = GenerateInfos(filenameBase,innerNs)
CSVRootMeanSquaredError(z_sol,N,df,start_time,end_time,innerNs,infos)

%
% xi(t) = sqrt(1 + t) (Cubic)
%

df = 14;

a0 = 1;
d0 = 1;

num_sol = FileReader(outerN,innerN,df,start_time,end_time,'1-10')
p = [-1, 0, 10*a0^2, 0, -25*a0^4, 0];
exactSol = CubicSqrtOnePlusTExact(outerN,start_time,end_time,a0,d0)

label1 = 'Exact (Gubiec and Symczak)'
label2 = 'Numerical'
PlotCubic(exactSol,num_sol,label1,label2);
title('Cubic Solution for \xi(t) = \surd(1 + t)','Interpreter','tex')

exact_ang = FindAngle(exactSol,NegativeReal(exactSol))
nume_ang = FindAngle(num_sol,NegativeReal(num_sol))

info = 'A';
FileWriter(outerN,exactSol,df,start_time,end_time,info);
info = 'B';
FileWriter(outerN,NegativeReal(exactSol),df,start_time,end_time,info,'/Cubic/ExactSolutions/');

% Find Root Mean Squared Error

innerNs = [5 10 50 100 200 300 400 500];
filenameBase = '1-Cubic-'
infos = GenerateInfos(filenameBase,innerNs)
CSVRootMeanSquaredError(exactSol,outerN,df,start_time,end_time,innerNs,infos)
