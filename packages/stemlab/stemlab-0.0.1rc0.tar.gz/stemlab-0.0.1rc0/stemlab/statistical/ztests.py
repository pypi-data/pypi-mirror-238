from pandas import DataFrame, Series, concat
from numpy import unique, round, asfarray, sqrt
from scipy.stats import norm
from ..core.validate import (
    val_boolean, val_decimals, val_string, val_listitems, val_len_equal,
    val_numeric
)
from ..core.arraylike import to_listuple, is_iterable
from ..core.errors import RequiredError
from ..core.htmlatex import pzt_table
from ..statistical.dataframes import series_name
from ..statistical.decisions import test_decision, test_conclusion
from ..core.files import write_html
from ..statistical.core import alternative_func

def _statistics_func(
        method, methods, sample1, sample2, std1, std2, conf_level
):

    sample1 = Series(sample1)
    n1 = len(sample1)
    mean1 = sample1.mean()
    sem1 = std1 / sqrt(n1)

    if method in methods[1:]:
        sample2 = Series(sample2)
        sample12 = concat([sample1, sample2])
        n2 = len(sample2)
        mean2 = sample2.mean()
        sem2 = std2 / sqrt(n2)

        # combined
        n12 = n1 + n2
        mean12 = sample12.mean()
        std12 = sample12.std()
        sem12 = sample12.sem()
        
        # confidence intervals
        LCI2, UCI2 = norm.interval(
            confidence=conf_level,
            loc=mean2,
            scale=sem2
        ) 
        
        LCI12, UCI12 = norm.interval(
            confidence=conf_level,
            loc=mean12,
            scale=sem12
        )

        sample_diff = sample1 - sample2
        n12_diff = n1
        mean12_diff = sample_diff.mean()
        std12_diff = sample_diff.std()
        sem12_diff = sample_diff.sem()
        LCI12_diff, UCI12_diff = norm.interval(
            confidence=conf_level,
            loc=mean12_diff,
            scale=sem12_diff
        )

    else: # one-sample
        n2, n12, n12_diff, mean2, mean12, std2, std12, sem2, sem12 = [0] * 9
        mean12_diff, std12_diff, sem12_diff = [0] * 3
        LCI2, UCI2, LCI12, UCI12, LCI12_diff, UCI12_diff = [0] * 6
    
    dfn_name, dfn = [0] * 2 # dfn is not needed for ztest

    # confidence intervals
    LCI1, UCI1 = norm.interval(
        confidence=conf_level,
        loc=mean1,
        scale=sem1
    )
    
    return (n1, n2, n12, n12_diff, mean1, mean2, mean12, mean12_diff,
            std1, std2, std12, std12_diff, sem1, sem2, sem12, sem12_diff,
            LCI1, UCI1, LCI2, UCI2, LCI12, UCI12, LCI12_diff, UCI12_diff, 
            dfn, dfn_name
            )

def hypothesis_func(
        method, 
        sample1, 
        sample2,
        sample2_or_group,
        hyp_mean, 
        std1,
        std2,
        alternative, 
        dfn,
        decimals
):

    if 'one' in method or sample2_or_group is None:
        test_name = 'one-sample-z'
        table_title = 'One-sample z test'
        n1 = len(sample1)
        mean1 = sample1.mean()
        z_cal = (mean1 - hyp_mean) / (std1 / sqrt(n1))
        p_value = _p_value(alternative, z_cal)
    elif 'two' in method:
        test_name = 'two-samples-z'
        table_title = 'Two sample z test'
        z_cal = 1/7
        p_value = 1/7
    elif 'paired' in method:
        test_name = 'paired-samples-z'
        table_title = 'Paired z test'
        sample_diff = sample1 - sample2
        z_cal = sample_diff.mean() / sqrt(len(sample_diff))
        p_value = _p_value(alternative, z_cal)
    
    return test_name, table_title, z_cal, p_value

