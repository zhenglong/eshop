'''
Created on Apr 19, 2015

@author: tristan
'''

import inspect
from sqlalchemy.orm.collections import InstrumentedList

def obj_map(src, dest, rules=None, mapper=None):
    '''
    dest could be 1) instance => copy the data to dest and return it
                  2) class => create a class instance, copy the data and return it
    rules: conversion rule
    '''
    
    if inspect.isclass(dest):
        target = dest()
    else:
        target = dest
    if hasattr(target, '_sa_instance_state'):
        columns = target._sa_instance_state.attrs._data.keys()
    else:
        columns = target.__dict__.keys()
    src_columns = dir(src)
    if rules is not None:
        src_columns = src_columns + rules.keys()
    for prop_name in src_columns:
        if not prop_name.startswith('_') and prop_name in columns:
            # if it is list then map each
            # else map itself
            if rules is not None and rules.has_key(prop_name):
                setattr(target, prop_name, None if rules[prop_name] is None else rules[prop_name](src))
                continue
            elif hasattr(src, prop_name):
                srcValue = getattr(src,prop_name)
            else:
                srcValue = None
            
            if type(srcValue) is list or type(srcValue) is InstrumentedList:
                c = list()
                for v in srcValue:
                    c.append(obj_map(v, mapper[type(v)], rules, mapper))
                setattr(target, prop_name, c)
            elif type(srcValue) is object:
                setattr(target, prop_name, obj_map(srcValue, 
                                                     mapper[type(srcValue)], rules=rules, mapper=mapper))
            else:
                setattr(target,prop_name, srcValue)
    return target
