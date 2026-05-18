# Code bits I tend to forget

## printing things

- printing a few entries of a dict:
    
    rprint(dict(list(variants_dict.items())[:3]))

- printing insde a loop (when it's a list)

    `for variant in variants[:20]:`
    # Wrap in list() first, then slice
    `for key, value in list(my_dict.items())[:20]:`
        ...

## venv
restarting the venv:
`source venv/bin/activate`

## percentages

**"the part" divided by "the whole", times 100**
    matched_pct = (matched_count / unique_people) * 100 

## snippets for all the typing

https://snippet-generator.app/


## all of those pesky loops

### number of variables 

The pattern you use depends on what each iteration hands you. It's not a stylistic choice — it's a match between the shape of what's being iterated and how many "slots" you create on the left side of the for.

* for x in y: each iteration hands you one thing. So you need one variable. Use this for lists, sets, dict keys (when iterating a dict directly), or dict.values().
* for x, y in z: each iteration hands you two things packed together (a pair, technically a tuple). So you need two variables to unpack them. The classic case is dict.items(), which hands you (key, value) pairs. Another case is a list of pairs like [(1, 'a'), (2, 'b')].
* for i, x in enumerate(y): this is just a special case of the two-variable pattern. enumerate wraps any iterable and turns it into pairs of (index, item). So enumerate always hands you two things, which is why you always need two variables. Use it when you need to know the position of each item, not just the item itself. Your sort_order task is a perfect example — you care about whether you're on the first ID or the second ID.

The rule of thumb: **count what each iteration hands you, then create that many variables.**

### number of loops

**The number of loops equals how many levels deep you need to go, not how many nested structures exist.**

## does the key already exist in my dict?

check for membership with `if **variable** in **dict**`, then do:

    `dict[variable].append({})`
    else:
    `dict[variable] = {}

## alas, methods

Quick reference for "add a thing to a collection":

    list → .append(item) (adds one item to the end)
    set → .add(item)
    dict → d[key] = value (assignment, not a method)


## compare two dicts with matching keys, use values from the second one in the first one

    ```
    for name, entry in to_check.items():
        entry["info"]["person_id"] = checked[name]["info"]["person_id"]
        entry["info"]["match_found"] = checked[name]["info"]["match_found"]
        rprint(name, entry)
    ```
## Dictionary comprehensions, oooh aaah

    # Dict comprehension to shape my data and separate it into separate data structures

    singles_found = {k: v["info"] for k, v in singles_checked.items() if v["info"]["person_id"] is not None}
    rprint(f"existing singles: {len(singles_found)}")

    new_singles = {k: v["info"] for k, v in singles_checked.items() if v["info"]["person_id"] is None}
    rprint(f"new_singles count: {len(new_singles)}")

    The key to remember is: **in a dict comprehension, the left side of the `:` can be anything** — it doesn't have to be the original key.

    The pattern is:

    ```
    {new_key_expression : value_expression for k, v in some_dict.items()}
    ```

    - `k` and `v` are just variables available to you — you don't have to use both
    - `new_key_expression` can be `k`, `v`, `v["some_field"]`, a calculation, anything
    - Same for the value side

    So the question to ask yourself is: *"What do I want each key to be in my new dict?"* Then put that expression on the left.

    `★ Insight ─────────────────────────────────────`
    The `if` clause is only for **filtering** (deciding which items to include). If you're not throwing anything away — just reshaping or remapping — you don't need it.
    `─────────────────────────────────────────────────`

    SYNTAX:
    [result for item in source if condition]

    a compact “take-transform-collect” sentence with strict word order.

**“Result first, then loop source.”**

[name.upper() for name in names]
| Part    | Meaning                                               |
| ------- | ----------------------------------------------------- |
| `names` | the existing collection you already have              |
| `name`  | the temporary variable representing ONE thing from it |



## Help, which is the most up to date file

    from datetime import datetime

    for file in matched_folder.iterdir():

    datetime.fromtimestamp(file.stat().st_mtime)
    with open(file, "r") as f:
       matched = json.load(f)

    rprint(f"{file.stem} has {len(matched)} entries")
    rprint(f"{file.stem} — {len(matched)} entries — last modified: {datetime.fromtimestamp(file.stat().st_mtime)}")
