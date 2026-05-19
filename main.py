import json

with open("data/people/matched/matches_extended.json") as f:
    extended = json.load(f)

with open("data/people/fixing_ids/matches_ready.json") as f:
    ready = json.load(f)

extended_person_ids = {str(v["person_id"]) for v in extended.values() if v.get("person_id")}

in_ready = extended_person_ids & set(ready.keys())
not_in_ready = extended_person_ids - set(ready.keys())

print("extended person_ids already in matches_ready:", len(in_ready))
print("extended person_ids NOT in matches_ready:", len(not_in_ready))
