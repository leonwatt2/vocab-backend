import utils

config = utils.read_json("input/index.json")
data_index = {
    "categories": []
}

categories = config["categories"]

for c_id in categories.keys():
    c = categories[c_id]
    lists = c["lists"]

    data_lists = []

    for l_id in lists.keys():
        l = lists[l_id]
        raw_entries = utils.read_csv(f"input/{c_id}/{l_id}.csv")
        
        target = c["target"]
        origin = c["origin"]

        entries = [{"target": e[target], "origin": e[origin]} for e in raw_entries]
        path = f"data/{c_id}/{l_id}.json"

        data_lists.append({
            "id": l_id,
            "title": l["title"],
            "path": path,
            "hash": utils.hash(entries)
        })

        utils.write_json(path, {
            "entries": entries,
            "target": target,
            "origin": origin
        })

    data_index["categories"].append({
        "id": c_id,
        "title": c["title"],
        "origin": c["origin"],
        "target": c["target"],
        "lists": data_lists
    })
    
utils.write_json("data/index.json", data_index)