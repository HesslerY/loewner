from Constants import CONST_IDX, LINR_IDX, KAPPA_IDX, CALPHA_IDX, SQRTPLUS_IDX
from LoewnerRun import LoewnerRun, ConstantLoewnerRun, LinearLoewnerRun, KappaLoewnerRun, CAlphaLoewnerRun, SqrtTPlusOneLoewnerRun

class LoewnerRunFactory():

    def __init__(self, start_time, final_time, outer_points, inner_points, compile_modules = True, save_plot = True, save_data = True):

        self.start_time = start_time
        self.final_time = final_time
        self.outer_points = outer_points
        self.inner_points = inner_points

        self.compile_modules = compile_modules
        self.save_plot = save_plot
        self.save_data = save_data

        self.standard_idxs = [i for i in range (1,10)] + [i for i in range(12,15)]
        self.exact_cubic_idx = [0,14]

    def select_single_run(self,index,start_time=None,final_time=None,outer_points=None,inner_points=None,constant=None,kappa=None,alpha=None):

        if start_time is None:
            start_time = self.start_time

        if final_time is None:
            final_time = self.final_time

        if outer_points is None:
            outer_points = self.outer_points

        if inner_points is None:
            inner_points = self.inner_points

        if index == CONST_IDX:
            return ConstantLoewnerRun(constant,start_time,final_time,outer_points,inner_points,self.compile_modules,self.save_plot,self.save_data)

        if index == LINR_IDX:
            return LinearLoewnerRun(start_time,final_time,outer_points,inner_points,self.compile_modules,self.save_plot,self.save_data)

        if index == KAPPA_IDX:

            if final_time > 1:
                final_time = 1

            return KappaLoewnerRun(kappa,start_time,final_time,outer_points,inner_points,self.compile_modules,self.save_plot,self.save_data)

        if index == CALPHA_IDX:
            return CAlphaLoewnerRun(alpha,start_time,final_time,outer_points,inner_points,self.compile_modules,self.save_plot,self.save_data)

        if index == SQRTPLUS_IDX:
            return SqrtTPlusOneLoewnerRun(start_time,final_time,outer_points,inner_points,self.compile_modules,self.save_plot,self.save_data)

        return LoewnerRun(index,start_time,final_time,outer_points,inner_points,self.compile_modules,self.save_plot,self.save_data)

    def create_standard_runs(self):
        return [self.select_single_run(index=i) for i in self.standard_idxs]

    def vary_kappa(self, kappas):
        return [self.select_single_run(index=KAPPA_IDX, kappa=k) for k in kappas]

    def vary_alpha(self, alphas):
        return [self.select_single_run(index=CALPHA_IDX, alpha=a) for a in alphas]

    def vary_inner_res(self, index, points, constant=None, kappa=None, alpha=None):
        return [self.select_single_run(index=index, inner_points=p, constant=constant, kappa=kappa, alpha=alpha) for p in points]

    def vary_final_time(self, index, times, constant=None, kappa=None, alpha=None):
        return [self.select_single_run(index=index, final_time=t, constant=constant, kappa=kappa, alpha=alpha) for t in times]

    def create_exact_cubic(self):
        constant = 1
        return [self.select_single_run(index=i, constant=constant) for i in self.exact_cubic_idx]
