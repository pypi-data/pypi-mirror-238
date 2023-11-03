"""

##### List of functions (alphabetical order) #####

## Functions WITH TESTS ###

- column_name_in_dataframe(column_name, data_frame, param_name, func_name)
- is_empty_data_frame(data_frame, param_name, func_name)



## Functions WITH some TESTS (needs improvements) ###


## Functions WITHOUT tests ###



##### List of CLASS (alphabetical order) #####







Author: Anderson Marcos Dias Canteli <andersonmdcanteli@gmail.com>

Created: October 27, 2023.

Last update: October 27, 2023



"""

##### IMPORTS #####

### Standard ###


### Third part ###

### home made ###


##### CONSTANTS #####


##### CLASSES #####


##### FUNCTIONS #####
def column_name(column_name, data_frame, param_name, func_name):
    """This function checks whether the *str* *column_name* is a valid column name for the :doc:`DataFrame <pandas:reference/api/pandas.DataFrame>` *dataframe*.

    Parameters
    ----------
    column_name : str
        The name of the column to be checked;
    data_frame : :doc:`DataFrame <pandas:reference/api/pandas.DataFrame>`
        The :doc:`DataFrame <pandas:reference/api/pandas.DataFrame>` that should contain the column named *column_name*;
    param_name : str
        The name of the parameter that received the variable *value*';
    func_name : str
        The name of the function that utilizes the parameter *param_name*;

    Returns
    -------
    True
        If variable *column_name* **IS** a valid column name for the *data_frame*;
    ValueError
        If variable *column_name* is **NOT** a valid column name for the *data_frame*;

    Examples
    --------
    >>> import pandas as pd
    >>> from paramcheckup import data_frames
    >>> df = pd.DataFrame({
        "Column A": [1, 2, 3, 4, 5],
        "Column V": [-1, -2, -3, -4, -5],
    })
    >>> print(data_frames.column_name("Column A", df, "data_frame", "my_function"))
    True

    >>> data_frames.column_name("Column B", df, "data_frame", "my_function")
    The parameter 'data_frame' in function 'my_function' does not contain a column with the name *Column B*.
    """

    if column_name not in data_frame.columns:
        try:
            raise ValueError("ColumnNameError")
        except ValueError:
            print(
                f"The parameter '{param_name}' in function '{func_name}' does not contain a column with the name *{column_name}*.\n"
            )
            raise
    return True


def is_empty(data_frame, param_name, func_name):
    """This function checks whether the *data_frame* is an empty :doc:`DataFrame <pandas:reference/api/pandas.DataFrame>`

    Parameters
    ----------
    data_frame : :doc:`DataFrame <pandas:reference/api/pandas.DataFrame>`
        The :doc:`DataFrame <pandas:reference/api/pandas.DataFrame>` to be checked for emptiness;
    param_name : str
        The name of the parameter that received the variable *value*';
    func_name : str
        The name of the function that utilizes the parameter *param_name*;

    Returns
    -------
    True
        If variable *data_frame* is **NOT** an empty :doc:`DataFrame <pandas:reference/api/pandas.DataFrame>`;
    ValueError
        If variable *data_frame* is an **EMPTY** :doc:`DataFrame <pandas:reference/api/pandas.DataFrame>`;

    Examples
    --------
    >>> from paramcheckup import data_frames
    >>> import pandas as pd
    >>> df = pd.DataFrame({
        "Dataset": [1, 2, 3, 4, 5]
    })
    >>> print(data_frames.is_empty(df, "data", "ttest"))
    True


    >>> from paramcheckup import data_frames
    >>> import pandas as pd
    >>> df = pd.DataFrame({})
    >>> data_frames.is_empty(df, "data", "ttest")
    The DataFrame 'data' in function 'ttest' is an EMPTY DataFrame.

    """

    if data_frame.empty:
        try:
            raise ValueError("EmptyDataFrameError")
        except ValueError:
            print(
                f"The DataFrame '{param_name}' in function '{func_name}' is an EMPTY DataFrame.\n"
            )
            raise
    return True
