function f = Evaluate(z,p)

    f = 0;
    nterms = length(p);

    for i = 1:nterms
        power = (nterms - i);
        f = f + p(i)*z^power;
    end

end
