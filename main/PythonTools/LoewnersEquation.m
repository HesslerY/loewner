function [F, J] = LoewnersEquation(g_current,g_previous,xi_t,pi_over_alpha,delta_t)

    F = (g_current - g_previous)/delta_t - ((2*g_previous)/(g_previous^pi_over_alpha - xi_t^pi_over_alpha));

    term_a = g_previous^pi_over_alpha - xi_t^pi_over_alpha;

    term_1 = 2 * pi_over_alpha * g_previous^pi_over_alpha;
    term_2 = term_a^2;

    term_3 = 2;
    term_4 = term_a;

    term_5 = 1 / delta_t;

    J = term_1 / term_2 - term_3 / term_4 - term_5;

end
