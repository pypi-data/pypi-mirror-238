"""
##### List of functions (alphabetical order) #####

## Functions WITH TESTS ###
- is_bool(value, param_name, func_name)
- is_data_frame(data_frame, param_name, func_name)
- is_dict(value, param_name, func_name)
- is_float(value, param_name, func_name)
- is_int(value, param_name, func_name)
- is_list_of_types(my_list, param_name, func_name, expected_type)
- is_list(value, param_name, func_name)
- is_numpy(value, param_name, func_name)
- is_str(value, param_name, func_name)
- is_subplots(value, param_name, func_name)


## Functions WITH some TESTS (needs improvements) ###


## Functions WITHOUT tests ###

##### List of CLASS (alphabetical order) #####


Author: Anderson Marcos Dias Canteli <andersonmdcanteli@gmail.com>

Created: October 24, 2023.

Last update: October 26, 2023

"""

##### IMPORTS #####

### Standard ###


### Third part ###
import numpy as np
import pandas as pd
from matplotlib.axes import SubplotBase

### home made ###


##### CONSTANTS #####


##### CLASSES #####


##### FUNCTIONS #####
def is_bool(value, param_name, func_name):
    """This function checks whether a variable *value* is of the *bool* type.

    Parameters
    ----------
    value : any type
        The variable that is tested as being of type *bool*;
    param_name : str
        The name of the parameter that received the variable *value*';
    func_name : str
        The name of the function that utilizes the parameter *param_name*;


    Returns
    -------
    True
        If variable *value* **IS** of the *bool* type;
    TypeError
        If variable *value* is **NOT** of the *bool* type;


    Examples
    --------
    >>> from paramcheckup import types
    >>> print(types.is_bool(True, "param", "my_function"))
    True

    >>> from paramcheckup import types
    >>> types.is_bool(None, "param", "my_function")
    The parameter 'param' in function 'my_function' must be of type *bool*, but its type is *NoneType*.

    """
    if isinstance(value, bool) is False:
        try:
            raise TypeError("NotBoolError")
        except TypeError:
            print(
                f"The parameter '{param_name}' in function '{func_name}' must be of type *bool*, but its type is *{type(value).__name__}*.\n"
            )
            raise
    return True


def is_data_frame(data_frame, param_name, func_name):
    """This function checks whether a variable *data_frame* is of the :doc:`DataFrame <pandas:reference/api/pandas.DataFrame>` type.

    Parameters
    ----------
    data_frame : any type
        The variable that is tested as being of :doc:`DataFrame <pandas:reference/api/pandas.DataFrame>` type;
    param_name : str
        The name of the parameter that received the variable *data_frame*';
    func_name : str
        The name of the function that utilizes the parameter *param_name*;


    Returns
    -------
    True
        If variable *data_frame* **IS** of the :doc:`DataFrame <pandas:reference/api/pandas.DataFrame>` type;
    TypeError
        If variable *data_frame* is **NOT** of the :doc:`DataFrame <pandas:reference/api/pandas.DataFrame>` type;


    Examples
    --------
    >>> from paramcheckup import types
    >>> import pandas as pd
    >>> df = pd.DataFrame({
        "Dataset": [1, 2, 3, 4, 5]
    })
    >>> print(types.is_data_frame(df, "data", "ttest"))
    True

    >>> from paramcheckup import types
    >>> data = (1, 2, 3, 4, 5)
    >>> types.is_data_frame(data, "data", "ttest")
    The parameter 'data' in function 'ttest' must be of type *DataFrame*, but its type is *tuple*.

    """
    if isinstance(data_frame, pd.DataFrame) is False:
        try:
            raise TypeError("NotDataFrameError")
        except TypeError:
            print(
                f"The parameter '{param_name}' in function '{func_name}' must be of type *DataFrame*, but its type is *{type(data_frame).__name__}*.\n"
            )
            raise
    return True