def _p_value(alternative, z_cal):
    """
    Calculate the p-value.
    """
    if alternative == 'less':
        p_value = norm.cdf(x = z_cal)
    elif alternative == 'greater':
        p_value = 1 - norm.cdf(x = z_cal)
    else:
        p_value = 2 * norm.cdf(x = -abs(z_cal))

    return p_value

def other_options_func(
        alternative, conf_level, decimals
):

    # alternative='two-sided',
    alternatives = ['less', 'two-sided', 'greater']
    alternative = val_string(par_name='alternative', user_input=alternative)
    alternative = val_listitems(
        par_name='alternative', 
        valid_items=alternatives, 
        user_input=alternative
    )
    
    # conf_level
    conf_level = val_numeric(
        user_input=conf_level, to_float=True, par_name='conf_level'
    )
    conf_level = val_listitems(
        par_name='conf_level',
        valid_items=[.90, .95, .99],
        user_input=conf_level
    )
    
    # decimals
    decimals = val_decimals(decimals=decimals)
    
    return alternative, conf_level, decimals

def ztest(
        sample1, 
        sample2_or_group,
        by_group=False,
        hyp_mean=0,
        std1=1,
        std2=1,
        alternative='two-sided', 
        method='one-sample',
        conf_level=.95,
        decimals=4
    ):
    """
    ```

    Mean comparison using z test.

    Parameters
    ----------

    Returns
    -------

    Examples
    --------
    >> import stemlab as stm
    >> df = stm.read_dataset(name='scores')
    
    ## One-sample z test
    ## -----------------
    >> result = stm.ztest(
            sample1=df['score_before'], 
            sample2_or_group=None, 
            hyp_mean=32.75, 
            alternative='two-sided', 
            method='one-sample'
        )
    >> result

    ## Paired samples z test
    ## ---------------------
    >> result = stm.ztest(
            sample1=df['score_before'], 
            sample2_or_group=df['score_after'], 
            alternative='less', 
            method='paired-samples'
        )
    >> result
    
    ## Two samples z test
    ## ------------------
    >> result = stm.ztest(
            sample1=df['score_before'], 
            sample2_or_group=df['gender'], 
            alternative='greater', 
            method='two-samples'
        )
    >> result
    ```
    """
    # method
    methods = ['one-sample', 'two-samples', 'paired-samples']
    method = val_string(par_name='method', user_input=method)
    method = val_listitems(
        par_name='method', valid_items=methods, user_input=method
    )
    
    # sample1
    sample1_name = series_name(data=sample1, n=1) # if Series, get the name
    sample1 = to_listuple(
        array_values=sample1, to_ndarray=True, par_name='sample1'
    )

    # by_group
    by_group = val_boolean(user_input=by_group, default=False)

    # sample2_or_group
    if sample2_or_group is None: # if None, then perform one-sample z test
        method = 'one-sample'
        sample2, sample2_name = (None, None)
    else:
        if method in methods[1:]: # two-samples and paired samples
            hyp_mean = 0
            sample2_name = series_name(data=sample2_or_group, n=2)
            sample2 = to_listuple(
                array_values=sample2_or_group, 
                to_ndarray=True, 
                par_name='sample2_or_group'
            )
            # if there are only two categories, then it must be `grouped by` 
            # so force by_group=True 
            # (this avoids avoidable crushing, and going back to user)
            if len(unique(sample2)) == 2:
                by_group = True
            # paired
            if method == 'paired-samples':
                # validate number of elements (when by_group=False)
                if len(unique(sample2)) == 2:
                    raise TypeError(
                        f"'sample_or_group' is categorical, maybe you "
                        "intended to perform `two-samples z test`"
                    )
                _ = val_len_equal(
                        x=sample1, 
                        y=sample2, 
                        par_name=['sample1', 'sample2_or_group']
                    )
                # force this to be False so that the branch below is not 
                # evaluated
                by_group = False

            if by_group is True:
                # validate number of elements
                _ = val_len_equal(
                    x=sample1, y=sample2, par_name=['sample1', 'sample2_or_group']
                )
                # check there are exactly 2 categories
                unique_groups = unique(sample2)
                _ = to_listuple(
                    array_values=unique_groups, 
                    n=2, 
                    label='exactly', 
                    par_name='sample2_or_group'
                )
                # get the sample names from the categories
                sample1_name, sample2_name = unique_groups
                dframe = DataFrame(data=[sample1, sample2]).T
                dframe.columns = ['values', 'group']
                sample1 = dframe[dframe['group'] == unique_groups[0]]
                sample2 = dframe[dframe['group'] == unique_groups[1]]
                sample1 = asfarray(sample1.iloc[:, 0].values.flatten())
                sample2 = asfarray(sample2.iloc[:, 0].values.flatten())
            
            if method == 'paired-samples':
                # validate number of elements (when by_group=False)
                _ = val_len_equal(
                        x=sample1, 
                        y=sample2, 
                        par_name=['sample1', 'sample2_or_group']
                    )
            # raise error if sample1 and sample2 are the same
            if sample1.tolist() == sample2.tolist():
                raise ValueError(
                    "'sample1' and 'sample_or_group' are identical"
                )
        else: # one-sample z test
            sample2, sample2_name = (None, None)
            # hyp_mean
            if not hyp_mean:
                raise RequiredError(
                    par_name='hyp_mean', required_when="method='one-sample'"
                )
            hyp_mean = val_numeric(
                user_input=hyp_mean, to_float=False, par_name='hyp_mean'
            )

    alternative, conf_level, decimals = other_options_func(
        alternative, conf_level, decimals
    )

    # begin calculations 
    # ------------------

    (n1, n2, n12, n12_diff, mean1, mean2, mean12, mean12_diff,
     std1, std2, std12, std12_diff, sem1, sem2, sem12, sem12_diff,
     LCI1, UCI1, LCI2, UCI2, LCI12, UCI12, LCI12_diff, UCI12_diff,
     dfn, dfn_name) = _statistics_func(
         method, methods, sample1, sample2, std1, std2, conf_level
     )

    # z test
    sig_level = 1 - conf_level
    one_sample = 'one' in method # True / False
    
    # hypothesis and z_critical
    test_type = 'z'
    hyp_sign, z_crit = alternative_func(test_type, alternative, dfn, sig_level, decimals)

    # z statistic and p-value
    test_name, table_title, z_cal, p_value = hypothesis_func(
        method, 
        sample1, 
        sample2,
        sample2_or_group,
        hyp_mean, 
        std1,
        std2,
        alternative,
        dfn,
        decimals
    )

    decision = test_decision(
        p_value=round(p_value, decimals), 
        sig_level=round(sig_level, decimals),
        decimals=decimals
    )

    conclusion = test_conclusion(
        test_name,
        sample1_name,
        sample2_name,
        mean1,
        mean2,
        hyp_mean,
        std1,
        std2,
        round(z_cal, decimals),
        round(dfn, decimals),
        alternative,
        p_value,
        round(sig_level, 3)
    )

    result_table = pzt_table(
        table_title,
        sample1_name, 
        sample2_name, 
        n1, 
        n2, 
        n12,
        n12_diff,
        mean1, 
        mean2, 
        mean12, 
        mean12_diff,
        std1, 
        std2, 
        std12,
        std12_diff,
        sem1, 
        sem2, 
        sem12, 
        sem12_diff,
        LCI1, 
        UCI1,
        LCI2, 
        UCI2,
        LCI12, 
        UCI12,
        LCI12_diff, 
        UCI12_diff,
        z_cal,
        hyp_mean,
        round(dfn, decimals),
        dfn_name,
        hyp_sign,
        round(z_crit, decimals),
        p_value,
        round(conf_level, decimals),
        round(sig_level, decimals),
        one_sample,
        decision,
        conclusion,
        decimals
    )

    write_html(file_name='ttest.html', html_list=result_table)

    statistics = {
        'test_name': test_name,
        'alternative': alternative,
        'Mean1': mean1,
        'Mean2': mean2,
        'hyp_mean': hyp_mean,
        'mean_comb': mean12,
        'mean_diff': mean12_diff,
        'LCI': {'LCI1': LCI1, 'LCI2': LCI2, 'LCI12': LCI12},
        'UCI': {'UCI1': UCI1, 'UCI2': UCI2, 'UCI_comb': UCI12},
        'z_cal': z_cal,
        'df': dfn,
        'z_crit': z_crit,
        'sig_level': round(sig_level, 4),
        'conf_level': round(conf_level, 4),
        'p_value': p_value
    }

    return statistics

