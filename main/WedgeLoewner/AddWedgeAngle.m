function AddWedgeAngle(gResult,alpha)

    maxVal = 0;

    lineX = [0];
    lineY = [0];

    gResult(end);

    if real(gResult(end)) > imag(gResult(end))
        maxVal = real(gResult(end));
    else
        maxVal = imag(gResult(end));
    end

    maxVal = 5;
    angle = pi^2/alpha;

    lineX = [lineX , maxVal * cos(angle)];
    lineY = [lineY , maxVal * sin(angle)];

    atan(imag(gResult(end))/real(gResult(end)));

    plot(lineX,lineY);

end
