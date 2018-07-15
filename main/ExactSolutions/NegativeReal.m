function secondTrace = NegativeReal(z)

    N = length(z);
    secondTrace = zeros(N,1);

    for i = 1:N
        secondTrace(i) = -real(z(i)) + imag(z(i))*1j;
    end

end
