function gResult = GubiecSzymczakEquation32(df,N,origLoewner,tRange)

    gResult = [df.xi(0)];

    for i = 2:N

        loewner = @(gdt) origLoewner(gResult(end),gdt,df.xi(tRange(i)));

        [x,fval,exitflag,output] = fsolve(loewner,gResult(end) + 0.5j);

        if imag(x) < imag(gResult(end)) | exitflag < 0
            break;
        end

        gResult = [gResult x];

    end

end
