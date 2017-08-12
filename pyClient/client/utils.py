
class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class cUnDelete(object) :
    def __delattr__(self, key) :
        raise Exception( "can not delete "+key )

class Dict( dict ):
    def __getattr__(self,key):
        return self[key] 
