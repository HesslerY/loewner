function PlotRegular(z_sol1,z_sol2,label1,label2)

    col = hsv(2);

    figure
    p1 = plot(z_sol1,'color',col(1,:))
    hold

    if exist('z_sol2','var')
        p2 = plot(z_sol2,'color',col(2,:))
        legend([p1 p2],{label1,label2});
    end

    xlabel('Real')
    ylabel('Imaginary')

end