def is_dict(value, param_name, func_name):
    """This function checks whether a variable *value* is of the *dict* type.

    Parameters
    ----------
    value : any type
        The variable that is tested as being of type *dict*;
    param_name : str
        The name of the parameter that received the variable *'value*';
    func_name : str
        The name of the function that utilizes the parameter *param_name*;


    Returns
    -------
    True
        If variable *value* **IS** of the *dict* type;
    TypeError
        If variable *value* is **NOT** of the *dict* type;


    Examples
    --------
    >>> from paramcheckup import types
    >>> param = {
        "Exp A": [1, 2, 3, 4, 5],
        "Exp B": [1, 2, 3, 4, 5, 6, 7, 8],
    }
    >>> print(types.is_dict(param, "param", "my_function"))
    True


    >>> from paramcheckup import types
    >>> param = [1, 2, 3, 4, 5]
    >>> types.is_dict(param, "param", "my_function")
    The parameter 'param' in function 'my_function' must be of type *dict*, but its type is *list*.

    """
    if isinstance(value, dict) is False:
        try:
            raise TypeError("NotDictError")
        except TypeError:
            print(
                f"The parameter '{param_name}' in function '{func_name}' must be of type *dict*, but its type is *{type(value).__name__}*.\n"
            )
            raise
    return True


def is_float(value, param_name, func_name):
    """This function checks whether a variable *value* is of the *float* type.

    Parameters
    ----------
    value : any type
        The variable that is tested as being of *float* type;
    param_name : str
        The name of the parameter that received the variable *value*';
    func_name : str
        The name of the function that utilizes the parameter *param_name*;

    Returns
    -------
    True
        If variable *value* **IS** of the *TYPE* float;
    TypeError
        If variable *value* is **NOT** of the *float* type;


    Notes
    -----
    The following types are considered to be *True*:

    * *float*;
    * *np.floating*;

    Examples
    --------
    >>> from paramcheckup import types
    >>> print(types.is_float(0.05, "alpha", "ttest"))
    True


    >>> from paramcheckup import types
    >>> types.is_float(5, "alpha", "ttest")
    The parameter 'alpha' in function 'ttest' must be of type *float*, but its type is *int*.

    """
    if isinstance(value, (float, np.floating)) is False:
        try:
            raise TypeError("NotFloatError")
        except TypeError:
            print(
                f"The parameter '{param_name}' in function '{func_name}' must be of type *float*, but its type is *{type(value).__name__}*.\n"
            )
            raise
    else:
        return True


def is_int(value, param_name, func_name):
    """This function checks whether a variable *value* is of the *int* type.

    Parameters
    ----------
    value : any type
        The variable that is tested as being of *int* type;
    param_name : str
        The name of the parameter that received the variable *value*';
    func_name : str
        The name of the function that utilizes the parameter *param_name*;


    Returns
    -------
    True
        If variable *value* **IS** of the *int* type;
    TypeError
        If variable *value* is **NOT** of the *int* type;


    Notes
    -----
    The following types are considered to be *True*:

    * *int*;
    * *np.uint*;
    * *np.integer*;


    Examples
    --------
    >>> from paramcheckup import types
    >>> print(types.is_int(5, "tcalc", "ttest"))
    True

    >>> from paramcheckup import types
    >>> print(types.is_int(5.0, "tcalc", "ttest"))
    The parameter 'tcalc' in function 'ttest' must be of type *int*, but its type is *float*.

    """
    if isinstance(value, (int, np.uint, np.integer)) is False:
        try:
            raise TypeError("NotIntError")
        except TypeError:
            print(
                f"The parameter '{param_name}' in function '{func_name}' must be of type *int*, but its type is *{type(value).__name__}*.\n"
            )
            raise
    return True


