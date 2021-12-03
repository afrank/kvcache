
import base64
import os
import yaml

class KVCache:
    """
    KVCache is a simple persistent key-value cache

    Every cache has a scope and within each scope you can have
    cache objects, then within each object you can have an arbitrary
    number of key-value pairs.

    The directory structure is ~/.kvcache/<scope>/<object>.cache

    Within a given cache object you have a yaml list of plaintext keys
    with base64-encoded values. 

    TODO: should we encrypt?
    """
    def __init__(self, scope="default", obj="default", basepath="~/.kvcache"):
        self.scope = scope
        self.path = os.path.expanduser(f"{basepath}/{scope}")
        self.obj = obj

        if not os.path.exists(self.path):
            os.makedirs(self.path)

        self.cache = {}

    @property
    def obj(self):
        return self._obj

    @obj.setter
    def obj(self, obj):
        self._obj = obj

    def read_object_file(self):
        items = {}
        try:
            res = yaml.load(open(f"{self.path}/{self.obj}.cache"), Loader=yaml.Loader)
        except:
            return

        for k,v in res.items():
            items[k] = base64.b64decode(v).decode("ascii")

        self.cache[self.obj] = items

    def write_object_file(self):
        if self.obj not in self.cache:
            self.read_object_file()

        enc_obj = {}

        for k,v in self.cache.get(self.obj):
            enc_obj[k] = base64.b64encode(v.encode("utf-8"))

        fp = open(f"{self.path}/{self.obj}.cache", "w")
        fp.write(yaml.dump(self.cache.get(enc_obj), Dumper=yaml.Dumper))
        fp.close()

    def get(self, key=None, obj=None):
        if obj:
            self.obj = obj
        res = None
        if self.obj not in self.cache and not os.path.exists(f"{self.path}/{self.obj}.cache"):
            return None
        elif self.obj not in self.cache:
            self.read_object_file()

        if key:
            return self.cache.get(self.obj).get(key)

        return self.cache.get(self.obj)

    def set(self, **kwargs):
        for k,v in kwargs.items():
            if self.obj not in self.cache:
                self.cache[self.obj] = {}

            #self.cache[self.obj][k] = base64.b64encode(v.encode("utf-8"))
            self.cache[self.obj][k] = v

        self.write_object_file()
