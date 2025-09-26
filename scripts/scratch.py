import json
from pathlib import Path
from pprint import pp
from re import sub


batch_log = Path("data/logs/batch_progress.json")
log = Path("data/logs/data_loading_log.json")
parsed_folder = Path("data/parsed")
parsed_files = list(parsed_folder.iterdir())
available_files = set()
# pp(f"Number of files in parsed: {len(count_files)}")
processed = {'batch_de-lit-texte_6-20.json',
'batch_mittelalter_6-6.json',
'batch_musik_6-11.json',
'batch_griechenland_4-10.json',
'batch_fremdsprachige_8-39.json',
'batch_fremdsprachige_17-39.json',
'batch_erstausgaben3_58-79.json',
'batch_erstausgaben3_48-79.json',
'batch_maerchen_3-3.json',
'batch_fruehes_1-5.json',
'batch_illustrierte_8-14.json',
'batch_reisen_12-13.json',
'batch_kunstbuecher_24-38.json',
'batch_ethnologie_5-13.json',
'batch_antike_2-9.json',
'batch_de-lit-texte_10-20.json',
'batch_philosophie_11-25.json',
'batch_erstausgaben3_2-79.json',
'batch_fremdsprachige_28-39.json',
'batch_biographien_24-27.json',
'batch_erstausgaben3_67-79.json',
'batch_briefe_12-15.json',
'batch_erstausgaben3_77-79.json',
'batch_biographien_12-27.json',
'batch_fremdsprachige_1-39.json',
'batch_erstausgaben3_41-79.json',
'batch_erstausgaben3_51-79.json',
'batch_russland_16-17.json',
'batch_literatur_5-12.json',
'batch_griechenland_10-10.json',
'batch_insel_26-27.json',
'batch_erstausgaben3_23-79.json',
'batch_erstausgaben3_33-79.json',
'batch_fremdsprachige_21-39.json',
'batch_zeitgeschichte_2-3.json',
'batch_biographien_2-27.json',
'batch_religion_1-5.json',
'batch_illustrierte_1-14.json',
'batch_de-lit-texte_19-20.json',
'batch_insel_19-27.json',
'batch_kunstbuecher_3-38.json',
'batch_philosophie_18-25.json',
'batch_literatur_4-12.json',
'batch_reisen_1-13.json',
'batch_russland_17-17.json',
'batch_biographien_13-27.json',
'batch_erstausgaben3_32-79.json',
'batch_mythologie_2-3.json',
'batch_kunstbuecher_13-38.json',
'batch_buddhismus_4-4.json',
'batch_insel_27-27.json',
'batch_insel_18-27.json',
'batch_de-lit-texte_18-20.json',
'batch_religion_3-5.json',
'batch_neuzeit_4-4.json',
'batch_signierte_5-10.json',
'batch_illustrierte_12-14.json',
'batch_okkultismus_2-8.json',
'batch_fruehes_3-5.json',
'batch_musik_7-11.json',
'batch_de-lit-texte_7-20.json',
'batch_bibliophile_1-9.json',
'batch_erstausgaben3_49-79.json',
'batch_erstausgaben3_59-79.json',
'batch_fremdsprachige_16-39.json',
'batch_philosophie_6-25.json',
'batch_insel_11-27.json',
'batch_judentum_7-8.json',
'batch_philosophie_10-25.json',
'batch_literatur_12-12.json',
'batch_kunstbuecher_35-38.json',
'batch_reisen_13-13.json',
'batch_illustrierte_9-14.json',
'batch_kunstbuecher_25-38.json',
'batch_christentum_5-6.json',
'batch_erstausgaben3_14-79.json',
'batch_biographien_25-27.json',
'batch_fremdsprachige_39-39.json',
'batch_erstausgaben3_3-79.json',
'batch_russland_5-17.json',
'batch_insel_5-27.json',
'batch_kunstbuecher_11-38.json',
'batch_erstausgaben3_20-79.json',
'batch_erstausgaben3_30-79.json',
'batch_suchliste_3-3.json',
'batch_signierte_10-10.json',
'batch_insel_25-27.json',
'batch_philosophie_24-25.json',
'batch_literatur_6-12.json',
'batch_biographien_11-27.json',
'batch_symbolkunde_1-2.json',
'batch_fremdsprachige_2-39.json',
'batch_russland_15-17.json',
'batch_illustrierte_10-14.json',
'batch_biographien_1-27.json',
'batch_musik_11-11.json',
'batch_fremdsprachige_32-39.json',
'batch_erstausgaben3_8-79.json',
'batch_philosophie_4-25.json',
'batch_biographien_18-27.json',
'batch_aegypten_1-4.json',
'batch_griechenland_7-10.json',
'batch_musik_5-11.json',
'batch_geschichte_2-3.json',
'batch_erstausgaben3_39-79.json',
'batch_erstausgaben3_29-79.json',
'batch_judentum_3-8.json',
'batch_de-lit-texte_5-20.json',
'batch_christentum_1-6.json',
'batch_biographien_8-27.json',
'batch_biographien_27-27.json',
'batch_bibliophile_5-9.json',
'batch_kunstbuecher_9-38.json',
'batch_literatur_10-12.json',
'batch_bibliophile_9-9.json',
'batch_insel_13-27.json',
'batch_islam_1-3.json',
'batch_erstausgaben3_16-79.json',
'batch_reisen_11-13.json',
'batch_fremdsprachige_15-39.json',
'batch_philosophie_5-25.json',
'batch_christentum_3-6.json',
'batch_griechenland_6-10.json',
'batch_judentum_1-8.json',
'batch_aegypten_3-4.json',
'batch_antike_6-9.json',
'batch_de-lit-texte_4-20.json',
'batch_musik_4-11.json',
'batch_erstausgaben3_28-79.json',
'batch_erstausgaben3_38-79.json',
'batch_russland_6-17.json',
'batch_fruehes_5-5.json',
'batch_erstausgaben3_75-79.json',
'batch_erstausgaben3_65-79.json',
'batch_briefe_10-15.json',
'batch_okkultismus_4-8.json',
'batch_erstausgaben3_17-79.json',
'batch_okkultismus_8-8.json',
'batch_ethnologie_7-13.json',
'batch_kunstbuecher_36-38.json',
'batch_reisen_10-13.json',
'batch_mittelalter_2-6.json',
'batch_kinder_4-4.json',
'batch_philosophie_13-25.json',
'batch_kunstbuecher_8-38.json',
'batch_insel_12-27.json',
'batch_insel_24-27.json',
'batch_philosophie_25-25.json',
'batch_insel_4-27.json',
'batch_erstausgaben3_31-79.json',
'batch_erstausgaben3_21-79.json',
'batch_russland_14-17.json',
'batch_erstausgaben3_43-79.json',
'batch_fremdsprachige_3-39.json',
'batch_biographien_10-27.json',
'batch_literatur_7-12.json',
'batch_religion_5-5.json',
'batch_suchliste_1-3.json',
'batch_briefe_7-15.json',
'batch_illustrierte_3-14.json',
'batch_illustrierte_11-14.json',
'batch_sonstiges_3-4.json',
'batch_buddhismus_2-4.json',
'batch_erstausgaben3_9-79.json',
'batch_musik_10-11.json',
'batch_buch_7-8.json',
'batch_fremdsprachige_23-39.json',
'batch_illustrierte_6-14.json',
'batch_zeitgeschichte_3-3.json',
'batch_illustrierte_14-14.json',
'batch_erstausgaben3_79-79.json',
'batch_erstausgaben3_69-79.json',
'batch_fremdsprachige_26-39.json',
'batch_fremdsprachige_36-39.json',
'batch_philosophie_20-25.json',
'batch_wien_7-10.json',
'batch_mythologie_1-3.json',
'batch_insel_21-27.json',
'batch_buch_2-8.json',
'batch_erstausgaben3_24-79.json',
'batch_kunstbuecher_15-38.json',
'batch_musik_8-11.json',
'batch_renaissance_2-4.json',
'batch_erstausgaben3_56-79.json',
'batch_ethnologie_11-13.json',
'batch_fremdsprachige_19-39.json',
'batch_biographien_15-27.json',
'batch_philosophie_9-25.json',
'batch_literatur_2-12.json',
'batch_reisen_7-13.json',
'batch_erstausgaben3_5-79.json',
'batch_erstausgaben3_70-79.json',
'batch_judentum_8-8.json',
'batch_kunstbuecher_23-38.json',
'batch_kunstbuecher_33-38.json',
'batch_ethnologie_2-13.json',
'batch_judentum_4-8.json',
'batch_erstausgaben3_12-79.json',
'batch_insel_17-27.json',
'batch_de-lit-texte_17-20.json',
'batch_christentum_6-6.json',
'batch_philosophie_16-25.json',
'batch_griechenland_3-10.json',
'batch_kinder_1-4.json',
'batch_fremdsprachige_10-39.json',
'batch_de-lit-monographien_9-10.json',
'batch_bibliophile_2-9.json',
'batch_de-lit-texte_1-20.json',
'batch_maerchen_2-3.json',
'batch_okkultismus_1-8.json',
'batch_musik_1-11.json',
'batch_oesterreich_12-13.json',
'batch_christentum_4-6.json',
'batch_russland_2-17.json',
'batch_judentum_6-8.json',
'batch_de-lit-texte_16-20.json',
'batch_insel_16-27.json',
'batch_aegypten_4-4.json',
'batch_philosophie_17-25.json',
'batch_kunstbuecher_32-38.json',
'batch_ethnologie_3-13.json',
'batch_kunstbuecher_22-38.json',
'batch_erstausgaben3_13-79.json',
'batch_monographien_3-3.json',
'batch_fruehes_2-5.json',
'batch_griechenland_2-10.json',
'batch_okkultismus_3-8.json',
'batch_fremdsprachige_11-39.json',
'batch_mittelalter_5-6.json',
'batch_illustrierte_7-14.json',
'batch_fremdsprachige_37-39.json',
'batch_erstausgaben3_68-79.json',
'batch_philosophie_21-25.json',
'batch_de-lit-texte_20-20.json',
'batch_de-lit-texte_9-20.json',
'batch_sonstiges_4-4.json',
'batch_reisen_6-13.json',
'batch_literatur_3-12.json',
'batch_fremdsprachige_7-39.json',
'batch_philosophie_8-25.json',
'batch_biographien_14-27.json',
'batch_fremdsprachige_18-39.json',
'batch_russland_10-17.json',
'batch_erstausgaben3_47-79.json',
'batch_philosophie_15-25.json',
'batch_bibliophile_4-9.json',
'batch_insel_14-27.json',
'batch_de-lit-texte_14-20.json',
'batch_kunstbuecher_20-38.json',
'batch_mittelalter_1-6.json',
'batch_erstausgaben3_63-79.json',
'batch_biographien_20-27.json',
'batch_okkultismus_7-8.json',
'batch_bibliophile_8-9.json',
'batch_musik_2-11.json',
'batch_oesterreich_8-13.json',
'batch_de-lit-texte_2-20.json',
'batch_literatur_8-12.json',
'batch_philosophie_3-25.json',
'batch_fremdsprachige_13-39.json',
'batch_geschichte_3-3.json',
'batch_biographien_6-27.json',
'batch_buddhismus_1-4.json',
'batch_fremdsprachige_25-39.json',
'batch_buch_8-8.json',
'batch_ethnologie_8-13.json',
'batch_zeitschriften_1-1.json',
'batch_russland_12-17.json',
'batch_biographien_16-27.json',
'batch_griechenland_9-10.json',
'batch_insel_2-27.json',
'batch_oesterreich_1-13.json',
'batch_erstausgaben3_37-79.json',
'batch_biographien_7-27.json',
'batch_erstausgaben3_19-79.json',
'batch_buch_6-8.json',
'batch_illustrierte_4-14.json',
'batch_kunstbuecher_38-38.json',
'batch_kunstbuecher_6-38.json',
'batch_signierte_1-10.json',
'batch_fremdsprachige_4-39.json',
'batch_biographien_17-27.json',
'batch_ethnologie_13-13.json',
'batch_griechenland_8-10.json',
'batch_symbolkunde_2-2.json',
'batch_wien_5-10.json',
'batch_neuzeit_3-4.json',
'batch_erstausgaben3_36-79.json',
'batch_erstausgaben3_26-79.json',
'batch_islam_2-3.json',
'batch_erstausgaben3_10-79.json',
'batch_okkultismus_5-8.json',
'batch_briefe_9-15.json',
'batch_kunstbuecher_31-38.json',
'batch_fruehes_4-5.json',
'batch_de-lit-texte_15-20.json',
'batch_insel_15-27.json',
'batch_russland_1-17.json',
'batch_biographien_21-27.json',
'batch_erstausgaben3_72-79.json',
'batch_de-lit-texte_3-20.json',
'batch_musik_3-11.json',
'batch_fremdsprachige_12-39.json',
'batch_philosophie_2-25.json',
'batch_griechenland_1-10.json',
'batch_aegypten_2-4.json'}
pp(len(processed))
pp(type(processed))

