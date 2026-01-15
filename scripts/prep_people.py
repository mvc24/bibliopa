import json
import sys

from pathlib import Path
from itertools import islice
from rich import print, inspect

people_file = Path("database/in_progress/people_prepped.json")

people_grouped_file = Path("database/in_progress/people_grouped.json")
# people_grouped_file = Path("database/in_progress/people_grouped_testing.json")

people_records_prepped_file = Path("data/people/people_records_prepped.json")
books2people_prepped_file = Path("data/people/books2people_prepped.json")
people_records_overview_file = Path("data/people/people_records_overview.json")

def create_people_lookup():
    people_dict = {}
    people_entries = []

    with open(people_file, "r") as f:
        people_entries = json.load(f)
        # print(people_entries)

    for entry in people_entries:
        unified_id = entry["unified_id"]
        people_dict.setdefault(unified_id, []).append(entry)

    sorted_entries = sorted(people_dict.items())
    sorted_dict = dict(sorted_entries)
    # print(sorted_dict)
    with open(people_grouped_file, "w") as f:
        json.dump(sorted_dict, f, ensure_ascii=False, indent=2)

# create_people_lookup()


def prep_people_for_loading():

    org_keywords = ["stiftung", "archiv", "gesellschaft", "forum", "gemeinde", "sammlung", "institut", "museum", "kultur", "kuratorium", "verlag", "ministerium", "akademie", "trust", "verein", "organisation", "vereinigung", "universität", "bibliothek"]

    people_records = []
    book2people_records = []
    people_overview_records = {}

    with open(people_grouped_file, "r") as f:
        people_grouped = json.load(f)

    # for unified_id, entries in islice(people_grouped.items(), 35):
    for unified_id, entries in people_grouped.items():
        entry_count = len(entries)

        all_family = set()
        all_given = set()
        all_particles = set()
        all_single = set()
        # print(unified_id, entries)
        entries_list = []

        for entry in entries:

            display_name = entry["display_name"]
            family_name = entry["family_name"]
            given_names = entry["given_names"]
            name_particles = entry["name_particles"]
            single_name = entry["single_name"]
            composite_id = entry["composite_id"]
            source_filename = entry["source_filename"]
            is_author = entry["is_author"]
            is_editor = entry["is_editor"]
            is_contributor = entry["is_contributor"]
            is_translator = entry["is_translator"]
            sort_order = entry["sort_order"]
            is_organisation = False

            if display_name:
                display_lower = display_name.lower()

            if any(keyword in display_lower for keyword in org_keywords):
                is_organisation = True
                print(f"found an org!")

            if single_name and not is_author:
                entry["single_name"] = None
                #print(f"removed a name!")

            if family_name:
                family_name = family_name.title()

            if single_name:
                single_name = single_name.title()

                # this needs to use the original spelling
            book2people_records.append({
                "composite_id": composite_id,
                "source_filename": source_filename,
                "unified_id": unified_id,
                "display_name": display_name,
                "family_name": family_name,
                "given_names": given_names,
                "name_particles": name_particles,
                "single_name": single_name,
                "is_author": is_author,
                "is_editor": is_editor,
                "is_contributor": is_contributor,
                "is_translator": is_translator,
                "sort_order": sort_order
            })

            entries_list.append({
                "composite_id": composite_id,
                "source_filename": source_filename,
                "unified_id": unified_id,
                "display_name": display_name,
                "is_author": is_author,
                "is_editor": is_editor,
                "is_contributor": is_contributor,
                "is_translator": is_translator,
                "sort_order": sort_order
            })

            if entry_count > 1:
                score_family = 0
                score_given = 0
                score_particles = 0
                score_single = 0

                if family_name:
                    score_family = len(family_name)
                    if any(ord(char) > 127 for char in family_name):
                        score_family += 2
                    all_family.add((score_family, family_name.title()))

                if given_names:
                    score_given = len(given_names)
                    if any(ord(char) > 127 for char in given_names):
                        score_given += 2
                    all_given.add((score_given, given_names))

                if name_particles:
                    score_particles = len(name_particles)
                    if any(ord(char) > 127 for char in name_particles):
                        score_particles += 2
                    all_particles.add((score_particles, name_particles))

                if single_name:
                    score_single = len(single_name)
                    if any(ord(char) > 127 for char in single_name):
                        score_single += 2
                    all_given.add((score_single, single_name))

        best_family = max(all_family, default=(0, None))
        best_given = max(all_given, default=(0, None))
        best_particles = max(all_particles, default=(0, None))
        best_single = max(all_single, default=(0, None))

        if entry_count > 1:
            family_name = best_family[1]
            given_names = best_given[1]
            name_particles = best_particles[1]
            single_name = best_single[1]

            # print(f"all_family: {all_family} best_family: {best_family}, family_name: {family_name}")
            # print(f"all_given: {all_given} best_given: {best_given}")
            # print(f"all_particle: {all_particles} best_particle: {best_particles}")
            # print(f"all_single: {all_single} best_single: {best_single}")

        if single_name:
            display_name = single_name
        else:
            display_name = " ".join(filter(None, [given_names, name_particles, family_name]))
        # print(display_name)

        family_variants = [name for score, name in all_family]
        given_variants = [name for score, name in all_given]
        particles_variants = [name for score, name in all_particles]
        single_variants = [name for score, name in all_single]

        # print(family_variants)

        people_records.append({
            "unified_id": unified_id,
            "family_name": family_name,
            "given_names": given_names,
            "name_particles": name_particles,
            "single_name": single_name,
            "is_organisation": is_organisation
        })
            # this should group everything AND store the variants in the "all_... " sets from the names
        people_overview_records.update({
            unified_id:
                {
                "family_name": family_name,
                "given_names": given_names,
                "name_particles": name_particles,
                "single_name": single_name,
                "is_organisation": is_organisation,
                "family_variants": family_variants,
                "given_variants": given_variants,
                "particles_variants": particles_variants,
                "single_variants": single_variants,
                "entries": entries_list
                }
            })

    with open(books2people_prepped_file, "w") as f:
        json.dump(book2people_records, f, ensure_ascii=False, indent=2)

    print(f"saved {len(book2people_records)} entries to books2people")

    with open(people_records_prepped_file, "w") as f:
        json.dump(people_records, f, ensure_ascii=False, indent=2)

    print(f"saved {len(people_records)} entries to people file")

    with open(people_records_overview_file, "w") as f:
        json.dump(people_overview_records, f, ensure_ascii=False, indent=2)
    print(f"saved {len(people_overview_records)} to overview file")

prep_people_for_loading()
