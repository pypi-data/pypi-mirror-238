"""
lib_dict

A universal library that deals with dict 

"""

import pickle
from functools import reduce
from typing import Any, Dict
from operator import itemgetter
import hashlib
import json 



def deepcopy(obj:any) -> any:
    """
    A faster deepcopy using pickle
    """
    return pickle.loads(pickle.dumps(obj, -1))


def flatten_dict(ddict: dict, prefix='') -> dict:
    """
    @deprecated
    @use flatten
    """
    return flatten(ddict)


def unflatten_dict(flatten_dict: dict) -> dict:
    """
    @deprecated
    @use unflatten
    """
    return unflatten(flatten_dict)


def dict_pick(ddict: dict, keys: list, check_keys=False) -> dict:
    """
    To pick and return specific keys from a flatten dict.

    Args:
      ddict: dict
      keys: A list of dot notation path to keep
      check_keys: bool - check if all keys exist

    Returns:
      a dict with the picked value

    Example
      keys: ["name", "location.city"]
      flatten_dict: { "name": "MM", "location.city": "Charlotte",
          "location.state": "NC", "age": 100}
      returns: {
        "name": "MM",
        "location": {
          "city": "Charlotte"
        }
      }
    """
    fd = flatten_dict(ddict)

    # check that all keys exist
    if check_keys:
        for k in keys:
            assert k in fd, "missing key '%s'" % k

    ufd = _dict_pick_merge_l2d([_dict_pick_lookup_dict(fd, k) for k in keys])
    return unflatten_dict(ufd)


def _dict_pick_merge_l2d(iter: list):
    """
    Flatten a looked up list of tuples into dict
    Returns dict
    """
    df = {}
    for u in iter:
        if isinstance(u, list):
            for u2 in u:
                df[u2[0]] = u2[1]
    return df


def _dict_pick_lookup_dict(fd, k):
    """
    To lookup a key in a flatten dict 
    If the key is not found directly, it will start from the parent dot

    Returns list of tuples
    """
    if k in fd:
        return [(k, fd[k])]
    p = []
    for dk, dv in fd.items():
        if dk.startswith("%s." % k):
            p.append((dk, dv))
    return p


def dict_find_replace(ddict: dict, kv_repl: dict, is_flatten=False):
    """
    Find/Replace a KV dict in a dict

    Args:
      - ddict
      - kv_repl
      - is_flatten

    Returns
      dict
    """

    fd = flatten_dict(ddict) if not is_flatten else ddict
    for k, v in fd.items():
        if isinstance(v, str) and v in kv_repl:
            fd[k] = kv_repl[v]
        elif isinstance(v, list):
            for l, e in enumerate(v):
                if isinstance(fd[k][l], str) and fd[k][l] in kv_repl:
                    fd[k][l] = kv_repl[fd[k][l]]
                elif isinstance(fd[k][l], dict):
                    fd[k][l] = dict_find_replace(fd[k][l], kv_repl, True)
        elif isinstance(v, dict):
            fd[k] = dict_find_replace(v, kv_repl, True)
    return unflatten_dict(fd)


def dict_set(my_dict, key_string, value):
    """
    dict_set
    Mutable
    """
    here = my_dict
    keys = key_string.split(".")
    for key in keys[:-1]:
        here = here.setdefault(key, {})
    here[keys[-1]] = value


def dict_get(obj, path, default=None):
    """
    Get a value via dot notaion

    Args:
        @obj: Dict
        @attr: String - dot notation path
            object-path: key.value.path
            object-with-array-index: key.0.path.value
    Returns:
        mixed
    """
    def _getattr(obj, path):
        try:
            if isinstance(obj, list) and path.isdigit():
                return obj[int(path)]
            return obj.get(path, default)
        except:
            return default
    return reduce(_getattr, [obj] + path.split('.'))


