from LoewnerRun import LoewnerRun

def LoewnerRunFactory(index, start_time, final_time, outer_res, inner_res, save_plot = True, save_data = True, kappa = None, alpha = None, constant = None)

    if index == CONST_IDX:
        return ConstantLoewnerRun(constant)

    if index == KAPPA_IDX:
        return KappaLoewnerRun(kappa)

    if index == CALPHA_IDX:
        return CAlphaLoewnerRun(alpha)

    if index == SQRTPLUS_IDX:
        return SqrtTPlusOneLoewnerRun()

    return LoewnerRun(index,start_time,final_time,outer_res,inner_res,save_plot,save_data)
