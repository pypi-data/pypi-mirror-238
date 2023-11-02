from pandas import read_csv, read_stata
import os.path as op

dir_datasets = op.dirname(op.realpath(__file__))
data_sets = read_csv(op.join(dir_datasets, "csv/datasets.csv"), sep=",")

def datasets_path():

    """
    This will be called in the sampledatasets.py module.
    """
    return op.dirname(op.realpath(__file__))

def save_data(dframe, file_name):
    """
    Save datasets.
    """
    
    if '.' not in file_name: # default is .csv
        file_name = f'{file_name}.csv'
    if file_name.endswith('.csv'):
        file_name = f'{datasets_path()}/csv/{file_name}'
        dframe.to_csv(file_name, index=False)
    elif file_name.endswith('.xlsx') or file_name.endswith('.xlsx'):
        file_name = f'{datasets_path()}/excel/{file_name}'
        dframe.to_excel(file_name, index=False)
    else:
        raise TypeError("'file_name' must be '.csv' or '.xlsx'")

def read_dataset(name):
    """
    ```

    Read example datasets.

    Parameters
    ----------
    name : string
        Name of dataset to read (without extension).
        Must be a valid dataset present in stemlab.statistical.datasets

    Returns
    -------
    data : DataFrame
        Requested dataset.

    Examples
    --------
    >> import stemlab as stm
    >> df = stm.read_dataset('cotes_n8')
    >> df
    ```
    """
    file_name, _ = op.splitext(name) # just incase someone added an extension
    # check that dataset exist
    if file_name not in data_sets["dataset"].to_numpy():
        raise ValueError(
            "Dataset does not exist. Available datasets include: "
            f"{data_sets['dataset'].tolist()}"
        )
    # read dataset
    try:
        dframe = read_csv(op.join(dir_datasets, 'csv/' + file_name + ".csv"), sep=",")
    except:
        dframe = read_stata(op.join(dir_datasets, 'stata/' + file_name + ".dta"))

    return dframe

def show_datasets(details=True):
    """
    ```

    List available example datasets.

    Returns
    -------
    dframe : DataFrame
        A dataframe with the name and description and reference of all the
        datasets included in stemlab library.
    file_names : list
        A list of the file names for all the datasets.

    Examples
    --------

    >> import stemlab as stm
    >> desc, fnames = stm.get_datasets()
    ```
    """
    if not isinstance(details, bool):
        details = True
    dframe = data_sets
    dframe = dframe.sort_values(by='dataset')
    dframe.index = range(1, dframe.shape[0]+1)
    if details is True:
        df_or_list = dframe
    else:
        df_or_list = dframe['dataset'].tolist()
    
    return df_or_list
