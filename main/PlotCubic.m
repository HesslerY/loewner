function PlotCubic(z_sol)

    figure
    plot(z_sol)
    hold
    plot(NegativeReal(z_sol))
    xlabel('Real')
    ylabel('Imaginary')

end
