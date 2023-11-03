"""
##### List of functions (alphabetical order) #####

## Functions WITH TESTS ###
- is_between_a_and_b(value, a, b, param_name, func_name, inclusive=True)
- is_float_or_int(value, param_name, func_name)
- is_greater_than(value, lower, param_name, func_name, inclusive=True)
- is_lower_than(value, upper, param_name, func_name, inclusive=True)
- is_positive(value, param_name, func_name)
- is_negative(value, param_name, func_name)



## Functions WITH some TESTS (needs improvements) ###


## Functions WITHOUT tests ###



##### List of CLASS (alphabetical order) #####







Author: Anderson Marcos Dias Canteli <andersonmdcanteli@gmail.com>

Created: October 24, 2023.

Last update: October 25, 2023



"""

##### IMPORTS #####

### Standard ###


### Third part ###
import numpy as np

### home made ###


##### CONSTANTS #####


##### CLASSES #####


##### FUNCTIONS #####
def is_between_a_and_b(value, a, b, param_name, func_name, inclusive=True):
    """This function checks whether a number (*value*) is within the range (open or closed) *a* and *b*.

    Parameters
    ----------
    value : int or float
        The number that needs to be checked;
    a : int or float
        The lower bound
    b : int or float
        The upper bound
    param_name : str
        The name of the parameter that received the variable *value*';
    func_name : str
        The name of the function that utilizes the parameter *param_name*;
    inclusive : bool, optional
        Specify whether the boundaries should be open (*False*) or closed (*True*, default);


    Notes
    -----
    If *a* is greater than *b*, the function automatically inverts the values.


    Returns
    -------
    output : True
        If value **IN** [a;b] (or (a;b)) interval;
    raises : ValueError
        If value **NOT** in [a;b] (or (a;b)) interval;

    Examples
    --------
    >>> from paramcheckup import numbers
    >>> alpha = 0.0
    >>> lower = 0
    >>> upper = 1
    >>> result = numbers.is_between_a_and_b(alpha, lower, upper, "alpha", "ttest")
    >>> print(result)
    True

    >>> from paramcheckup import numbers
    >>> alpha = -0.35
    >>> lower = 0
    >>> upper = 1
    >>> result = numbers.is_between_a_and_b(alpha, lower, upper, "alpha", "ttest")
    The value of parameter 'alpha' in function 'ttest' must be within the range of 0 <= value <= 1, but it is '-0.35'.

    >>> from paramcheckup import numbers
    >>> alpha = 0.0
    >>> lower = 0
    >>> upper = 1
    >>> result = numbers.is_between_a_and_b(alpha, lower, upper, "alpha", "ttest", inclusive=False)
    The value of parameter 'alpha' in function 'ttest' must be within the range of 0 < value < 1, but it is '0.0'.

    """
    values = [a, b]
    lower = min(values)
    upper = max(values)

    if inclusive is True:
        if (lower <= value <= upper) is False:
            try:
                raise ValueError("OutofBoundsError")
            except ValueError:
                print(
                    f"The value of parameter '{param_name}' in function '{func_name}' must be within the range of {lower} <= value <= {upper}, but it is '{value}'.\n"
                )
                raise
    else:
        if (lower < value < upper) is False:
            try:
                raise ValueError("OutofBoundsError")
            except ValueError:
                print(
                    f"The value of parameter '{param_name}' in function '{func_name}' must be within the range of {lower} < value < {upper}, but it is '{value}'.\n"
                )
                raise
    return True


