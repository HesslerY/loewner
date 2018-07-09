function gResult = GubiecSzymczakEquation32(drivingFunction,N,origLoewner)

    origLoewner = @(gt,gdt) origLoewner(gt,gdt,drivingFunction);

    gResult = [drivingFunction];

    for i = 2:N

        loewner = @(gdt) origLoewner(gResult(end),gdt);

        [x,fval,exitflag,output] = fsolve(loewner,gResult(end) + 0.5j);

        if imag(x) < imag(gResult(end))
            break;
        end

        gResult = [gResult x];

    end

end
