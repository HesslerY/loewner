from math import pi, sin, cos, sqrt, floor

class DrivingFunction:

    def __init__(self, index, constant = None, kappa = None, alpha = None):

        if index == 0:

            self.name = "Constant"
            self.constant = constant
            self.plot_title = "$\\xi (t) = " + str(self.constant) + "$"
            self.xi = lambda t: self.constant

        if index == 1:

            self.name = "t"
            self.plot_title = "$\\xi (t) = t$"
            self.xi = lambda t: t

        if index == 2:

            self.name = "cos(t)"
            self.plot_title = "$\\xi (t) = \cos(t)$"
            self.xi = lambda t: cos(t)

        if index == 3:

            self.name = "t * cos(t)"
            self.plot_title = "$\\xi (t) = t \ \cos(t)$"
            self.xi = lambda t: t * cos(t)

        if index == 4:

            self.name = "cos(t * pi)"
            self.plot_title = "$\\xi (t) = \cos(\pi t)$"
            self.xi = lambda t: cos(pi * t)

        if index == 5:

            self.name = "t * cos(t * pi)"
            self.plot_title = "$\\xi (t) = t \ \cos(\pi t)$"
            self.xi = lambda t: t * cos(pi * t)

        if index == 6:

            self.name = "sin(t)"
            self.plot_title = "$\\xi (t) = \sin(t)$"
            self.xi = lambda t: sin(t)

        if index == 7:

            self.name = "t * sin(t)"
            self.plot_title = "$\\xi (t) = t \ \sin(t)$"
            self.xi = lambda t: t * sin(t)

        if index == 8:

            self.name = "sin(t * pi)"
            self.plot_title = "$\\xi (t) = \sin(\pi t)$"
            self.xi = lambda t: sin(pi * t)

        if index == 9:

            self.name = "t * sin(t * pi)"
            self.plot_title = "$\\xi (t) = t \ \sin(\pi t)$"
            self.xi = lambda t: t * sin(pi * t)

        if index == 10:

            self.name = "2 * dsqrt(kappa * (1 - t))"
            self.kappa = kappa
            self.plot_title = "xi (t) = 2 \ \sqrt{" + str(self.kappa)[:3] + "\ (1 - t)}$"
            self.xi = lambda t: sqrt(self.kappa * (1 - t))

        if index == 11:

            self.name = "dsqrt(t) * c_alpha"
            self.alpha = alpha
            self.calpha = (2 - 4 * alpha) / sqrt(alpha - alpha**2)
            self.plot_title = "$\\xi (t) = c_{" + str(self.alpha)[:3] + "} \sqrt{t}$"
            self.xi = lambda t: self.calpha * sqrt(t)

        if index == 12:

            self.name = "floor(t)"
            self.plot_title = "$\\xi (t) = \lfloor t \\rfloor $"
            self.xi = lambda t: floor(t)

        if index == 13:

            self.name = "floot(t) % 2"
            self.plot_title = "$\\xi (t) = \lfloor t \\rfloor \ \\mathrm{mod} \ 2$"
            self.xi = lambda t: floor(t) % 2

        if index == 14:

            self.name = "sqrt(1 + t)"
            self.plot_title = "$\\xi (t) = \sqrt{1 + t}$"
            self.xi = lambda t: sqrt(1 + t)
