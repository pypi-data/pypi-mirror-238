import pydoc
import copy
import datetime
import pickle
import hashlib
from os.path import join
from pathlib import Path

import yaml


def create_object_from_dict(d, **default_kwargs):
    """Create an object from a dictionary.

    Inspired by `iglovikov_helper_functions.config_parsing.utils`. [1]_

    Parameters
    ----------
    d : dict
        Dictionary to create the object from. Must have a key "type" which specifies the class of the object.
        Any additional key-value pairs will be passed to the constructor when creating the object.
    **default_kwargs : additional arguments
        Default parameters to be passed to the constructor, if they do not exist in `d`.

    Returns
    -------
    object
        The initialized object.

    References
    ----------
    .. [1] https://github.com/ternaus/iglovikov_helper_functions/
    """
    if not isinstance(d, dict):
        raise TypeError("'d' should be of type 'dict'.")
    if not 'type' in d:
        raise KeyError("'d' should have a key 'type'.")
    kwargs = d.copy()
    class_type = kwargs.pop('type')
    for name, value in default_kwargs.items():
        kwargs.setdefault(name, value)
    return pydoc.locate(class_type)(**kwargs)


def get_class_from_str(s):
    """Get the uninitialized class `s`.

    Parameters
    ----------
    s : str
        The name of the class.

    Returns
    -------
    class
        The uninitialized class `s`.
    """
    return pydoc.locate(s)


def yield_nested_dict_values(d):
    """Yield (non-dict) values from a nested dict.

    Code from [2]_.

    Parameters
    ----------
    d : dict
        Nested dictionary.

    Returns
    -------
    generator
        Iterator yielding all (non-dict) values from `d` and its child dictionaries.

    References
    ----------
    .. [2] https://tutorial.eyehunts.com/python/python-get-all-values-from-nested-dictionary-example-code/
    """
    for v in d.values():
        if isinstance(v, dict):
            yield from yield_nested_dict_values(v)
        else:
            yield v


def save_pickle(data, path, filename):
    Path(path).mkdir(parents=True, exist_ok=True)
    with open(join(path, filename + '.pickle'), 'wb') as f:
        pickle.dump(data, f)


def save_yaml(data, path, filename, **kwargs):
    Path(path).mkdir(parents=True, exist_ok=True)
    with open(join(path, filename + '.yaml'), 'w') as f:
        yaml.dump(data, f, default_flow_style=False, **kwargs)


def load_yaml(path):
    with open(path) as file:
        yaml_file = yaml.safe_load(file)
    return yaml_file


def seed_hash(*args):
    """Derive an integer hash from `args` to use as a random seed."""
    args_str = str(args)
    return int(hashlib.md5(args_str.encode('utf-8')).hexdigest(), 16) % (2**31)


def create_results_dir_from_config(
    config,
    suffix=None,
    update_config=False
):
    """Create a directory for storing results.

    Parameters
    ----------
    config : dict
        Configuration dictionary. Must have a key 'results' with a key 'path' 
        specifying the path to the results directory.
    suffix : str, optional
        Suffix to append to the results directory name.
    update_config : bool, optional
        Whether to update the configuration dictionary with the new results path.
    """
    time_stamp = datetime.datetime.now().strftime('%Y%m%d_%H%M')
    if suffix is not None:
        time_stamp += '_' + suffix
    results_path = join(config['results']['path'], time_stamp)
    Path(results_path).mkdir(parents=True, exist_ok=True)
    
    if update_config:
        config = copy.deepcopy(config)
        config['results']['path'] = results_path
        return results_path, config
    else:
        return results_path
