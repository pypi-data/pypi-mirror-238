from numpy import sqrt
from scipy.stats import t, norm

def alternative_func(test_type, alternative, dfn, sig_level, decimals=8):
    
    crit_value = 0 # placeholder for invalid test_type
    if alternative == 'less':
        hyp_sign = '<'
        if test_type == 't':
            crit_value = abs(t.ppf(q=sig_level/2, df=round(dfn, decimals)))
        else:
            crit_value = abs(norm.ppf(q=sig_level/2))
    elif alternative == 'greater':
        hyp_sign = '>'
        if test_type == 't':
            crit_value = abs(t.ppf(q=1 - sig_level/2, df=round(dfn, decimals)))
        else:
            crit_value = abs(norm.ppf(q=1 - sig_level/2))
    else:
        hyp_sign = '\\ne'
        if test_type == 't':
            crit_value = abs(t.ppf(q=1 - sig_level, df=round(dfn, decimals)))
        else:
            crit_value = abs(norm.ppf(q=1 - sig_level))
            
    if isinstance(crit_value, (tuple, list)):
        crit_value = crit_value[0]
    
    return hyp_sign, crit_value

def corr_tpvalue(corr, n, alternative='two-sided', sig_level=.05, decimals=4):
    """
    Calculate test statistic (t) and p-value for correlation analysis
    """
    dfn = n-2
    t_cal = corr * sqrt(n - 2) / sqrt(1 - corr**2)
    if alternative == 'less':
        p_value = t.cdf(x = t_cal, df=round(dfn, decimals))
    elif alternative == 'greater':
        p_value = 1 - t.cdf(x = t_cal, df=round(dfn, decimals))
    else:
        p_value = 2 * t.cdf(x = -abs(t_cal), df=round(dfn, decimals))

    if p_value <= sig_level:
        conclusion = "Correlation is statistically significant"
    else:
        conclusion = "Correlation is NOT statistically significant"
    
    result = {
        "t_cal": t_cal, 
        "p_value":p_value, 
        "conclusion": conclusion
    }

    return result