def get_not_loaded():

    for file in parsed_files:
        available_files.add(file.name)
    pp(len(available_files))
    pp(type(available_files))

    not_processed = available_files - processed

    pp(len(not_processed))
    pp(type(not_processed))

# processed: 306
# <class 'set'>
# available: 525
# <class 'set'>
# not_processed: 219
# <class 'set'>

get_not_loaded()

# def count_consolidated_entries():
#     folder = Path("data/consolidated")
#     total_entries = 0
#     counts = []
#     # file_paths = list(folder.iterdir())
#     for file in list(folder.iterdir()):
#         file_path = file

#         with open(file_path, "r") as f:
#             content = json.load(f)
#             count = len(content)
#             counts.append(count)
#             total_entries += count


#         # pp(filename)
#         # pp(f"count: {count}")

#         total = 0

#     for count in counts:
#         # pp(f"total = {total}")
#         previous_total = total
#         total += count
#         pp(f"{previous_total} + {count} is {total}.")


#     pp(total)


# count_consolidated_entries()

# def count_entries():
#     completed = []
#     with open (batch_log, "r") as f:
#         batches = json.load(f)
#         batch_count = 0
#         batch_entry_count = 0
#         count_unique_batch_entries = 0

#     with open(log, "r") as f:
#         entries = json.load(f)
#         entry_count = 0
#         corrupt_count = 0
#         unique_count = 0

