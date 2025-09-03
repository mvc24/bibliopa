# import packages
import json

# read parsed file
with open("data/last_output.txt", "r") as f:
    filepath = f.read().strip()

# print(filepath)

with open(filepath, "r", encoding="utf-8") as f:
    data = json.load(f)

result_raw = data["content"][0]

print(result_raw)