def is_list_of_types(my_list, param_name, func_name, expected_type):
    """ "This function checks whether all elements in the *list*  *my_list* have the expected type of *expected_type*."

    Parameters
    ----------
    my_list :  list
        The *list* that the values are tested as being of *expected_type* type;
    param_name : str
        The name of the parameter that received the variable *my_list*;
    func_name : str
        The name of the function that utilizes the parameter *param_name*;
    expected_type : any
        The type that each element of the *list* *my_list* must possess.


    Returns
    -------
    True
        If all elements in  *my_list* are of the type *expected_type*;
    TypeError
        If at least one elements in *my_list* **IS NOT** of type *expected_type*;

    Examples
    --------
    >>> from paramcheckup import types
    >>> x_exp = [1, 2, 3, 4, 5]
    >>> expected_type = int
    >>> print(types.is_list_of_types(x_exp, "x_data", "tcalc", expected_type))
    True


    >>> from paramcheckup import types
    >>> x_exp = [1, 2.0, 3, 4, 5]
    >>> expected_type = int
    >>> types.is_list_of_types(x_exp, "x_data", "tcalc", expected_type)
    At least one element in parameter 'x_data' of the 'tcalc' function is not of type *int*.
    The following elements are not of type *int*:
    -  2.0 is *float*

    """
    if all(isinstance(item, expected_type) for item in my_list) is False:
        try:
            error_type = expected_type.__name__.capitalize()
            raise TypeError(f"Not{error_type}Error")
        except TypeError:
            print(
                f"At least one element in parameter '{param_name}' of the '{func_name}' function is not of type *{expected_type.__name__}*."
            )
            print(f"The following elements are not of type *{expected_type.__name__}*:")
            for element in my_list:
                if not isinstance(element, expected_type):
                    print("- ", element, "is", f"*{type(element).__name__}*")
            print("\n")
            raise
    return True


def is_list(value, param_name, func_name):
    """This function checks whether a variable *value* is of the *list* type.

    Parameters
    ----------
    value : any type
        The variable that is tested as being of *list* type;
    param_name : str
        The name of the parameter that received the variable *value*';
    func_name : str
        The name of the function that utilizes the parameter *param_name*;

    Returns
    -------
    True
        If variable *value* **IS** of the *list* type;
    TypeError
        If variable *value* is **NOT** of the *list* type;


    Examples
    --------
    >>> from paramcheckup import types
    >>> data = [1, 2, 3, 4]
    >>> print(types.is_list(data, "data", "ttest"))
    True


    >>> from paramcheckup import types
    >>> data = (1, 2, 3, 4)
    >>> types.is_list(data, "data", "ttest")
    The parameter 'data' in function 'ttest' must be of type *list*, but its type is *tuple*.

    """
    if isinstance(value, list) is False:
        try:
            raise TypeError("NotListError")
        except TypeError:
            print(
                f"The parameter '{param_name}' in function '{func_name}' must be of type *list*, but its type is *{type(value).__name__}*.\n"
            )
            raise
    return True


def is_numpy(value, param_name, func_name):
    """This function checks whether a variable *value* is of the :doc:`numpy array <numpy:reference/generated/numpy.array>` type.

    Parameters
    ----------
    value : any
        The variable that is tested as being of :doc:`numpy array <numpy:reference/generated/numpy.array>` type;
    param_name : str
        The name of the parameter that received the variable *value*';
    func_name : str
        The name of the function that utilizes the parameter *param_name*;

    Returns
    -------
    True
        If variable *value* **IS** of the :doc:`numpy array <numpy:reference/generated/numpy.array>` type;
    TypeError
        If variable *value* is **NOT** of the :doc:`numpy array <numpy:reference/generated/numpy.array>` type;


    Examples
    --------
    >>> from paramcheckup import types
    >>> import numpy as np
    >>> data = np.array([1, 2, 3, 4, 5])
    >>> print(types.is_numpy(data, "data", "ttest"))
    True


    >>> from paramcheckup import types
    >>> import numpy as np
    >>> data = [1, 2, 3, 4, 5]
    >>> types.is_numpy(data, "data", "ttest")
    The parameter 'data' in function 'ttest' must be of type *numpy.ndarray*, but its type is *list*.

    """
    if isinstance(value, np.ndarray) is False:
        try:
            raise TypeError("NotNumPyError")
        except TypeError:
            print(
                f"The parameter '{param_name}' in function '{func_name}' must be of type *numpy.ndarray*, but its type is *{type(value).__name__}*.\n"
            )
            raise

    return True


