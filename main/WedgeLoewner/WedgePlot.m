function WedgePlot(WedgeA,WedgeB,CubicA,CubicB,LegendB)

    col = hsv(2);

    figure
    p1 = plot(WedgeA,'color',col(1,:));
    hold
    p2 = plot(WedgeB,'color',col(1,:));

    p3 = plot(CubicA,'color',col(2,:));
    p4 = plot(CubicB,'color',col(2,:));
    legend([p1 p3],{'Wedge \pi/2',LegendB});

    xlabel('Real')
    ylabel('Imaginary')

    hold off

end

