#-----------------------------
# -- Xango --
#-----------------------------

import re
import copy
import arrow
import uuid
from . import lib, lib_dict, exceptions
from functools import reduce
# ----

# Operators that work with list
LISTTYPES_OPERATORS = ["xadd", "xadd_many", "xrem", "xrem_many", "xpush", "xpush_many", "xpushl", "xpushl_many"]

# _NMutDict: A dict thats aggregates data to be mutated in a nested context
class _NMutDict(dict): pass

# _NMutList: A list of data to be mutatated in a nested context
class _NMutList(list): pass

# _FlattenDictType - Data Type flatten_dict
class _FlattenDictType(dict): pass

# To unset a value from being updated
class _UnOperableValue(object): pass

# MUTS3 {'d1.location:$set': 'zoomba'} 
def mutate(mutations: dict, init_data: dict = {}, immuts:list=[], custom_ops:dict={}):
    """
    mutate

    Args:
        mutations:dict - data contains operators to update
        init_data:dict - initial data 
        immuts: list - list of keys to not mutate
        custom_ops: dict - dict of custom operations

    Returns:
        tuple(updated_data:dict, oplog)

    """
    
    _muts = _flatten_dict(lib.deepcopy(mutations))
    _inits = _flatten_dict(lib.deepcopy(init_data))
    muts = {}

    _restructed = {}
    for k, v in _muts.items():
        # since data is flat, let's restructure some data so they can be properly mutated
        xl = list(filter(lambda v: v, re.split("(\:\$\w+)(?:\.)?", k)))
        if len(xl) > 2:
            _op = xl[1].replace(":$", "")
            if _op in LISTTYPES_OPERATORS:
                _pathkey = "%s:$%s" % (xl[0], _op)
                if _pathkey not in _restructed:
                    _restructed[_pathkey] = _NMutDict()
                _jpath = ".".join(xl[2:]).replace(".:$", ":$")
                _restructed[_pathkey][_jpath] = v
            else:
                muts[k] = _NMutList([_NMutDict(vv) if isinstance(vv, dict) else vv for vv in v]) if isinstance(v, list) else v
        else:
            # by default, data will be a :$set. This will allow inner update
            k = "%s:$set" % k if ":$" not in k else k
            muts[k] = _NMutList([_NMutDict(vv) if isinstance(vv, dict) else vv for vv in v]) if isinstance(v, list) else v

    muts.update(_restructed)
    d, _ = _mutate(mutations=muts, init_data=_inits, immuts=immuts, custom_ops=custom_ops)

    return _unflatten_dict(d), _