def dict_merge(base_dct, merge_dct, add_keys=True) -> dict:
    """
    Deep merge two dict

    Args:
        - base_dct: source
        - merge_dct: new dict

    Returns: 
        dict
    """
    rtn_dct = base_dct.copy()
    if add_keys is False:
        merge_dct = {key: merge_dct[key] for key in set(
            rtn_dct).intersection(set(merge_dct))}

    rtn_dct.update({
        key: dict_merge(rtn_dct[key], merge_dct[key], add_keys=add_keys)
        if isinstance(rtn_dct.get(key), dict) and isinstance(merge_dct[key], dict)
        else merge_dct[key]
        for key in merge_dct.keys()
    })
    return rtn_dct


def flatten(input_dict:dict, separator:str='.', prefix='') -> dict:
    """
    !!! USE THIS instead of flatten_dict
    To flatten a dict
    """
    output_dict = {}
    for key, value in input_dict.items():
        if isinstance(value, dict) and value:
            deeper = flatten(value, separator, prefix+key+separator)
            output_dict.update({key2: val2 for key2, val2 in deeper.items()})
        elif isinstance(value, list) and value:
            for index, sublist in enumerate(value, start=0):
                if sublist and isinstance(sublist, dict):
                    deeper = flatten(sublist, separator, prefix+key+separator+str(index)+separator)
                    output_dict.update({key2: val2 for key2, val2 in deeper.items()})
                else:
                    output_dict[prefix+key+separator+str(index)] = sublist
        else:
            output_dict[prefix+key] = value
    return output_dict

def unflatten(field_dict:dict) -> dict:
    """
    !!! USE THIS instead of unflatten_dict

    To unflatten a flatten dict.
    It accepts regular dot notation dict: `key.key2.key3`
    And list dot notation -> key.0.nested
    or list bracket -> key[0].nested

    Examples
    input_dict = {'a[0]': 1,
                  'a[1]': 10,
                  'a[2]': 5,
                  'b': 10,
                  'c.test.0': "hi",
                  'c.test.1': "bye",
                  "c.head.shoulders": "richard",
                  "c.head.knees": 'toes',
                  "z.trick.or[0]": "treat",
                  "z.trick.or[1]": "halloween",
                  "z.trick.and.then[0]": "he",
                  "z.trick.and.then[1]": "it",
                  "some[0].nested.field[0]": 42,
                  "some[0].nested.field[1]": 43,
                  "some[2].nested.field[0]": 44,
                  "mixed": {
                      "statement": "test",
                      "break[0]": True,
                      "break[1]": False,
                  }}

        expected_dict = {'a': [1, 10, 5],
                     'b': 10,
                     'c': {
                         'test': ['hi', 'bye'],
                         'head': {
                             'shoulders': 'richard',
                             'knees' : 'toes'
                         }
                     },
                     'z': {
                         'trick': {
                             'or': ["treat", "halloween"],
                             'and': {
                                 'then': ["he", "it"]
                             }
                         }
                     },
                     'some': {
                         0: {
                             'nested': {
                                 'field': [42, 43]
                             }
                         },
                         2: {
                             'nested': {
                                 'field': [44]
                             }
                         }
                     },
                     "mixed": {
                         "statement": "test",
                         "break": [True, False]
                     }}
    """
    field_dict = dict(field_dict)
    new_field_dict = dict()
    field_keys = list(field_dict)
    field_keys.sort()

    for each_key in field_keys:
        field_value = field_dict[each_key]
        processed_key = str(each_key)
        current_key = None
        current_subkey = None
        for i in range(len(processed_key)):
            if processed_key[i] == "[":
                current_key = processed_key[:i]
                start_subscript_index = i + 1
                end_subscript_index = processed_key.index("]")
                current_subkey = int(processed_key[start_subscript_index : end_subscript_index])

                # reserve the remainder descendant keys to be processed later in a recursive call
                if len(processed_key[end_subscript_index:]) > 1:
                    current_subkey = "{}.{}".format(current_subkey, processed_key[end_subscript_index + 2:])
                break

            # next child key is a dictionary
            if processed_key[i] == ".":
                split_work = processed_key.split(".", 1)
                if len(split_work) > 1:
                    current_key, current_subkey = split_work
                else:
                    current_key = split_work[0]
                break

        if current_subkey is not None:
            if current_key.isdigit():
                current_key = int(current_key)
            if current_key not in new_field_dict:
                new_field_dict[current_key] = dict()
            new_field_dict[current_key][current_subkey] = field_value
        else:
            new_field_dict[each_key] = field_value

    # Recursively unflatten each dictionary on each depth before returning back to the caller.
    all_digits = True
    highest_digit = -1
    for each_key, each_item in new_field_dict.items():
        if isinstance(each_item, dict):
            new_field_dict[each_key] = unflatten(each_item)

        # validate the keys can safely converted to a sequential list.
        all_digits &= str(each_key).isdigit()
        if all_digits:
            next_digit = int(each_key)
            if next_digit > highest_digit:
                highest_digit = next_digit

    # If all digits and can be sequential order, convert to list.
    if all_digits and highest_digit == (len(new_field_dict) - 1):
        digit_keys = list(new_field_dict)
        digit_keys.sort()
        new_list = []

        for k in digit_keys:
            i = int(k)
            if len(new_list) <= i:
                # Pre-populate missing list elements if the array index keys are out of order
                # and the current element is ahead of the current length boundary.
                while len(new_list) <= i:
                    new_list.append(None)
            new_list[i] = new_field_dict[k]
        new_field_dict = new_list
    return new_field_dict

