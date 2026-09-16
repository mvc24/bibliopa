import json
from pathlib import Path
from collections import defaultdict

project_root = Path(__file__).parent.parent

nopes_results_dir = project_root / "database/in_progress/nopes_results"
unmatched_file = project_root / "data/people/unmatched_flat.json"
output_file = project_root / "database/in_progress/nopes_final.json"


def build_unmatched_lookup(unmatched):
    """
    Build lookup: composite_id -> list of unmatched entries.
    Mirrors the structure used in the notebook.
    """
    lookup = defaultdict(list)
    for entry in unmatched:
        lookup[entry["composite_id"]].append(entry)
    return lookup


def load_nopes_results():
    result_files = sorted(nopes_results_dir.glob("results_nopes_*.json"))

    if not result_files:
        print(f"No result files found in {nopes_results_dir}")
        return []

    print(f"Found {len(result_files)} result files")

    all_results = []
    for rf in result_files:
        with open(rf, "r", encoding="utf-8") as f:
            data = json.load(f)
        for entry in data:
            entry.pop("_source_custom_id", None)
            entry.pop("_error", None)
            entry.pop("_raw_content", None)
        all_results.extend(data)

    print(f"Loaded {len(all_results)} total results")
    return all_results


def main():
    print(f"Loading unmatched from {unmatched_file}...")
    with open(unmatched_file, "r", encoding="utf-8") as f:
        unmatched = json.load(f)

    unmatched_lookup = build_unmatched_lookup(unmatched)
    print(f"Built unmatched lookup: {len(unmatched_lookup)} composite_ids")

    all_results = load_nopes_results()

    if not all_results:
        return

    new_people = []
    matches = []
    oops = []

    for result in all_results:
        display_norm = result.get("display_norm")

        if result.get("unified_id") == "oops":
            oops.append(result)
            continue

        if result.get("match_found"):
            matches.append({
                "display_norm": display_norm,
                "composite_id": result.get("composite_id"),
                "matched_unified_id": result.get("matched_unified_id"),
                "matched_person_id": result.get("matched_person_id")
            })
            continue

        # New person — re-attach entries and roles from unmatched
        entries = []
        for composite_id in result.get("composite_id", []):
            records = unmatched_lookup.get(composite_id, [])
            for u in records:
                if u.get("display_norm") == display_norm:
                    entries.append({
                        "display_name": u.get("display_name"),
                        "composite_id": composite_id,
                        "sort_order": u.get("sort_order"),
                        "is_author": u.get("is_author"),
                        "is_editor": u.get("is_editor"),
                        "is_contributor": u.get("is_contributor"),
                        "is_translator": u.get("is_translator")
                    })
                    break

        new_people.append({
            "unified_id": result.get("unified_id"),
            "family_name": result.get("family_name"),
            "given_names": result.get("given_names"),
            "name_prefix": result.get("name_prefix"),
            "name_particles": result.get("name_particles"),
            "name_suffix": result.get("name_suffix"),
            "single_name": result.get("single_name"),
            "is_organisation": result.get("is_organisation", False),
            "entries": entries
        })

    output = {
        "new_people": new_people,
        "matches": matches,
        "oops": oops,
        "summary": {
            "total_results": len(all_results),
            "new_people": len(new_people),
            "matches": len(matches),
            "oops": len(oops)
        }
    }

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\n=== DONE ===")
    print(f"New people:  {len(new_people)}")
    print(f"Matches:     {len(matches)}")
    print(f"Oops:        {len(oops)}")
    print(f"Saved to:    {output_file}")


if __name__ == "__main__":
    main()
