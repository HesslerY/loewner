function secondTrace = NegativeReal(z)

    N = length(z);
    secondTrace = zeros(1,N);

    for i = 1:N
        secondTrace(i) = -real(z(i)) + imag(z(i));
    end

end