def _mutate(mutations:_FlattenDictType, init_data:_FlattenDictType={}, immuts:list=[], custom_ops:dict={}):
    """
    Mutation operations

    Args:
        mutations:dict - data contains operators to update
        init_data:dict - initial data 
        immuts: list - list of keys to not mutate
        custom_ops: dict - dict of custom operations

    Returns:
        tuple(updated_data:_FlattenDictType, oplog)

    Operators:
        $set - to set a literal k/v
        $incr - to increase an INT value
        $decr - to decrease an INT value
        $unset - To remove a property
        $rename - To rename a property
        $copy - To copy the value of property to another one
        $datetime - gen the current datetime. Can manipulate time
        $template - Evalute the string as template
        $uuid4 - gen a UUID4 string, with the dashes
        $xadd - add item if doesn't exist
        $xadd_many - add many items in the list if not already in the list
        $xrem - remove item
        $xrem_many - remove many items in a list
        $xpush - push item on the right
        $xpush_many - push many items in a list on the right
        $xpushl - push item on the left
        $xpushl_many - push many items in a list on the left
        $xpop - pop an item from a list on the right 
        $xpopl - pop an item from a list on the left
        $xlen - calculate the length of an object
        
    Example
        {
           "key:$incr": True|1|Num,
           "key:$decr": True|1|Num,
           "some.key:$unset": True,
           "old.key:$rename: "@new_path",
           "some.key:$copy: "@new_path",
           "some.list:$xadd": Any,
           "some.list:$xadd_many": [Any, Any, Any, ...],
           "some.list:$xrem": Any,
           "some.list:$xrem_many": [Any, Any, Any, ...],     
           "some.list:$xpush": Any,
           "some.list:$xpush_many": [Any, Any, Any, ...],   
           "some.list:$xpushl": Any,
           "some.list:$xpushl_many": [Any, Any, Any, ...],    
           "some.list:$xpop": True,
           "some.list:$xpopl: False,
           "some.value:$xlen": "@some.data.path",
           "some.datetimefield:$datetime": True,             
           "some.datetimefield:$datetime": "+1Day +2Hours 5Minutes",
           "some.key:$template": "Hello {{ name }}!",
           "some.random.id:$uuid4": True,
        }

    Custom operations
        Extends the dict mutator with custom operations 

        It's K/V pair with key being the name of the operation and value a callable with
            def name(data, path, value)
        

        ie:
            def _new_uuid4(data, path, value):
                return str(uuid.uuid4()).replace("-")

            custom_ops = { 
                "new_uuid4": _new_uuid4
            }

            ops = {
                "new_uid:$new_uuid4": True
            }    
    """
    data = init_data
    oplog = {}
    postproc = {}
    replace_set = {}

    # disabled immuts
    immuts = []
    
    for path, value in mutations.items():

        # -- skip
        if immuts and path in immuts:
            continue 

        if ":" in path:
            # -- skip
            if ":$" not in path:
                continue
            
            if isinstance(value, dict):
                value = _mutate(value)[0]

            if isinstance(value, list):
                value = [ _mutate(vv)[0] if isinstance(vv, dict) else vv for vv in value]

            oppath = path
            oplog_path = path
            path, op = path.split(":$")

            
            # -- skip
            if immuts and path in immuts:
                continue 
            
            # post-process data. To be parsed later
            if op in ["template", "xlen", "rename", "copy"]:
                postproc[oppath] = value 
                continue 

            # $set. literal assigment, leave as is 
            if op == "set":
                pass

            # $incr
            elif op == "incr":
                value = _get_int_data(data, path) + \
                    (value if isinstance(value, int) else 1)
                oplog[oplog_path] = value

            # $decr
            elif op == "decr":
                _ = (value if isinstance(value, int) else 1) * -1
                value = _get_int_data(data, path) + _
                oplog[oplog_path] = value

            # $unset
            elif op == "unset":
                v = _pop(data, path)
                oplog[oplog_path] = v
                value = _UnOperableValue()


            # $datetime 
            elif op in ["datetime", "timestamp", "currdate"]:
                
                dt = _get_datetime()
                if value is True:
                    value = dt
                else:
                    try:
                        if isinstance(value, str):
                            value = _arrow_date_shifter(dt=dt, stmt=value)
                        else:
                            value = _UnOperableValue()
                    except:
                        value = _UnOperableValue()

            # $uuid4
            elif op == "uuid4":
                value = str(uuid.uuid4()) #.replace("-", "")


            # LIST operators

            elif op in (
                "xadd", "xadd_many",
                "xrem", "xrem_many",
                "xpush", "xpush_many",
                "xpushl", "xpushl_many"
            ):
                values = _values_to_mlist(value, many=op.endswith("_many"))
                v = _get_list_data(data, path)

                # $xadd|$xadd_many
                if op.startswith("xadd"):
                    for val in values:
                        if val not in v:
                            v.append(val)
                    value = v

                # $xrem|$xrem_many
                elif op.startswith("xrem"):
                    _removed = False
                    for val in values:
                        if val in v:
                            _removed = True
                            v.remove(val)
                    value = v
                    if not _removed:
                        value = _UnOperableValue()

                # $xpush|$xpush_many
                elif op in ("xpush", "xpush_many"):
                    v.extend(values)
                    value = v

                # $xpushl|$xpushl_many
                elif op in ("xpushl", "xpushl_many"):
                    v2 = list(values)
                    v2.extend(v)
                    value = v2

            # $xpop
            elif op == "xpop":
                v = _get_list_data(data, path)
                if len(v):
                    value = v[:-1]
                    oplog[oplog_path] = v[-1]

            # $xpopl
            elif op == "xpopl":
                v = _get_list_data(data, path)
                if len(v):
                    value = v[1:]
                    oplog[oplog_path] = v[0]

            # $$custom_ops, add to post process
            elif op in custom_ops:
                postproc[oppath] = value 
                continue 

            # _UnOperableValue
            else:
                value = _UnOperableValue()

        if not isinstance(value, _UnOperableValue):
            data[path] = value

    # Post process
    if postproc:
        for path, value in postproc.items():            
            try:
                if ":" in path:
                    # -- skip
                    if ":$" not in path:
                        continue

                    path, op = path.split(":$")

                    # -- skip
                    if path in immuts:
                        continue 

                    # $template
                    if op == "template": 
                        _tpl_data =  {
                            **data,
                            "TIMESTAMP": _j2_currdate,
                            "DATETIME": _j2_currdate
                        }              
                        data[path] = lib.render_template(source=value, data=_tpl_data, is_data_flatten=True)
                    
                    # $xlen, requires @ref
                    elif op == "xlen" and _is_value_at_ref(value):
                        value = _clean_value_ref(value)
                        try:
                            v = _lookup_flat_data(data, value)
                            data[path] = len(v) if v else 0
                        except:
                            data[path] = 0

                    # $rename, requires @ref
                    elif op == "rename" and _is_value_at_ref(value):
                        value = _clean_value_ref(value)
                        data[value] = _pop(data, path)

                    # $copy, requires @ref
                    elif op == "copy" and _is_value_at_ref(value):
                        data[path] = _get(data, _clean_value_ref(value))

                    # custom ops
                    elif op in custom_ops:
                        data[path] = custom_ops[op](data, path, value)

            except:
                pass


    return data, oplog


