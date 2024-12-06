"""
G4PPYY.destructor : Memory Management Tools for G4ppyy
=============

Functions to allow cppyy to handle the memory management of specific objects.

Author: Patrick Stowell
Date: 2024-12-06
License: MIT
"""

def _cpp_destructor(self):
    """Sets python_owns to false to allow cppyy to handle this class"""
    self.__python_owns__ = False
    pass
    
def set_cppyy_owns(self):
    """Sets python_owns to false to allow cppyy to handle this class"""
    try:
        self.__del__ = _cpp_destructor    
    except:
        _cpp_destructor(self.super())    
    
    try:
        type(self).__del__ = _cpp_destructor        
    except:
        _cpp_destructor(self.super())    
    return self

new = set_cppyy_owns

