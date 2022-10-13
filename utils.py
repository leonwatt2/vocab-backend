import csv
from functools import reduce
import json
import copy
from pathlib import Path
import re
import os
import send2trash
import glob
import hashlib

DATE_FORMAT = "%Y-%m-%dT%H:%M:%S"

def read_from_file(path):
    with open(path) as f:
        return f.read()

def write_to_file(path, content):
    create_dir_if_not_existing(path)
    with open(path, "w") as f:
        f.write(str(content))

def read_csv(path, delimiter = ","):
    with open(path) as f:
        return list(csv.DictReader(f, delimiter=delimiter))

def read_json(path):
    return json.loads(read_from_file(path))

def write_csv(path, content):
    create_dir_if_not_existing(path)
    with open(path, "w") as f:
        writer = csv.writer(f)
        header = content[0].keys()
        writer.writerow(header)
        writer.writerows([[row[h] for h in list(header)] for row in content])

def write_json(path, content, indent=None):
    write_to_file(path, json.dumps(content, indent=indent))

def write_json_and_csv(path_without_suffix, content, indent_json=None, csv_array_attribute=None):
    write_json(f"{path_without_suffix}.json", content, indent_json)
    write_csv(f"{path_without_suffix}.csv", content if csv_array_attribute == None else content[csv_array_attribute])

def create_dir_if_not_existing(path):
    if("/" not in path): return
    file_part = re.findall("\/[^\/]+\.[^\/]+$", path)
    if len(file_part): path = path[:-len(file_part[0])]
    Path(path).mkdir(parents=True, exist_ok=True)

def exists(path):
    return os.path.exists(path)

def move_files_to_bin(glob_string):
    files = glob.glob(glob_string)
    send2trash.send2trash(files)

def execute_if_not_cached(fn, json_cache_file):
    try:
        return read_json(json_cache_file)
    except:
        res = fn()
        write_json(json_cache_file, res)
        return res

def group_by(arr_of_dicts, grouping_attr):
    res = {}

    for el in arr_of_dicts:
        grouping_value = el[grouping_attr]
        res.setdefault(grouping_value, [])
        res[grouping_value] += [el]

    return res

def group_by_as_list(arr_of_dicts, grouping_attr):
    return list(group_by(arr_of_dicts, grouping_attr).values())


def divide_or_zero(numerator, denominator):
    if denominator == 0: return 0
    return numerator / denominator

def flatten(list_of_lists):
    res = []
    for l in list_of_lists: res.extend(l)
    return res

def filter_duplicates(arr, key_fn = lambda x: x):
    return [el for (i, el) in enumerate(arr) if arr.index([el2 for el2 in arr if key_fn(el) == key_fn(el2)][0]) == i]

def merge_objects(o1, o2):
    res = copy.copy(o1)
    for k in o2.keys():
        if k not in res: res[k] = o2[k]
    return res

def filtered_keys(obj, filter_fn):
    return {k: v for (k, v) in obj.items() if filter_fn(k)}
        
def filtered_list_item_keys(arr, filter_fn):
    return [filtered_keys(obj, filter_fn) for obj in arr]

def find(arr, filter_fn):
    return next((el for el in arr if filter_fn(el)), None)

def pairs(arr):
    return list(zip(arr, arr[1:]))

def accumulate_elements(arr):
    return [reduce(lambda a, b: a + b, arr[:i], 0) for i in range(1, len(arr) + 1)]

def hash(anything):
    s = anything if type(anything) == str else json.dumps(anything)
    return hashlib.sha256(s.encode("utf-8")).hexdigest()