function exactSol = CubicLinearExact(N,start_time,end_time) 

    exactSol = zeros(N,1);
    t_arr = linspace(start_time,end_time,N);

    initial_guess = @(t) 1 + 1i * sqrt(2*t) - (1/3) * t;

    for i = 1:N

        f = @(z) z^2 - 2*log(z) - 1 + 4*t_arr(i);
        exactSol(i) = fsolve(f,initial_guess(t_arr(i)));

    end

end
