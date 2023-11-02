from ..core.validate import val_numeric, val_listitems, val_string

def _pvalue_alternative(alternative, t_cal, dfn=None, p_value=None):
    """
    P-value and alternative hypothesis phrase.
    """

    if p_value >= 0.001:
        if dfn is None:
            pvalue_str = (
                f"p = {round(p_value, 3)}"
            )
        else:
            pvalue_str = (
                f"t({round(dfn, 2)}) = {round(t_cal, 2)}, p = {round(p_value, 3)}"
            )
    else:
        pvalue_str = (
            f"p < .001"
        )
    # add trailing zeros
    for n in range(9):
        pvalue_str = pvalue_str.replace(f'.{n})', f'.{n}0)')
        pvalue_str = pvalue_str.replace(f'.{n},', f'.{n}0,')
        pvalue_str = pvalue_str.replace(f'.0)', f'.00)')
        pvalue_str = pvalue_str.replace(f'.0,', f'.00,')

    pvalue_str = pvalue_str.replace('p = 1', 'p = 1.00')

    # direction in the conclusion
    if alternative == 'less':
        alternative = 'lower than'
    elif alternative == 'greater':
        alternative = 'greater than'
    else:
        alternative = 'different from'

    return pvalue_str, alternative

def _conclusion_str(conclusion_str):
    """
    Ensure two decimal places (i.e. add trailing zeros)
    """
    # remove the leading zero in float
    conclusion_str.replace('(0.', '(.').replace(' 0.', '.')
    # remove trailing zero in integers
    conclusion_str = conclusion_str.replace('.0\\', '\\')
    for n in range(9):
        conclusion_str = conclusion_str.replace(f'.{n})', f'.{n}0)')
        conclusion_str = conclusion_str.replace(f'.{n},', f'.{n}0,')
        conclusion_str = conclusion_str.replace(f'.0)', f'.00)')
        conclusion_str = conclusion_str.replace(f'.0,', f'.00,')

    return conclusion_str

def test_decision(p_value, sig_level, decimals):
    """
    ```
    Making a decision about the null hypothesis.

    Parameters
    ----------
    p_value : float
        The p-value.
    sig_level : float
        The level of significance.

    Returns
    -------
    decision_str : str
        A string with the decision statement.
    ```
    """
    # p_value
    p_value = val_numeric(
        par_name='p_value', 
        limits=[0, 1], 
        boundary='inclusive', 
        user_input=p_value
    )
    
    # sig_level
    sig_level = val_listitems(
        par_name='sig_level', 
        valid_items=[.1, .05, .01],
        user_input=sig_level
    )

    if p_value <= sig_level:
        decision_str = (
            f"Reject \(\\text{{H}}_{{0}}\) "
            f"since the p-value \(({round(p_value, decimals)})\) is less "
            f"than the level of significance \(({round(sig_level, 3)})\)."
        )
    else:
        decision_str = (
            f"Fail to reject \(\\text{{H}}_{{0}}\) "
            f"since the p-value \(({round(p_value, decimals)})\) is greater "
            f"than the level of significance \(({round(sig_level, 3)})\)."
        )
    decision_str = decision_str.replace('(0.', '(.').replace(' 0.', '.')
    decision_str = decision_str.replace('1.0)', '1.000)')
    decision_str = decision_str.replace('.0)', '.000)')

    return decision_str

