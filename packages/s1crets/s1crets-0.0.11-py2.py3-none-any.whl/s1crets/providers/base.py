from abc import ABCMeta, abstractmethod
from s1crets.cache import Cache
import hashlib
import cloudpickle


# try to make a hashable key for caching
def args_cache_key(*args, **kw):
    return hashlib.sha256(cloudpickle.dumps([args, kw])).digest()


class DefaultValue(object):
    """Indicates a default value, which is distinguishable from None (which
    can also be a default value)
    """
    pass


class BaseProvider(object, metaclass=ABCMeta):
    def __init__(self, cache_args={}, **kwargs):
        self.cache = Cache(**cache_args)
        self.kwargs = kwargs

    @staticmethod
    def dict_filt(d, keys):
        """filter dictionary d to keys keys"""
        return dict([(i, d[i]) for i in d if i in set(keys)])

    @abstractmethod
    def get(self, path, keypath=None, default=DefaultValue, decrypt=True, cached=True,
            retry=None, timeout=None):
        pass

    @abstractmethod
    def get_by_path(self, path, decrypt=True, recursive=True, cached=True,
                    retry=None, timeout=None):
        pass

    @abstractmethod
    def update(self, path, value, retry=None, timeout=None):
        pass

    @abstractmethod
    def path_exists(self, path, keypath=None, cached=True, retry=None, timeout=None):
        pass