def is_greater_than(value, lower, param_name, func_name, inclusive=True):
    """This function checks if a *value* is equal or higher than *lower*.

    Parameters
    ----------
    value : int or float
        The number that needs to be checked;
    lower : int or float
        The lower bound
    param_name : str
        The name of the parameter that received the variable *value*';
    func_name : str
        The name of the function that utilizes the parameter *param_name*;
    inclusive : bool, optional
        Specify whether the boundaries should be open (*False*) or closed (*True*, default);

    Returns
    -------
    output : True
        If value > lower (or value >= lower);
    raises : ValueError
        If value <= lower (or value < lower);

    Examples
    --------
    >>> from paramcheckup import numbers
    >>> alpha = 0.05
    >>> lower = 0
    >>> result = numbers.is_greater_than(alpha, lower, "alpha", "ttest", inclusive=True)
    >>> print(result)
    True

    >>> from paramcheckup import numbers
    >>> alpha = -0.05
    >>> lower = 0
    >>> result = numbers.is_greater_than(alpha, lower, "alpha", "ttest", inclusive=True)
    The value of the parameter 'alpha' in function 'ttest' must be equal or greater than '0', but it is '-0.05'.


    >>> from paramcheckup import numbers
    >>> alpha = 0.0
    >>> lower = 0
    >>> result = numbers.is_greater_than(alpha, lower, "alpha", "ttest", inclusive=False)
    >>> print(result)
    True

    >>> from paramcheckup import numbers
    >>> alpha = -0.05
    >>> lower = 0
    >>> result = numbers.is_greater_than(alpha, lower, "alpha", "ttest", inclusive=False)
    The value of the parameter 'alpha' in function 'ttest' must be greater than '0', but it is '-0.05'.
    """

    if inclusive:
        if value <= lower:
            try:
                raise ValueError("OutofBoundsError")
            except ValueError:
                print(
                    f"The value of the parameter '{param_name}' in function '{func_name}' must be equal or greater than '{lower}', but it is '{value}'.\n"
                )
                raise
    else:
        if value < lower:
            try:
                raise ValueError("OutofBoundsError")
            except ValueError:
                print(
                    f"The value of the parameter '{param_name}' in function '{func_name}' must be greater than '{lower}', but it is '{value}'.\n"
                )
                raise
    return True


def is_lower_than(value, upper, param_name, func_name, inclusive=True):
    """This function checks if a *value* is equal or lower than *upper*.

    Parameters
    ----------
    value : int or float
        The number that needs to be checked;
    upper : int or float
        The upper bound
    param_name : str
        The name of the parameter that received the variable *value*';
    func_name : str
        The name of the function that utilizes the parameter *param_name*;
    inclusive : bool, optional
        Specify whether the boundaries should be open (*False*) or closed (*True*, default);

    Returns
    -------
    output : True
        If value < upper (or value <= upper);
    raises : ValueError
        If value >= upper (or value > upper);

    Examples
    --------
    >>> from paramcheckup import numbers
    >>> alpha = 0.05
    >>> upper = 1
    >>> result = numbers.is_lower_than(alpha, upper, "alpha", "ttest", inclusive=True)
    >>> print(result)
    True

    >>> from paramcheckup import numbers
    >>> alpha = 1.05
    >>> upper = 1
    >>> result = numbers.is_lower_than(alpha, upper, "alpha", "ttest", inclusive=True)
    The value of the parameter 'alpha' in function 'ttest' must be equal or lower than '1', but it is '1.05'.

    >>> from paramcheckup import numbers
    >>> alpha = 0.
    >>> upper = 0
    >>> result = numbers.is_lower_than(alpha, upper, "alpha", "ttest", inclusive=False)
    >>> print(result)
    True

    >>> from paramcheckup import numbers
    >>> alpha = 0.05
    >>> upper = 0
    >>> result = numbers.is_lower_than(alpha, upper, "alpha", "ttest", inclusive=False)
    The value of the parameter 'alpha' in function 'ttest' must be lower than '0', but it is '0.05'.
    """
    if inclusive:
        if value >= upper:
            try:
                raise ValueError("OutofBoundsError")
            except ValueError:
                print(
                    f"The value of the parameter '{param_name}' in function '{func_name}' must be equal or lower than '{upper}', but it is '{value}'.\n"
                )
                raise
    else:
        if value > upper:
            try:
                raise ValueError("OutofBoundsError")
            except ValueError:
                print(
                    f"The value of the parameter '{param_name}' in function '{func_name}' must be lower than '{upper}', but it is '{value}'.\n"
                )
                raise
    return True


