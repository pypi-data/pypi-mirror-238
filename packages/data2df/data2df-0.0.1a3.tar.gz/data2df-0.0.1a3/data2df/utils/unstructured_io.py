import json
import pickle

"""
For the moment I chose to not extend the devices to unstructured data types.
In my usual workflow, functions like these are enough.
Also, extending to unstructured seem problematic, probably I couldn't reuse
the same BaseDevice class.
Not sure if it's worth the hassle.

TODO: add type annotations
"""


def json2dict(path: str):
    with open(path, "r") as f:
        data = json.load(f)
    return data


def to_jsonfile(data, filename: str):
    # Handle sets in python dict
    def set_default(obj):
        if isinstance(obj, set):
            return list(obj)
        raise TypeError

    with open(filename, "w") as json_file:
        json.dump(data, json_file, indent=2, default=set_default)


def from_jsonfile(filename: str):
    with open(filename, "r") as json_file:
        data = json.load(json_file)
    return data


def to_pickle(object, filename: str):
    with open(filename, "wb") as pickle_file:
        pickle.dump(object, pickle_file)


def from_pickle(filename: str):
    with open(filename, "rb") as pickle_file:
        obj = pickle.load(pickle_file)
    return obj
