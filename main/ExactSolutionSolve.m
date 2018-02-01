N = 1000;
t_arr = linspace(0,25,N);

initial_guess = @(t) 2 * 1i * sqrt(t) + (2/3) * t;

z_sol = zeros(N,1);

for i = 1:N

    t = t_arr(i);
    f = @(z) z + 2 * log(2 - z) - 2 * log(2) - t;

    z_sol(i) = fsolve(f,initial_guess(t));

end

plot(z_sol);

fileID = fopen('/../../writeuploewner/finalreport/data/1-0-25-1000-exact.csv','w');

for i=1:N
    fprintf(fileID,'%.18f %.18f\n',real(z_sol(i)), imag(z_sol(i)));
end

fclose(fileID);
