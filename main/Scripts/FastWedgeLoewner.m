addpath('../WedgeLoewner/')

index = 0;
start_time = 0;
final_time = 10;
inner_points = 10;
outer_points = 1000;
wedge_alpha = 1/6;
constant = 1;
kappa = 2.5;
fast = 1;

driving_functions = [0,2,4,14];

degrees = [180 150 120 90 60 30];

for i = 1:length(degrees)
    wedge_alpha = deg2rad(degrees(i));
    z_result = SolveWedgeLoewner(index,start_time,final_time,inner_points,outer_points,wedge_alpha,fast,constant,kappa);
    SaveWedgeLoewner(index,z_result,start_time,final_time,inner_points,outer_points,wedge_alpha,kappa)
    figure
    plot(z_result)
end
