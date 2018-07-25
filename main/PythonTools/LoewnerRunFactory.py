from Constants import CONST_IDX, LINR_IDX, KAPPA_IDX, CALPHA_IDX, SQRTPLUS_IDX
from LoewnerRun import LoewnerRun, ConstantLoewnerRun, LinearLoewnerRun, KappaLoewnerRun, CAlphaLoewnerRun, SqrtTPlusOneLoewnerRun

def LoewnerRunFactory(index, start_time, final_time, outer_points, inner_points, compile_modules = True, save_plot = True, save_data = True, kappa = None, alpha = None, constant = None):

    if index == CONST_IDX:
        return ConstantLoewnerRun(constant,start_time,final_time,outer_points,inner_points,compile_modules,save_plot,save_data)

    if index == LINR_IDX:
        return LinearLoewnerRun(start_time,final_time,outer_points,inner_points,compile_modules,save_plot,save_data)

    if index == KAPPA_IDX:

        if final_time > 1:
            final_time = 1

        return KappaLoewnerRun(kappa=kappa,start_time=start_time,final_time=final_time,outer_points=outer_points,inner_points=inner_points,compile_modules=compile_modules,save_plot=save_plot,save_data=save_data)

    if index == CALPHA_IDX:
        return CAlphaLoewnerRun(alpha,start_time,final_time,outer_points,inner_points,compile_modules,save_plot,save_data)

    if index == SQRTPLUS_IDX:
        return SqrtTPlusOneLoewnerRun(start_time,final_time,outer_points,inner_points,compile_modules,save_plot,save_data)

    return LoewnerRun(index,start_time,final_time,outer_points,inner_points,compile_modules,save_plot,save_data)
