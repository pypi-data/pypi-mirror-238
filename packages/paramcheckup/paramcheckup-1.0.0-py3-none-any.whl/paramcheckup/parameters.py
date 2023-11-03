"""
##### List of functions (alphabetical order) #####

## Functions WITH TESTS ###
param_options(option, param_options, param_name, func_name)




## Functions WITH some TESTS (needs improvements) ###


## Functions WITHOUT tests ###



##### List of CLASS (alphabetical order) #####







Author: Anderson Marcos Dias Canteli <andersonmdcanteli@gmail.com>

Created: October 28, 2023.

Last update: October 28, 2023



"""

##### IMPORTS #####

### Standard ###

### Third part ###

### home made ###


##### CONSTANTS #####


##### CLASSES #####

##### FUNCTIONS #####


def param_options(option, param_options, param_name, func_name):
    """This function checks whether a *option* is a valid *param_options*.

    Parameters
    ----------
    option : any
        The parameter option to be evaluated;
    param_options : list
        A list with all the possible values for the *param_name* function;
    param_name : str
        The name of the parameter that received the variable *option*';
    func_name : str
        The name of the function that utilizes the parameter *param_name*;

    Returns
    -------
    output : True
        If *option* **IS** in *param_options*;
    raises : ValueError
        If *option* is **NOT** in *param_options*;


    Examples
    --------
    >>> from paramcheckup import parameters
    >>> options = ["tukey", "fisher", "dunett"]
    >>> param = "tukey"
    >>> result = parameters.param_options(param, options, "test", "mean_comparison")
    >>> print(result)
    True


    >>> from paramcheckup import parameters
    >>> options = ["tukey", "fisher", "dunett"]
    >>> param = "bonferroni"
    >>> result = parameters.param_options(param, options, "test", "mean_comparison")
    The option 'bonferroni' is not a valid option for the parameter 'test' in function 'mean_comparison'.
    Only the following options are accepted:
    --> tukey
    --> fisher
    --> dunett

    """
    if option not in param_options:
        try:
            raise ValueError("OptionNotFoundError")
        except ValueError:
            print(
                f"The option '{option}' is not a valid option for the parameter '{param_name}' in function '{func_name}'."
            )
            print("Only the following options are accepted:")
            for p_value in param_options:
                print(f"--> {p_value}")
            print("\n")
            raise
    return True
