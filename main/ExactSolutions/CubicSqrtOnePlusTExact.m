function exactSol = SolveSqrtOnePlusT(N,start_time,end_time,a0,d0)

    t_arr = linspace(start_time,end_time,N);

    exactSol = zeros(N,1);

    p = [-1, 0, 10*a0^2, 0, -25*a0^4, 0];

    for i = 1:N

        p(6) = 16*(a0^2 + d0*t_arr(i))^(5/2);
        r = roots(p);
        exactSol(i) = r(4);
        
    end

end