def get_keys_depth(obj:dict) -> int:
    """
    To calculate the max depth of an object.
    It will get all nested level and return the deepest depth
    Return int
    """
    flattened = flatten(obj)
    return max([len(k.split(".")) for k in flattened.keys()])

def get_keys_count(obj:dict, deep=False) -> int:
    """
    Calculate the 1st level keys of a dict or total count of all keys in a dict when deep=True
    Return int
    """
    if deep:
        flattened = flatten(obj)
        return sum([len(k.split(".")) for k in flattened.keys()])        
    return len(obj)


def upper_keys(obj) -> dict:
    """
    Change all the keys to uppercase in dict
    Args:
        obj: dict
    Returns
        dict

    """
    return { k.upper(): v for k, v in obj }

def list_sorted_dict(l:list, key:str) -> list:
    """
    To order a list of dict, by the value in the dict

    list_sorted_dict(list, "name")
    """
    return sorted(l, key=itemgetter(key))


def get_md5_hash(dictionary: Dict[str, Any]) -> str:
    """ MD5 hash of a dictionary."""
    # We need to sort arguments so {'a': 1, 'b': 2} is
    # the same as {'b': 2, 'a': 1}
    encoded = json.dumps(dictionary, sort_keys=True).encode()
    return hashlib.md5(encoded).hexdigest()


def dict_pop(obj:dict, path:str) -> Any:
    """
    * Mutates #obj

    To pop a property from a dict dotnotation

    Args:
        obj:dict - This object will be mutated
        path:str - the dot notation path to update
        value:Any - value to update with

    Returns:
        Any - The value that was removed
    """

    here = obj 
    keys = path.split(".")

    for key in keys[:-1]:
        here = here.setdefault(key, {})
    if isinstance(here, dict):
        return here.pop(keys[-1])
    else:
        val = here[keys[-1]]
        del here[keys[-1]]
        return val
    

class ddict(dict):
    """
    A Dict class extension to get value with dot notation
    
    Example
        d = {...}
        mydict = ddict(d)
        print(mydict.get("key.deep.path.down"))
    """

    def get(self, path:str, default=None):
        value = dict_get(obj=dict(self), path=path, default=default)
        if isinstance(value, dict):
            return ddict(value)
        return value 

    def set(self, path:str, value):
        dict_set(my_dict=self, key_string=path, value=value)