def is_str(value, param_name, func_name):
    """This function checks whether a variable *value* is of the *str* type.

    Parameters
    ----------
    value : any type
        The variable that is tested as being of *str* type;
    param_name : str
        The name of the parameter that received the variable *value*';
    func_name : str
        The name of the function that utilizes the parameter *param_name*;

    Returns
    -------
    True
        If variable *value* **IS** of the *str* type;
    TypeError
        If variable *value* is **NOT** of the *str* type;


    Examples
    --------
    >>> from paramcheckup import types
    >>> my_str = "hello darkness my old friend..."
    >>> print(types.is_str(my_str, "param", "my_func"))
    True


    >>> from paramcheckup import types
    >>> my_str = 0
    >>> types.is_str(my_str, "param", "my_func")
    The parameter 'param' in function 'my_func' must be of type *str*, but its type is *int*.

    """
    if isinstance(value, str) is False:
        try:
            raise TypeError("NotStrError")
        except TypeError:
            print(
                f"The parameter '{param_name}' in function '{func_name}' must be of type *str*, but its type is *{type(value).__name__}*.\n"
            )
            raise
    return True


def is_subplots(value, param_name, func_name):
    """This function checks whether a variable *value* is of the *matplotlib.axes.SubplotBase* type.

    Parameters
    ----------
    value : any type
        The variable that is tested as being of *matplotlib.axes.SubplotBase* type;
    param_name : str
        The name of the parameter that received the variable *value*';
    func_name : str
        The name of the function that utilizes the parameter *param_name*;

    Returns
    -------
    True
        If variable *value* **IS** of the *matplotlib.axes.SubplotBase* type;
    TypeError
        If variable *value* is **NOT** of the *matplotlib.axes.SubplotBase* type;

    Examples
    --------
    >>> from paramcheckup import types
    >>> import matplotlib.pyplot as plt
    >>> fig, ax = plt.subplots()
    >>> print(types.is_subplots(ax, "axes", "ploting_func"))
    True
    >>> plt.close()


    >>> from paramcheckup import types
    >>> import matplotlib.pyplot as plt
    >>> fig, ax = plt.subplots()
    >>> types.is_subplots(fig, "axes", "ploting_func")
    The parameter 'axes' in function 'ploting_func' must be of type *matplotlib.axes.SubplotBase*, but its type is *Figure*.

    """
    if isinstance(value, SubplotBase) is False:
        try:
            raise TypeError("NotSubplotError")
        except TypeError:
            print(
                f"The parameter '{param_name}' in function '{func_name}' must be of type *matplotlib.axes.SubplotBase*, but its type is *{type(value).__name__}*.\n"
            )
            raise
    return True


def is_tuple(value, param_name, func_name):
    """This function checks whether a variable *value* is of the *tuple* type.

    Parameters
    ----------
    value : any type
        The variable that is tested as being of *tuple* type;
    param_name : str
        The name of the parameter that received the variable *value*';
    func_name : str
        The name of the function that utilizes the parameter *param_name*;

    Returns
    -------
    True
        If variable *value* **IS** of the *tuple* type;
    TypeError
        If variable *value* is **NOT** of the *tuple* type;


    Examples
    --------
    >>> from paramcheckup import types
    >>> data = (1, 2, 3, 4)
    >>> print(types.is_tuple(data, "data", "ttest"))
    True


    >>> from paramcheckup import types
    >>> data = [1, 2, 3, 4]
    >>> types.is_tuple(data, "data", "ttest")
    The parameter 'data' in function 'ttest' must be of type *tuple*, but its type is *tuple*.

    """
    if isinstance(value, tuple) is False:
        try:
            raise TypeError("NotTupleError")
        except TypeError:
            print(
                f"The parameter '{param_name}' in function '{func_name}' must be of type *tuple*, but its type is *{type(value).__name__}*.\n"
            )
            raise
    return True
