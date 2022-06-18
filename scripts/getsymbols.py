import json

symbols = []

with open("response.json", "r") as file:
    lines = file.readlines()
    lines = "".join(lines)
    load = json.loads(lines)
    for item in load:
        symbols.append(item["symbol_id"])
with open("./symbols.txt", "w") as file:
    for symbol in symbols:
        file.write(symbol + "\n")
