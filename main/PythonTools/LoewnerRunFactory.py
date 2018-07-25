from LoewnerRun import LoewnerRun

def LoewnerRunFactory(index, start_time, final_time, outer_res, inner_res, kappa = None, alpha = None, constant = None)

    if index == CONST_IDX:
        return ConstantLoewnerRun(CONST_IDX, constant)

    if index == KAPPA_IDX:
        return KappaLoewnerRun(KAPPA_IDX, kappa)

    if index == CALPHA_IDX:
        return CAlphaLoewnerRun(CALPHA_IDX, alpha)

    return LoewnerRun(index)
