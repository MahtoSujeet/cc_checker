with open("api/proxies.txt", "r") as file:
    proxis = file.readlines()
    d = dict()
    for item in proxis:
        item.split("\\")[0]
        d["http"] = item

print(d)
