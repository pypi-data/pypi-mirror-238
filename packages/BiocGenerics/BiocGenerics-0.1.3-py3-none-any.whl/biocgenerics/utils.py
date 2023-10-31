__author__ = "jkanche, keviny2"
__copyright__ = "jkanche"
__license__ = "MIT"


def _convert_1d_sparse_to_dense(x):
    """Convert 1-dimensional sparse vector to a :py:class:`~numpy.ndarray`.

    Args:
        x: A sparse 1-d array

    Returns:
        ndarray: A numpy ndarray.
    """
    elem = x.todense()

    if elem.shape[0] == 1:
        elem = elem[0]

    return elem


def _convert_sparse_to_dense(x):
    """Convert sparse vector to a :py:class:`~numpy.ndarray`.

    Args:
        x: A sparse 1-d array

    Returns:
        ndarray: A numpy ndarray.
    """
    return x.todense()


def _is_1d_dense_arrays(x) -> bool:
    """Check if all elements in x are 1-dimensional dense arrays.

    Args:
        x: A list of numpy arrays.

    Returns:
        bool: True if all elements are 1d, otherwise False.
    """
    return all(len(y.shape) == 1 for y in x)


def _is_1d_sparse_arrays(x) -> bool:
    """Check if all elements in x are 1-dimensional sparse arrays.

    Args:
        x: A list of scipy arrays.

    Returns:
        bool: True if all elements are 1d, otherwise False.
    """
    return all(y.shape[0] == 1 for y in x)


def _do_arrays_match(x, dim: int) -> bool:
    """Check if all arrays match the nth dimension specified by ``dim``.

    Args:
        x: A list of arrays.
        dim (int): Dimension to check.

    Returns:
        bool: True if all arrays match the nth dimension.
    """
    all_shapes = [y.shape[dim] for y in x]

    first = all_shapes[0]
    return all(y == first for y in all_shapes)


def _is_any_element_list(x, target_type) -> bool:
    """Check if ``x`` is a list and any of the elements are of the ``target_type``.

    Args:
        x: A list of objects.
        target_type: Target type to check

    Returns:
        bool: True if any element in x is the expected type.
    """
    return isinstance(x, (list, tuple)) and any(
        isinstance(item, target_type) for item in x
    )
