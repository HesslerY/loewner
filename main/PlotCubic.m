function PlotCubic(z_sol1,z_sol2,label1,label2)

    col = hsv(2);

    figure
    p1 = plot(z_sol1,'color',col(1,:))
    hold
    p2 = plot(NegativeReal(z_sol1),'color',col(1,:))

    if exist('z_sol2','var')
        p3 = plot(z_sol2,'color',col(2,:))
        p4 = plot(NegativeReal(z_sol2),'color',col(2,:))
        legend([p1 p3],{label1,label2});
    end

    xlabel('Real')
    ylabel('Imaginary')

end