_arrow_date_shifter = lib.arrow_date_shifter

def _get(data:dict, path):
    """
    _get: Alias to get data from a path
    """
    return lib.dict_get(obj=data, path=path)

def _set(data:dict, path, value):
    """
    _set: Alias to set value in data
    """
    lib.dict_set(data, path, value)
    return data

def _pop(data, path):
    """
    _pop: Alias to remove object from data
    """
    if path in data:
        return data.pop(path)
    return None 

def _get_int_data(data: dict, path: str) -> int:
    """
    _get_int_data: Returns INT for number type operations
    """
    v = _get(data, path)
    if v is None:
        v = 0
    if not isinstance(v, int):
        raise TypeError("Invalid data type for '%s'. Must be 'int' " % path)
    return v

def _get_list_data(data: dict, path: str) -> list:
    """
    _get_list_data: Returns a data LIST, for list types operations
    """
    v = _get(data, path)
    if v is None:
        return []
    if not isinstance(v, list):
        raise TypeError("Invalid data type for '%s'. Must be 'list' " % path)
    return v

def _values_to_mlist(value, many=False) -> list:
    """
    _values_to_mlist: Convert data multiple list items
    """
    return [value] if many is False else value if isinstance(value, (list, tuple)) else [value]

def _get_datetime() -> arrow.Arrow:
    """
    Generates the current UTC datetime with Arrow date

    ISO FORMAT
    Date    2022-08-13
    Date and time in UTC : 2022-08-13T22:45:03+00:00

    Returns:
      Arrow UTC Now
    """
    return arrow.utcnow()

def _j2_currdate(format_="ISO_DATETIME", shifter=None):
    dt = _get_datetime()
    if shifter:
        dt = _arrow_date_shifter(dt=dt, stmt=shifter)
    return lib.arrow_date_format(dt, format_)

def _lookup_flat_data(d_flatten, key):
    return lib.dict_get(obj=_unflatten_dict(d_flatten), path=key)

def _is_value_at_ref(value) -> bool:
    return value and isinstance(value, str) and value.startswith("@")

def _clean_value_ref(value) -> str:
    return value.replace("@", "")

def _flatten_dict(_dict: dict, _str: str = '', reducer=None) -> dict:
    """
    To flatten a dict. Nested node will be separated by dot or separator
    It takes in consideration dict in list and flat them.
    Non dict stay as is

    Args:
        ddict:
        prefix:
    Returns:
        dict

    """
    sep = "."
    ret_dict = {}
    for k, v in _dict.items():
        if isinstance(v, dict):
            ret_dict.update(_flatten_dict(v, _str=sep.join([_str, k]).strip(sep)))
        elif isinstance(v, list):
            _k =  ("%s.%s" % (_str, k)).strip(sep)
            ret_dict[_k] = [_flatten_dict(item) if isinstance(item, dict) else item for item in v]
        else:
            ret_dict[sep.join([_str, k]).strip(sep)] = v
    return ret_dict

def _unflatten_dict(flatten_dict: dict) -> dict:
    """
    To un-flatten a flatten dict

    Args:
      flatten_dict: A flatten dict
    Returns:
      an unflatten dictionnary
    """

    output = {}
    for k, v in flatten_dict.items():
        path = k.split(".")
        if isinstance(v, list):
            v = [_unflatten_dict(i2) if isinstance(i2, dict) else i2 for i2 in v]
        _set_nested(output, path, v, k)
    return output

def _set_nested(d, path, value, full_path=None):
    try:
        _get_nested_default(d, path[:-1])[path[-1]] = value        
    except (AttributeError, TypeError) as e:
        raise exceptions.MutationTypeError("MutationTypeError: %s at '%s'" % (e, full_path))

def _get_nested_default(d, path):
    return reduce(lambda d, k: d.setdefault(k, {}), path, d)

