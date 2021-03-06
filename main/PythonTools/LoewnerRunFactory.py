from Constants import CONST_IDX, LINR_IDX, KAPPA_IDX, CALPHA_IDX, SQRTPLUS_IDX, EXACT_CUBIC_CONSTANT, STANDARD_IDXS, CUBIC_EXACT_IDXS, QUADRATIC_FORWARD_EXACT_IDXS, NOTORIGIN_IDXS
from LoewnerRun import LoewnerRun, ConstantLoewnerRun, LinearLoewnerRun, KappaLoewnerRun, CAlphaLoewnerRun, SqrtTPlusOneLoewnerRun

class LoewnerRunFactory():

    def __init__(self, start_time, final_time, outer_points, inner_points, compile_modules = True, save_data = True, save_plot = True):

        # Set the time parameters for the factory
        self.start_time = start_time
        self.final_time = final_time

        # Set the resolution parameters for the factory
        self.outer_points = outer_points
        self.inner_points = inner_points

        # Set the compilation setting for the factory
        self.compile_modules = compile_modules

        # Set the saving options for the factory
        self.save_plot = save_plot
        self.save_data = save_data

        # Give default arguments for the extra parameters
        self.kappa = 0
        self.alpha = 0
        self.constant = 0

    def select_single_run(self,index,start_time=None,final_time=None,outer_points=None,inner_points=None,constant=None,kappa=None,alpha=None):

        # Choose the class variables for the LoewnerRun object if no alternative is given
        if start_time is None:
            start_time = self.start_time

        if final_time is None:
            final_time = self.final_time

        if outer_points is None:
            outer_points = self.outer_points

        if inner_points is None:
            inner_points = self.inner_points

        if kappa is None:
            kappa = self.kappa

        if constant is None:
            constant = self.constant

        if alpha is None:
            alpha = self.alpha

        # Create LoewnerRun object based on which driving function was chosen
        if index == CONST_IDX:
            return ConstantLoewnerRun(constant,start_time,final_time,outer_points,inner_points,self.compile_modules,self.save_data,self.save_plot)

        if index == LINR_IDX:
            return LinearLoewnerRun(start_time,final_time,outer_points,inner_points,self.compile_modules,self.save_data,self.save_plot)

        if index == KAPPA_IDX:

            if final_time > 1:
                final_time = 1

            return KappaLoewnerRun(kappa,start_time,final_time,outer_points,inner_points,self.compile_modules,self.save_data,self.save_plot)

        if index == CALPHA_IDX:
            return CAlphaLoewnerRun(alpha,start_time,final_time,outer_points,inner_points,self.compile_modules,self.save_data,self.save_plot)

        if index == SQRTPLUS_IDX:
            return SqrtTPlusOneLoewnerRun(start_time,final_time,outer_points,inner_points,self.compile_modules,self.save_data,self.save_plot)

        # Create an ordinary LoewnerRun
        return LoewnerRun(index,start_time,final_time,outer_points,inner_points,self.compile_modules,self.save_data,self.save_plot)

    def create_standard_runs(self):
        # Create a list of LoewnerRuns for driving functions that do not require additional arguments
        return [self.select_single_run(index=i) for i in STANDARD_IDXS]

    def create_wedge_runs(self):
        # Create a list of LoewnerRuns for driving functions that do not start at origin excluding Kappa
        return [self.select_single_run(index=i,constant=1) for i in NOTORIGIN_IDXS]

    def vary_kappa(self, kappas, outer_points=None, inner_points=None):

        if outer_points is None:
            outer_points=self.outer_points
        if inner_points is None:
            inner_points=self.inner_points

        # Create a list of kappa-driving LoewnerRuns with different values for kappa
        return [self.select_single_run(index=KAPPA_IDX, kappa=k, outer_points=outer_points, inner_points=inner_points) for k in kappas]

    def vary_alpha(self, alphas):
        # Create a list of calpha-driving LoewnerRuns with different values for alpha
        return [self.select_single_run(index=CALPHA_IDX, alpha=a) for a in alphas]

    def vary_inner_res(self, index, points, constant=None, kappa=None, alpha=None):
        # Create a list of LoewnerRuns with the same driving function and different values for 'inner time'
        return [self.select_single_run(index=index, inner_points=p, constant=constant, kappa=kappa, alpha=alpha) for p in points]

    def vary_final_time(self, index, times, constant=None, kappa=None, alpha=None):
        # Create a list of LoewnerRuns with the same driving function and different values for the final time
        return [self.select_single_run(index=index, final_time=t, constant=constant, kappa=kappa, alpha=alpha) for t in times]

    def create_exact_cubic(self):
        # Create a list of LoewnerRuns that have an exact cubic forward solution
        return [self.select_single_run(index=i, constant=EXACT_CUBIC_CONSTANT) for i in CUBIC_EXACT_IDXS]

    def create_exact_quadratic_forward(self):
        # Create a list of LoewnerRuns that have an exact quadratic forward solution
        return [self.select_single_run(index=i) for i in QUADRATIC_FORWARD_EXACT_IDXS]
