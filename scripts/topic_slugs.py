import json
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from database.connection import get_db_connection
import unicodedata

import unicodedata

def normalize_topic(topic_name):
    """Apply the same normalization logic used in original ETL"""
    topic = topic_name.upper()

    # Handle special cases
    if topic == "DEUTSCHE LITERATUR MONOGRAPHIEN":
        return "de-lit-monographien"
    elif topic == "DEUTSCHE LITERATUR TEXTE":
        return "de-lit-texte"
    elif topic == "BIOGRAPHIE1":
        return "biographie"
    elif topic.startswith("ERSTAUSGABEN"):
        if "A - G" in topic:
            return "erstausgaben1"
        elif "H - M" in topic:
            return "erstausgaben2"
        elif "N - Z" in topic:
            return "erstausgaben3"
        else:
            return "erstausgaben"

    # Normal case: lowercase, take first word
    topic_lower = topic.lower()
    if "-" in topic_lower:
        topic_normalised = topic_lower.split("-")[0]
    elif "," in topic_lower:
        topic_normalised = topic_lower.split(",")[0]
    else:
        topic_normalised = topic_lower.split()[0]

    # Normalize unicode and replace umlauts
    topic_normalised = unicodedata.normalize("NFC", topic_normalised)
    topic_normalised = topic_normalised.replace('ä', 'ae').replace('ö', 'oe').replace('ü', 'ue').replace('ß', 'ss')

    return topic_normalised

def generate_topic_slugs():
    conn, cur = get_db_connection()

    try:
        cur.execute("SELECT topic_id, topic_name FROM topics ORDER BY topic_id")
        topics = cur.fetchall()

        mappings = []
        for topic_id, topic_name in topics:
            mappings.append({
                'topic_id': topic_id,
                'topic_name': topic_name,
                'topic_normalised': normalize_topic(topic_name)
            })

        # Save to JSON
        with open('topic_slugs.json', 'w', encoding='utf-8') as f:
            json.dump(mappings, f, indent=2, ensure_ascii=False)

        print(f"Generated {len(mappings)} topic slugs")

        # Print a few examples to verify
        for mapping in mappings[:5]:
            print(f"{mapping['topic_name']} → {mapping['topic_normalised']}")

    finally:
        conn.close()

if __name__ == "__main__":
    generate_topic_slugs()
