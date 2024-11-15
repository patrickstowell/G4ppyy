
def _cpp_destructor(self):
    self.__python_owns__ = False
    pass
    
def set_cppyy_owns(self):
    try:
        self.__del__ = _cpp_destructor    
    except:
        remove_destructor(self.super())    
    
    try:
        type(self).__del__ = _cpp_destructor        
    except:
        remove_destructor(self.super())    
    return self

new = set_cppyy_owns

