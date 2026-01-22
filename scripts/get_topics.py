from pathlib import Path
from pprint import pp
import json
import unicodedata

topics_dir = Path("data/raw/original")

def get_topics():
    topics = set()


    if not topics_dir.exists():
        raise NotADirectoryError("Directory doesn't exist!")

    for file in topics_dir.glob("*.docx"):
        topic = file.name.upper().replace(".DOCX", "")
        if topic == "ERSTAUSGABEN A - G":
            topic = "ERSTAUSGABEN"
        elif topic == "ERSTAUSGABEN H - M":
            topic = "ERSTAUSGABEN"
        elif topic == "ERSTAUSGABEN N - Z":
            topic = "ERSTAUSGABEN"
        elif topic == "BIOGRAPHIE1":
            topic = "BIOGRAPHIE"

        topics.add(topic.title())
    #print(topics)   # pp(unique_topics)
    return topics

#get_topics()


# def get_topics():
#     topics_dir = Path("data/original/keine preise")
#     topics = []

#     if not topics_dir.exists():
#         raise NotADirectoryError("Directory doesn't exist!")

#     for file in topics_dir.glob("*.docx"):
#         topic = file.name.upper().replace(".DOCX", "")
#         if topic == "DEUTSCHE LITERATUR MONOGRAPHIEN":
#                 topic_normalised = "de-lit-monographien"
#         elif topic == "DEUTSCHE LITERATUR TEXTE":
#             topic_normalised = "de-lit-texte"
#         elif topic == "ERSTAUSGABEN A - G":
#             topic = "erstausgaben"
#             topic_normalised = "erstausgaben1"
#         elif topic == "ERSTAUSGABEN H - M":
#             topic = "erstausgaben"
#             topic_normalised = "erstausgaben2"
#         elif topic == "ERSTAUSGABEN N - Z":
#             topic = "erstausgaben"
#             topic_normalised = "erstausgaben3"
#         else:
#             topic_lower = topic.lower()
#             if "-" in topic_lower:
#                 topic_normalised = topic_lower.split("-")[0]
#             elif "," in topic_lower:
#                 topic_normalised = topic_lower.split(",")[0]
#             else:
#                 topic_normalised = topic_lower.split()[0]  # Split on spaces, take first word

#             topic_normalised = unicodedata.normalize("NFC", topic_normalised)

#             topic_normalised = topic_normalised.replace('ä', 'ae').replace('ö', 'oe').replace('ü', 'ue').replace('ß', 'ss')
#         topics.append({
#             "topic": topic,
#         })
#         topics.sort()
#         # pp(topic)
#         # pp(topic_normalised)
#     pp(topics)
#     return topics

# get_topics()
