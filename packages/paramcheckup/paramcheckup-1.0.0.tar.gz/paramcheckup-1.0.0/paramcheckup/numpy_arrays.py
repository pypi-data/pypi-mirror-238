"""
##### List of functions (alphabetical order) #####

## Functions WITH TESTS ###

- empty_array(arr, param_name, func_name)
- greater_than_n(array, param_name, func_name, minimum=3, inclusive=True)
- matching_size(array_a, param_name_a, array_b, param_name_b, func_name)
- n_dimensions(arr, param_name, func_name, n_dimensions)

## Functions WITH some TESTS (needs improvements) ###
- cast_to_ndim(array, param_name, func_name, ndim=1) (first error does not have a test)

## Functions WITHOUT tests ###



##### List of CLASS (alphabetical order) #####







Author: Anderson Marcos Dias Canteli <andersonmdcanteli@gmail.com>

Created: October 26, 2023.

Last update: October 26, 2023



"""
import numpy as np


def cast_to_ndim(array, param_name, func_name, ndim=1):
    """This function attempts to transform an *array* into a one-dimensional :doc:`numpy array <numpy:reference/generated/numpy.array>`.

    Parameters
    ----------
    array : list, tuple or pd.Series
        The variable that will be converted into a one-dimensional :doc:`numpy array <numpy:reference/generated/numpy.array>`;
    param_name : str
        The name of the parameter that received the variable *array*';
    func_name : str
        The name of the function that utilizes the parameter *param_name*;
    ndim : int, optional
        The number of dimentions thatthe array *arr* must have (default is ``1``);

    Returns
    -------
    array :  :doc:`numpy array <numpy:reference/generated/numpy.array>`
        One dimension :doc:`numpy array <numpy:reference/generated/numpy.array>`;
    raises : ValueError
        If it was not possible to transform *array* A into an :doc:`numpy array <numpy:reference/generated/numpy.array>`;


    Examples
    --------
    >>> from paramcheckup import numpy_arrays
    >>> x_exp = [1, 2, 3, 4]
    >>> x_exp = numpy_arrays.cast_to_ndim(x_exp, "x_exp", "fit", ndim=1)
    >>> print(x_exp)
    [1 2 3 4]

    >>> from paramcheckup import numpy_arrays
    >>> x_exp = 1
    >>> x_exp = numpy_arrays.cast_to_ndim(x_exp, "x_exp", "fit", ndim=1)
    The array generated for the parameter 'x_exp' in function 'fit' contains '0' dimensions, but it must contain '1' dimensions. Please provide a variable with '1' dimensions.
    """
    array = np.asarray(array)
    if isinstance(array, np.ndarray) is False:
        try:
            raise ValueError("CastingError")
        except ValueError:
            print(
                f"Unable to transform parameter '{param_name}' in function '{func_name}' into a NumPyArray satisfactorily.\n"
            )
            raise
    elif array.ndim != ndim:
        try:
            raise ValueError("CastingError")
        except ValueError:
            print(
                f"The array generated for the parameter '{param_name}' in function '{func_name}' contains '{array.ndim}' dimensions, but it must contain '{ndim}' dimensions. Please provide a variable with '{ndim}' dimensions.\n"
            )
            raise
    elif array.size == 0:
        try:
            raise ValueError("CastingError")
        except ValueError:
            print(
                f"The array generated for the parameter '{param_name}' in function '{func_name}' is empty. \n"
            )
            raise
    else:
        return array


