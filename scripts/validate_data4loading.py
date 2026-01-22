import json
from pathlib import Path
from rich import print
from collections import defaultdict

people_records_prepped_file = Path("data/people/people_records_prepped.json")
books2people_prepped_file = Path("data/people/books2people_prepped.json")
people_records_validated_file = Path("data/people/people_records_validated.json")
folder_matched = Path("data/matched")
folder_validated = Path("data/validated")

validation_failed_log_file = Path("data/logs/validation_failed_log.json")
validation_report_log_file = Path("data/logs/validation_report_log.json")
validation_log_file = Path("data/logs/validation_log.json")

def validate_data():
    people_records = []
    books2people_records = []

    with open(people_records_prepped_file, "r") as f:
        people_records = json.load(f)

    with open(books2people_prepped_file, "r") as f:
        books2people_records = json.load(f)

    books2people_dict = defaultdict(list)
    for entry in books2people_records:
        books2people_dict[entry["composite_id"]].append(entry)

    people_dict = {person["unified_id"]: person for person in people_records}

    # all failed entries will be collected, grouped by file name. They will be separated between "not_found" for those where the composite_id doesn't appear in the lookup dict, and those where the expected total and counted total of people don't match OR have an "oops" unified_id will be in "issues".
    # All validated entries will be collected in the report, grouped by file. If there is a mismatch between expected and actual roles, the entire entry will be stored, together with a report. If there are no issues, only the composite_id will be stored.

    processed_file_count = 0
    failed_entries_total = 0

    failed_entries = {}
    validated_report = {}
    validation_log = {}
    people_not_validated = {}
    people_validated = []
    unified_id_found = set()

    for file in folder_matched.iterdir():
        validated_entries = {}
        validated_count = 0
        validated_with_issues_count = 0
        not_found_count = 0
        failed_count = 0
        entry_count = 0
        ids_found = 0

        validated_report[file.stem] = {
            "issues": {},
            "no_issues": []
        }

        failed_entries[file.stem] = {
            "not_found": {},
            "issues": {}
        }

        if not file.exists():
            raise FileNotFoundError(f"{file} doesn't exist!")

        with open(file, "r") as f:
            books = json.load(f)
            #rprint(books)
            processed_file_count += 1

        for composite_id, book in books.items():
            entry_count += 1
            authors = book["parsed_entry"].get("authors") or []
            editors = book["parsed_entry"].get("editors") or []
            contributors = book["parsed_entry"].get("contributors") or []
            translator = book["parsed_entry"]["translator"]
            is_translation = book["parsed_entry"]["is_translation"]

            authors_exp = len(authors)
            editors_exp = len(editors)
            contributors_exp = len(contributors)
            translator_exp = 1 if translator else 0
            expected_total = authors_exp + editors_exp + contributors_exp + translator_exp


            if composite_id in books2people_dict:
                ids_found += 1
                books2people_data = books2people_dict[composite_id]
                unified_ids_in_book = [entry["unified_id"] for entry in books2people_data]

                author_count = 0
                editor_count = 0
                contributor_count = 0
                translator_count = 0
                total = 0
                author_mismatch_count = 0
                editor_mismatch_count = 0
                contributor_mismatch_count = 0
                translator_mismatch_count = 0


                author_mismatch = False
                editor_mismatch = False
                contributor_mismatch = False
                translator_mismatch = False

                for entry in books2people_data:
                    unified_id = entry["unified_id"]
                    is_author = entry["is_author"]
                    is_editor = entry["is_editor"]
                    is_contributor = entry["is_contributor"]
                    is_translator = entry["is_translator"]

                    oops_id = False

                    if unified_id == "oops":
                        oops_id = True
                        failed_entries[file.stem]["issues"][composite_id] = {
                            "book": book,
                            "report": {
                                "oops": oops_id
                            }
                        }
                        failed_entries_total += 1
                        continue

                    if is_author:
                        author_count += 1
                        total +=1

                    if is_editor:
                        editor_count += 1
                        total +=1

                    if is_contributor:
                        contributor_count += 1
                        total +=1

                    if is_translator:
                        translator_count += 1
                        total +=1

                if not authors_exp == author_count:
                    author_mismatch = True
                    author_mismatch_count += 1

                if not editors_exp == editor_count:
                    editor_mismatch = True
                    editor_mismatch_count += 1

                if not contributors_exp == contributor_count:
                    contributor_mismatch = True
                    contributor_mismatch_count += 1

                if not translator_exp == translator_count:
                    translator_mismatch = True
                    translator_mismatch_count +=1

                # Check whether the overall count matches - this currently decides whether an entry fails or not
                if not expected_total == total:
                    failed_entries[file.stem]["issues"][composite_id] = {
                        "book": book,
                        "books2people": books2people_data,
                        "report": {
                            "expected_total": expected_total,
                            "found total": total,
                            "authors_exp": authors_exp,
                            "authors": author_count,
                            "editors_exp": editors_exp,
                            "editors": editor_count,
                            "contributors_exp": contributors_exp,
                            "contributors": contributor_count,
                            "translator_exp": translator_exp,
                            "translator": translator_count
                        }
                    }
                    failed_count +=1

                # overall number of people matches, counts as validated
                else:
                    # check people data
                    unified_id_found.update(unified_ids_in_book)

                    has_role_mismatch = any([author_mismatch, editor_mismatch, contributor_mismatch, translator_mismatch])
                    if not oops_id and not has_role_mismatch:
                        validated_entries[composite_id] = {
                            "books": book["parsed_entry"],
                            "admin":book["parsed_entry"].pop("administrative"),
                            "books2people": books2people_data
                        }
                        validated_report[file.stem]["no_issues"].append(composite_id)
                        validated_count +=1

                    if not oops_id and has_role_mismatch:
                        validated_with_issues_count +=1
                        validated_entries[composite_id] = {
                            "books": book["parsed_entry"],
                            "admin":book["parsed_entry"].pop("administrative"),
                            "books2people": books2people_data
                        }
                        validated_report[file.stem]["issues"][composite_id] = {
                        "book": book,
                        "report": {
                            "expected_total": expected_total,
                            "found total": total,
                            "authors_exp": authors_exp,
                            "authors": author_count,
                            "editors_exp": editors_exp,
                            "editors": editor_count,
                            "contributors_exp": contributors_exp,
                            "contributors": contributor_count,
                            "translator_exp": translator_exp,
                            "translator": translator_count
                        }
                    }

            else:
                failed_entries[file.stem]["not_found"][composite_id] = {"book": book}
                not_found_count += 1


        percent = (ids_found / entry_count ) * 100

        validation_log[file.stem] = {
            "books": entry_count,
            "matched": f"{percent:.2f}%",
            "not_found": not_found_count,
            "validated": validated_count,
            "validated_with_issues": validated_with_issues_count,
            "failed": failed_count
        }

        # write validated topic files:
        validated_path = folder_validated / file.name

        with open(validated_path, "w") as f:
            json.dump(validated_entries, f, ensure_ascii=False, indent=2)

    for unified_id, person in people_dict.items():
        if unified_id not in unified_id_found:
            people_not_validated[unified_id] = person
        else:
            people_validated.append(person)


    with open(validation_failed_log_file, "w") as f:
        json.dump(failed_entries, f, ensure_ascii=False, indent=2)

    with open(validation_log_file, "w") as f:
        json.dump(validation_log, f, ensure_ascii=False, indent=2)

    with open(validation_report_log_file, "w") as f:
        json.dump(validated_report, f, ensure_ascii=False, indent=2)

    with open(people_records_validated_file, "w") as f:
        json.dump(people_validated, f, ensure_ascii=False, indent=2)

    print(validation_log)
    # rprint(failed_entries)

validate_data()
