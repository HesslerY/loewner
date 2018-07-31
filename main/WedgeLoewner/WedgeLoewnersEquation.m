function [F, J] = LoewnersEquation(g_current,g_previous,xi_t,pi_over_alpha,delta_t)

    gp_to_poa = g_previous^pi_over_alpha;

    term_a = gp_to_poa - xi_t^pi_over_alpha;

    F = (g_current - g_previous)/delta_t - ((2*g_previous)/term_a);

    term_1 = 2 * pi_over_alpha * gp_to_poa;
    term_2 = term_a^2;

    term_5 = 1 / delta_t;

    J = term_1 / term_2 - 2 / term_a - term_5;

end
