function PlotCubic(z_sol1,z_sol2)

    col = hsv(2);

    figure
    plot(z_sol1,'color',col(1,:))
    hold
    plot(NegativeReal(z_sol1),'color',col(1,:))

    if exist('z_sol2','var')
        plot(z_sol2,'color',col(2,:))
        plot(NegativeReal(z_sol2),'color',col(2,:))
    end

    xlabel('Real')
    ylabel('Imaginary')

end
