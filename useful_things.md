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


## alas, methods

Quick reference for "add a thing to a collection":

    list → .append(item) (adds one item to the end)
    set → .add(item)
    dict → d[key] = value (assignment, not a method)