def ztest_stats(
        sample_size,
        sample_mean,
        sample_sd,
        hyp_mean,
        alternative='two-sided', 
        method='one-sample', 
        conf_level=.95,
        decimals=4
):
    """
    ```

    Mean comparison using z test.

    Parameters
    ----------

    Returns
    -------

    Examples
    --------
    ## n1 = 24; mean1 = 62.60; sd1 = 15.8;
    ## n2 = 24; mean2 = 51.34; sd2 = 13.4;
    >> result = stm.ttest_stats(
        sample_size=[24, 24],
        sample_mean=[62.6, 51.34],
        sample_sd=[15.8, 13.4],
        hyp_mean=0,
        alternative='greater',
        method='two-samples',
        conf_level=0.95,
        decimals=8
    )
    ```
    """
    
    if 'one' in method.lower():
        # sample_size
        try:
            n1 = int(sample_size) # will crush if not number
        except:
            if is_iterable(array_like=sample_size):
                sample_size = to_listuple(
                    array_values=sample_size, 
                    n=1, 
                    to_ndarray=True, 
                    label='exactly', 
                    par_name='sample_size'
                )
            n1 = sample_size[0]

        # sample_mean
        try:
            mean1 = float(sample_mean)
        except:
            if is_iterable(array_like=sample_mean):
                sample_mean = to_listuple(
                    array_values=sample_mean, 
                    n=1, 
                    to_ndarray=True, 
                    label='exactly', 
                    par_name='sample_mean'
                )
            mean1 = sample_mean[0]

        # sample_sd
        try:
            std1 = float(sample_sd)
        except:
            if is_iterable(array_like=sample_sd):
                sample_sd = to_listuple(
                    array_values=sample_sd, 
                    n=1, 
                    to_ndarray=True, 
                    label='exactly', 
                    par_name='sample_sd'
                )
            std1 = sample_sd[0]
        
        sem1 = std1/sqrt(n1)
        
        # hyp_mean
        hyp_mean = val_numeric(
            par_name='hyp_mean',
            user_input=hyp_mean
        )

        dfn_name = 'Degrees of freedom'
        dfn = n1 - 1
        n2, n12, n12_diff, mean2, mean12, std2, std12, sem2, sem12 = [0] * 9
        mean12_diff, std12_diff, sem12_diff = [0] * 3
        LCI2, UCI2, LCI12, UCI12, LCI12_diff, UCI12_diff = [0] * 6
    else:
        sample_size = to_listuple(
            array_values=sample_size, 
            n=2, 
            to_ndarray=True, 
            label='exactly', 
            par_name='sample_size'
        )
        n1, n2 = sample_size

        sample_mean = to_listuple(
            array_values=sample_mean, 
            n=2, 
            to_ndarray=True, 
            label='exactly', 
            par_name='sample_mean'
        )
        mean1, mean2 = sample_mean

        sample_sd = to_listuple(
            array_values=sample_sd, 
            n=2, 
            to_ndarray=True, 
            label='exactly', 
            par_name='sample_sd'
        )
        std1, std2 = sample_sd

        sem1 = std1/sqrt(n1)
        sem2 = std2/sqrt(n2)

        # combined
        n12 = n1 + n2
        mean12 = (n1 * mean1 + n2 * mean2) / n12
        d1, d2 = (mean1 - mean12, mean2 - mean12)
        std12 = sqrt(
            (n1 * std1**2 + n2 * std2**2 + n1 * d1**2 + n2 * d2**2) / n12
        )
        sem12 = std12 / sqrt(n12)

        n12_diff, mean12_diff , std12_diff, sem12_diff= [0] * 4
        LCI12_diff, UCI12_diff = [0] * 2

        # confidence intervals
        LCI2, UCI2 = norm.interval(
            confidence=conf_level,
            loc=mean2,
            scale=sem2
        ) 
        
        LCI12, UCI12 = norm.interval(
            confidence=conf_level,
            loc=mean12,
            scale=sem12
        )

    # should be here, not inside any of the above if-else satement
    LCI1, UCI1 = norm.interval(
        confidence=conf_level,
        loc=mean1,
        scale=sem1
    )

    alternative, conf_level, decimals = other_options_func(
        alternative, conf_level, decimals
    )

    # z test
    sig_level = 1 - conf_level
    one_sample = 'one' in method # True / False
    
    # hypothesis and z_critical
    test_type = 't'
    hyp_sign, z_crit = alternative_func(
        test_type, alternative, dfn, sig_level, decimals
    )

    # z statistic and p-value
    if 'one' in method:
        test_name = 'one-sample-z'
        table_title = 'One-sample z test'
        z_cal = (mean1 - hyp_mean) / (std1 / sqrt(n1))
        p_value = _p_value(alternative, z_cal)
    elif 'two' in method.lower():
        test_name = 'two-samples-z'
        z_cal, p_value = 1/7, 1/7

    decision = test_decision(
        p_value=round(p_value, decimals), 
        sig_level=round(sig_level, decimals)
    )

    sample1_name, sample2_name = ('Sample 1', 'Sample 2')

    conclusion = test_conclusion(
        test_name,
        sample1_name,
        sample2_name,
        mean1,
        mean2,
        hyp_mean,
        std1,
        std2,
        round(z_cal, decimals),
        round(dfn, decimals),
        alternative,
        p_value,
        round(sig_level, 3)
    )

    result_table = pzt_table(
        table_title,
        sample1_name, 
        sample2_name, 
        n1, 
        n2, 
        n12,
        n12_diff,
        mean1, 
        mean2, 
        mean12, 
        mean12_diff,
        std1, 
        std2, 
        std12,
        std12_diff,
        sem1, 
        sem2, 
        sem12, 
        sem12_diff,
        LCI1, 
        UCI1,
        LCI2, 
        UCI2,
        LCI12, 
        UCI12,
        LCI12_diff, 
        UCI12_diff,
        z_cal,
        hyp_mean,
        round(dfn, decimals),
        dfn_name,
        hyp_sign,
        round(z_crit, decimals),
        p_value,
        round(conf_level, decimals),
        round(sig_level, decimals),
        one_sample,
        decision,
        conclusion,
        decimals
    )

    write_html(file_name='ttest.html', html_list=result_table)

    statistics = {
        'test_name': test_name,
        'alternative': alternative,
        'Mean1': mean1,
        'Mean2': mean2,
        'hyp_mean': hyp_mean,
        'mean_comb': mean12,
        'mean_diff': mean12_diff,
        'LCI': {'LCI1': LCI1, 'LCI2': LCI2, 'LCI12': LCI12},
        'UCI': {'UCI1': UCI1, 'UCI2': UCI2, 'UCI_comb': UCI12},
        'z_cal': z_cal,
        'df': dfn,
        'z_crit': z_crit,
        'sig_level': round(sig_level, 4),
        'conf_level': round(conf_level, 4),
        'p_value': p_value
    }

    return statistics