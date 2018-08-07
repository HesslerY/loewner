addpath('../WedgeLoewner/')

index = 0;
start_time = 0;
final_time = 10;
inner_points = 10;
outer_points = 500;
wedge_alpha = 4/3;
constant = 1;
kappa = 0;
drive_alpha = 0;
fast = 1;

driving_functions = [0,2,4,1];

z_result = SolveWedgeLoewner(index,start_time,final_time,inner_points,outer_points,wedge_alpha,fast,constant,kappa);
SaveWedgeLoewner(index,z_result,start_time,final_time,inner_points,outer_points,wedge_alpha,kappa)

figure
plot(z_result)
