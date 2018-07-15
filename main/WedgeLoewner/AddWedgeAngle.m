function AddWedgeAngle(gResult,alpha)

    maxVal = 0;

    lineX = [0];
    lineY = [0];

    gResult(end)

    if real(gResult(end)) > imag(gResult(end))
        maxVal = real(gResult(end));
    else
        maxVal = imag(gResult(end));
    end

    maxVal = 5;

    lineX = [lineX ,maxVal * cos(pi/alpha)]
    lineY = [lineY ,maxVal * sin(pi/alpha)]

    180/alpha
    pi/alpha
    pi + pi/alpha
    pi - pi/alpha
    atan(imag(gResult(end))/real(gResult(end)))

    plot(lineX,lineY);

end