def test_conclusion(*args):
    """
    ```
    Making a decision about the null hypothesis.

    Parameters
    ----------
    p_value : float
        The p-value.
    sig_level : float
        The level of significance.

    Returns
    -------
    conclusion_str : str
        A string with the conclusion statement.
    ```
    """
    (test_name, sample1_name, sample2_name, mean1, mean2, hyp_mean,
    std1, std2, t_cal, dfn, alternative, p_value, sig_level) = args
    # test_name
    test_names = [
        'one-sample-p', 'two-samples-p', 'paired-samples-p',
        'one-sample-z', 'two-samples-z', 'paired-samples-z',
        'one-sample-t', 'two-samples-t', 'paired-samples-t'
    ]
    test_name = val_string(
        par_name='test_name', user_input=test_name
    )
    test_name = val_listitems(
        par_name='test_name', valid_items=test_names, user_input=test_name
    )

    # alternative,
    alternatives = ['less', 'two-sided', 'greater']
    alternative = val_string(par_name='alternative', user_input=alternative)
    alternative = val_listitems(
        par_name='alternative', 
        valid_items=alternatives, 
        user_input=alternative
    )

    # p_value
    p_value = val_numeric(
        par_name='p_value', 
        limits=[0, 1], 
        boundary='inclusive', 
        user_input=p_value
    )

    # sig_level
    sig_level = val_listitems(
        par_name='sig_level', 
        valid_items=[.1, .05, .01],
        user_input=sig_level
    )

    zt_tests = [
        'two-samples-z', 'paired-samples-z', 'two-samples-t', 'paired-samples-t'
    ]
    
    if test_name == 'one-sample-p':
        conclusion_str = _p1_sample(
            alternative, mean1, hyp_mean, t_cal, p_value, sig_level
        )
        
    elif test_name in ['two-samples-p', 'paired-samples-p']:
        conclusion_str = _p2_samples(alternative, p_value, sig_level)

    elif test_name in ['one-sample-z', 'one-sample-t']:
        conclusion_str = _t1_sample(
            alternative, mean1, hyp_mean, std1, t_cal, dfn, p_value, sig_level
        )
    elif test_name in zt_tests:
        conclusion_str = _t2_samples(
            alternative,
            sample1_name,
            sample2_name,
            mean1,
            mean2,
            std1,
            std2,
            t_cal,
            dfn,
            p_value,
            sig_level
        )

    return conclusion_str

def _p1_sample(alternative, p_value, sig_level):
    pass

def _p2_samples(alternative, p_value, sig_level):
     pass

def _z1_sample(alternative, p_value, sig_level):
     pass

def _z2_samples(alternative, p_value, sig_level):
     pass

def _t1_sample(*args):

    alternative, mean1, hyp_mean, std1, t_cal, dfn, p_value, sig_level = args
    
    pvalue_str, alternative = _pvalue_alternative(
        alternative=alternative,
        t_cal=t_cal,
        dfn=dfn,
        p_value=p_value
    )
    
    if p_value <= sig_level: # significant
        conclusion_str = (
            f"The population mean "
            f"\((M = {round(mean1, 2)}, SD = {round(std1, 2)})\) is "
            f"{alternative} the hypothesized mean \((M = {round(hyp_mean, 2)})\). "
            f"The mean difference of \({round(abs(mean1 - hyp_mean), 2)}\) is "
            f"statistically significant at "
            f"\({round(sig_level, 3) * 100}\%, {pvalue_str}\)."
        )
    else: # not significant
        conclusion_str = (
            f"The population mean "
            f"\((M = {round(mean1, 2)}, SD = {round(std1, 2)})\) "
            f"is not statistically significantly {alternative} the "
            f"hypothesized mean "
            f"\((M = {round(hyp_mean, 2)}), ~{pvalue_str}\)."
        )
    
    conclusion_str = _conclusion_str(conclusion_str)

    return conclusion_str

def _t2_samples(*args):

    (alternative, sample1_name, sample2_name, mean1, mean2,
     std1, std2, t_cal, dfn, p_value, sig_level) = args
     
    pvalue_str, alternative = _pvalue_alternative(
        alternative=alternative,
        t_cal=t_cal,
        dfn=dfn,
        p_value=p_value
    )
    
    if p_value <= sig_level: # significant
        conclusion_str = (
            f"The population mean of \(\\textbf{{{sample1_name}}}\) "
            f"\((M = {round(mean1, 2)}, SD = {round(std1, 2)})\) "
            f"is {alternative} that of \(\\textbf{{{sample2_name}}}\) "
            f"\((M = {round(mean2, 2)}, SD = {round(std2, 2)})\). "
            f"The mean difference of "
            f"\({round(abs(mean1 - mean2), 2)}\) is statistically "
            f"significant at \({round(sig_level, 3) * 100}\%, {pvalue_str}\)."
        )
    else: # not significant
        conclusion_str = (
            f"The population mean of \(\\textbf{{{sample1_name}}}\) "
            f"\((M = {round(mean1, 2)}, SD = {round(std1, 2)})\) "
            f"is not statistically significantly {alternative} "
            f"that of \(\\textbf{{{sample2_name}}}\) "
            f"\((M = {round(mean2, 2)}, SD = {round(std2, 2)}), ~{pvalue_str}\)."
        )
    
    conclusion_str = _conclusion_str(conclusion_str)

    return conclusion_str