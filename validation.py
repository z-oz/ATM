import sys

def validate(item, mini, maxi, inclusive_min=True, inclusive_max=True):
    """FUNCTION: Returns True if within the valid range, False otherwise. This
        was intended for numeric data, but it could potentially work for other
        data types.

    >> validate(item, mini, maxi, inclusive_min=True,
        inclusive_max=True)

    PARAMETERS
        @item: The input to validate.
        @mini: The lower bound.
        @maxi: The upper bound.
        @inclusive_min: Inclusive lower bound if True, exclusive if False.
        @inclusive_max: Inclusive upper bound if True, exclusive if False.

    RETURN
        True if contained within the valid range, False otherwise.
    """

    if (not isinstance(inclusive_min, bool)) or \
       (not isinstance(inclusive_min, bool)):
        raise ValueError("ERROR: Invalid Boolean argument.")

    min_valid = True
    max_valid = True

    if (inclusive_min and item < mini) or \
       (not inclusive_min and item <= mini):
        min_valid = False

    if (inclusive_max and item > maxi) or \
       (not inclusive_max and item >= maxi):
        max_valid = False

    return min_valid and max_valid


def get_integer(prompt, mini, maxi, inclusive_min=True, inclusive_max=True):
    """FUNCTION: Extract an integer and validate it within the parameterized
        range.

    >> get_integer(prompt, mini, maxi, inclusive_min=True, inclusive_max=True)

    PARAMETERS
        @prompt: The prompt for user input.
        @mini: The lower bound.
        @maxi: The upper bound.
        @inclusive_min: Inclusive lower bound if True, exclusive if False.
        @inclusive_max: Inclusive upper bound if True, exclusive if False.

    RETURN
        The validated integer.
    """

    valid = False

    while not valid:
        try:
            integer = int(input(prompt))
            valid = validate(integer, mini, maxi,
                             inclusive_min, inclusive_max)
        except Exception as e:
            sys.stderr.write("ERROR: " + str(e) + ".\n")

    return integer
