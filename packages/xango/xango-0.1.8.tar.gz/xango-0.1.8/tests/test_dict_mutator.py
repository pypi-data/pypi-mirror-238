import pytest
from xango import lib, dict_mutator

_get = lib.dict_get

def test_mutate_simple_set():
  init_data = {
    "name": "mutate",
    "version": "1.0.2"
  }

  mutations = {
    "version": "2.0.1",
    "location": "CLT"
  }

  d, _ = dict_mutator.mutate(mutations)
  assert d["version"] == "2.0.1"

def test_incr():
  init_data = {
    "counter": 2
  }
  m = {
    "counter:$incr": True
  }

  d, _ = dict_mutator.mutate(mutations=m, init_data=init_data)
  assert d.get("counter") == 3

  m = {
    "counter:$incr": 5
  }
  d, _ = dict_mutator.mutate(mutations=m, init_data=init_data)
  assert d.get("counter") == 7

  m = {
    "counter:$incr": -3
  }
  d, _ = dict_mutator.mutate(mutations=m, init_data=init_data)
  assert d.get("counter") == -1
 

def test_decr():
  init_data = {
    "counter": 2
  }
  m = {
    "counter:$decr": True
  }

  d, _ = dict_mutator.mutate(mutations=m, init_data=init_data)
  assert d.get("counter") == 1

  m = {
    "counter:$decr": 5
  }
  d, _ = dict_mutator.mutate(mutations=m, init_data=init_data)
  assert d.get("counter") == -3

  m = {
    "counter:$decr": -3
  }
  d, _ = dict_mutator.mutate(mutations=m, init_data=init_data)
  assert d.get("counter") == 5


def test_update():
  init_data = {
    "counter": 2,
    "d1": {
      "v1": 1,
      "v2": 2
    }
  }
  m = {
    "d1": {
      "v2": 4,
      "v3": 3
    }
  }

  d, _ = dict_mutator.mutate(mutations=m, init_data=init_data)
  assert d.get("d1").get("v2") == 4
  assert d.get("d1").get("v3") == 3


def test_xlen():
  init_data = {
    "counter": 2,
    "a": [1, 2, 3],
    "d1": {
      "v1": 1,
      "v2": 2,
      "v3": 3
    }
  }
  m = {
    "size:$xlen": "@d1",
  }  
  d, _ = dict_mutator.mutate(mutations=m, init_data=init_data)
  assert _get(d, "size") == 3


def test_copy():
  init_data = {
    "counter": 2,
    "d1": {
      "v1": 1,
      "v2": 2,
      "v3": 3
    }
  }
  m = {
    "copy:$copy": "@d1.v3",
  }  
  d, _ = dict_mutator.mutate(mutations=m, init_data=init_data)
  assert _get(d, "copy") == _get(d, "d1.v3")

def test_rename():
  init_data = {
    "counter": 2,
    "d1": {
      "v1": 1,
      "v2": 2,
      "v3": 3
    }
  }
  m = {
    "counter:$rename": "@newname",
  }  
  d, _ = dict_mutator.mutate(mutations=m, init_data=init_data)
  assert _get(d, "newname") is not None
  # nested
  m = {
    "d1.v1:$rename": "@d1.v0",
  }  
  d, _ = dict_mutator.mutate(mutations=m, init_data=init_data)
  assert _get(d, "d1.v0") is not None

def test_replace():
  init_data = {
    "counter": 2,
    "d1": {
      "v1": 1,
      "v2": 2,
      "v3": 3
    }
  }
  # MUTS3 {'d1.location:$set': 'zoomba'}
  m = {
    "d1:$zset": {
      "location": "zoomba"
    },
  }

  d, _ = dict_mutator.mutate(mutations=m, init_data=init_data)
  print("DSETTTT", d)
  assert d.get("d1").get("location") == "zoomba"