def is_float_or_int(value, param_name, func_name):
    """This function checks whether a variable *value* is of the *int* or *float* type.

    Parameters
    ----------
    value : any type
        The variable that is tested as being of *int* or *float* type;
    param_name : str
        The name of the parameter that received the variable *value*';
    func_name : str
        The name of the function that utilizes the parameter *param_name*;

    Returns
    -------
    True
        If variable *value* **IS** of the *int* or *float* type;
    TypeError
        If variable *value* is **NOT** of the *int* or *float* type;

    Notes
    -----
    The following types are considered to be *True*:

    * *int*;
    * *np.uint*;
    * *np.integer*;
    * *float*;
    * *np.floating*;

    Examples
    --------
    >>> from paramcheckup import numbers
    >>> print(numbers.is_float_or_int(2, param_name="hypotenuse", func_name="pitagoras"))
    True

    >>> from paramcheckup import numbers
    >>> print(numbers.is_float_or_int("2", param_name="hypotenuse", func_name="pitagoras"))
    The parameter 'hypotenuse' in function 'pitagoras' must be of type *int* or *float*, but its type is *str*.
    """
    if isinstance(value, (int, np.uint, np.integer, float, np.floating)) is False:
        try:
            raise TypeError("NotNumberError")
        except TypeError:
            print(
                f"The parameter '{param_name}' in function '{func_name}' must be of type *int* or *float*, but its type is *{type(value).__name__}*.\n"
            )
            raise
    else:
        return True


def is_negative(value, param_name, func_name):
    """This function checks whether a variable *value* is a negative number (lower than zero, not included).

    Parameters
    ----------
    value : int or float
        The number to whether if it is negative;
    param_name : str
        The name of the parameter that received the variable *value*';
    func_name : str
        The name of the function that utilizes the parameter *param_name*;

    Returns
    -------
    True
        If variable *value* **IS** negative;
    ValueError
        If variable *value* is **NOT** negative;

    Examples
    --------
    >>> from paramcheckup import numbers
    >>> value = -10
    >>> print(numbers.is_negative(value, "parameter", "my_func"))
    True

    >>> from paramcheckup import numbers
    >>> value = 10
    >>> numbers.is_negative(value, "parameter", "my_func")
    The parameter 'parameter' in function 'my_func' must be a negative number, but it is equal to '10'.
    """
    if value >= 0:
        try:
            raise ValueError("NotNegativeError")
        except ValueError:
            print(
                f"The parameter '{param_name}' in function '{func_name}' must be a negative number, but it is equal to '{value}'.\n"
            )
            raise
    return True


def is_positive(value, param_name, func_name):
    """This function checks whether a variable *value* is a positive number (greater than zero, not included).

    Parameters
    ----------
    value : int or float
        The number to whether if it is positive;
    param_name : str
        The name of the parameter that received the variable *value*';
    func_name : str
        The name of the function that utilizes the parameter *param_name*;

    Returns
    -------
    True
        If variable *value* **IS** positive;
    ValueError
        If variable *value* is **NOT** positive;

    Examples
    --------
    >>> from paramcheckup import numbers
    >>> c_zero = 10
    >>> print(numbers.is_positive(c_zero, "inlet_concentration", "bed_capacity"))
    True

    >>> from paramcheckup import numbers
    >>> c_zero = -10
    >>> numbers.is_positive(c_zero, "inlet_concentration", "bed_capacity")
    The parameter 'inlet_concentration' in function 'bed_capacity' must be a positive number, but it is equal to '-10'.

    """
    if value <= 0:
        try:
            raise ValueError("NotPositiveError")
        except ValueError:
            print(
                f"The parameter '{param_name}' in function '{func_name}' must be a positive number, but it is equal to '{value}'.\n"
            )
            raise
    return True