def empty_array(arr, param_name, func_name):
    """This function checks whether a :doc:`numpy array <numpy:reference/generated/numpy.array>` is empty.

    Parameters
    ----------
    arr : :doc:`numpy array <numpy:reference/generated/numpy.array>`
        The :doc:`numpy array <numpy:reference/generated/numpy.array>` to check for emptiness;
    param_name : str
        The name of the parameter that received the variable *arr*';
    func_name : str
        The name of the function that utilizes the parameter *param_name*;

    Returns
    -------
    True
        If the array *arr* is **NOT** empty;
    ValueError
        If the array *arr* is **EMPTY**;

    Examples
    --------
    >>> from paramcheckup import numpy_arrays
    >>> import numpy as np
    >>> data = np.array([1, 2, 3, 4, 5])
    >>> print(numpy_arrays.empty_array(data, "param", "ttest"))
    True

    >>> from paramcheckup import numpy_arrays
    >>> import numpy as np
    >>> data = np.array([])
    >>> numpy_arrays.empty_array(data, "param", "ttest")
    The parameter 'param' in function 'ttest' cannot be an empty array.
    """
    if arr.size == 0:
        try:
            raise ValueError("EmptyArrayError")
        except ValueError:
            print(
                f"The parameter '{param_name}' in function '{func_name}' cannot be an empty array.\n"
            )
            raise
    else:
        return True


def greater_than_n(array, param_name, func_name, minimum=3, inclusive=True):
    """This function checks if the size of the :doc:`numpy array <numpy:reference/generated/numpy.array>` *array* is greater than *minimum*.

    Parameters
    ----------
    array :  :doc:`numpy array <numpy:reference/generated/numpy.array>`
        One dimension :doc:`numpy array <numpy:reference/generated/numpy.array>`;
    param_name : str
        The name of the parameter that received the variable *array*';
    func_name : str
        The name of the function that utilizes the parameter *param_name*;
    minimum : int, optional
        The smallest acceptable value for the *array* (default is ``3``);
    inclusive : bool, optional
        Specify whether the *minimum* value should be included (closed range, *True* default) or excluded (open range, *False*);

    Returns
    -------
    output : True
        If the size of the *array* **IS** greater than the *minimum*
    raises : ValueError
        If the size of the *array* is **NOT** greater than the *minimum*

    Examples
    --------
    >>> from paramcheckup import numpy_arrays
    >>> import numpy as np
    >>> x_exp = np.array([1, 2, 3, 4, 4])
    >>> minimum = 5
    >>> output = numpy_arrays.greater_than_n(x_exp, "x_exp", "fit", minimum, inclusive=True)
    >>> print(output)
    True


    >>> from paramcheckup import numpy_arrays
    >>> import numpy as np
    >>> x_exp = np.array([1, 2, 3, 4, 4])
    >>> minimum = 6
    >>> output = numpy_arrays.greater_than_n(x_exp, "x_exp", "fit", minimum, inclusive=True)
    >>> print(output)
    The *array* passed to function 'fit' through parameter 'x_exp' must have a size greater than or equal to '6', but its size is '5'.


    >>> from paramcheckup import numpy_arrays
    >>> import numpy as np
    >>> x_exp = np.array([1, 2, 3, 4, 4])
    >>> minimum = 6
    >>> output = numpy_arrays.greater_than_n(x_exp, "x_exp", "fit", minimum, inclusive=False)
    >>> print(output)
    True


    >>> from paramcheckup import numpy_arrays
    >>> import numpy as np
    >>> x_exp = np.array([1, 2, 3, 4, 4])
    >>> minimum = 5
    >>> numpy_arrays.greater_than_n(x_exp, "x_exp", "fit", minimum, inclusive=False)
    The *array* passed to function 'fit' through parameter 'x_exp' must have a size greater than '5', but its size is '5'.
    """
    if inclusive:
        if array.size < minimum:
            try:
                raise ValueError("SmallSizeError")
            except ValueError:
                print(
                    f"The *array* passed to function '{func_name}' through parameter '{param_name}' must have a size greater than or equal to '{minimum}', but its size is '{array.size}'.\n"
                )
                raise
    else:
        if array.size <= minimum:
            try:
                raise ValueError("SmallSizeError")
            except ValueError:
                print(
                    f"The *array* passed to function '{func_name}' through parameter '{param_name}' must have a size greater than '{minimum}', but its size is '{array.size}'.\n"
                )
                raise
    return True