#         for index, entry in enumerate(entries):
#             entry_count += entry["entry_count"]
#             corrupt_count += entry["corrupt_entries_found"]
#             # pp(entry_count)
#             # processed = len(entries)

#         for batch in batches.items():
#             submitted = batches["submitted"]
#             completed = batches["completed"]


#             completed_total = len(batches["completed"])

#             batch_count = len(submitted)

#             for submitted_entry in submitted.values():
#                 batch_entry_count += submitted_entry["entry_count"]
#                 batch_id = submitted_entry.get("batch_id")
#                 count = submitted_entry.get("entry_count")

#             # unique_batches = [id for id in completed if batch_id in completed]
#                 if batch_id in completed:
#                     count_unique_batch_entries += count

            # nr_unique = len(unique_batches)
            # unique_count +=
            # for batch_id in completed.values():

    # pp(f"batch_id{batch_id}")
    # pp(f"count_unique_batch_entries: {count_unique_batch_entries}")
    # pp(f"processed {processed} files")
    # pp(f"entry count = {entry_count}")
    # pp(f"corrupt = {corrupt_count}")
    # pp(f"batches submitted = {batch_count}")
    # pp(f"entries submitted = {batch_entry_count}")
    # pp(f"ids completed = {completed_total}")
    # pp(524 * 25)
    # pp(type(completed))
    # # pp(f"completed = {completed}")
    # pp(f"unique = {unique_count}")


# count_entries()
