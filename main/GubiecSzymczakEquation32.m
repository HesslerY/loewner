function gResult = GubiecSzymczakEquation32(drivingFunction,N,origLoewner)

    origLoewner = @(gt,gdt) origLoewner(gt,gdt,drivingFunction);

    gResult = zeros(1,N);
    gResult(1) = drivingFunction;

    for i = 2:N

        loewner = @(gdt) origLoewner(gResult(i - 1),gdt);
        gResult(i) = fsolve(loewner,5j);

    end

end