def matching_size(array_a, param_name_a, array_b, param_name_b, func_name):
    """This function checks whether the size of :doc:`numpy array <numpy:reference/generated/numpy.array>` *array_a* is equal to the size of :doc:`numpy array <numpy:reference/generated/numpy.array>` *array_b*.

    Parameters
    ----------
    array_a :  numpy array
        One dimension :doc:`numpy array <numpy:reference/generated/numpy.array>`;
    param_name_a : str
        The name of the parameter that received the variable *array_a*;
    array_b :  *numpy array*
        One dimension :doc:`numpy array <numpy:reference/generated/numpy.array>`
    param_name_b : str
        The name of the parameter that received the variable *array_b*;
    func_name : str
        The name of the function that utilizes the arrays *param_name_a* and *param_name_b*;


    Returns
    -------
    True
        If the size of the array *array_a* **IS** equal to the size of  the array *array_b*;
    ValueError
        If the size of the array *array_a* is **NOT** equal to the size of  the array *array_b*;

    Examples
    --------
    >>> from paramcheckup import numpy_arrays
    >>> import numpy as np
    >>> x_data = np.array([1, 2, 3, 4, 5, 6])
    >>> y_data = np.array([1, 4, 9, 16, 25, 36])
    >>> print(numpy_arrays.matching_size(x_data, "time", y_data, "concentration", "regression"))
    True


    >>> from paramcheckup import numpy_arrays
    >>> import numpy as np
    >>> x_data = np.array([1, 2, 3, 4, 5, 6])
    >>> y_data = np.array([1, 4, 9, 16, 25,])
    >>> numpy_arrays.matching_size(x_data, "time", y_data, "concentration", "regression")
    The size of the parameter 'time' (6) is different from the size of the parameter 'concentration' (5) in function 'regression', but they must be the same.

    """
    if array_a.size != array_b.size:
        try:
            raise ValueError("SizeMismatchError")
        except ValueError:
            print(
                f"The size of the parameter '{param_name_a}' ({array_a.size}) is different from the size of the parameter '{param_name_b}' ({array_b.size}) in function '{func_name}', but they must be the same.\n"
            )
            raise
    else:
        return True


def n_dimensions(arr, param_name, func_name, n_dimensions):
    """This function checks whether a :doc:`numpy array <numpy:reference/generated/numpy.array>` has *n_dimensions*.

    Parameters
    ----------
    arr : :doc:`numpy array <numpy:reference/generated/numpy.array>`
        The :doc:`numpy array <numpy:reference/generated/numpy.array>` to check the dimensions;
    param_name : str
        The name of the parameter that received the variable *arr*';
    func_name : str
        The name of the function that utilizes the parameter *param_name*;
    n_dimensions : int
        The number of dimentions thatthe array *arr* must have;

    Returns
    -------
    True
        If the array *arr* **has** *n_dimensions*;
    ValueError
        If the array *arr* **does not have** *n_dimensions*;

    Examples
    --------
    >>> from paramcheckup import numpy_arrays
    >>> import numpy as np
    >>> data = np.array([1, 2, 3, 4, 5])
    >>> n_dim = 1
    >>> print(numpy_arrays.n_dimensions(data, "param", "ttest", n_dim))
    True


    >>> from paramcheckup import numpy_arrays
    >>> import numpy as np
    >>> data = np.array([1, 2, 3, 4, 5])
    >>> n_dim = 2
    >>> numpy_arrays.n_dimensions(data, "param", "ttest", n_dim)
    The parameter 'param' of the 'ttest' function must have '2' dimensions, but but it has ndim = '1'.

    """
    if arr.ndim != n_dimensions:
        try:
            raise ValueError("DimensionMismatchError")
        except ValueError:
            print(
                f"The parameter '{param_name}' of the '{func_name}' function must have '{n_dimensions}' dimensions, but but it has ndim = '{arr.ndim}'.\n"
            )
            raise
    return True
