from pprint import pp
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from scripts.get_topics import get_topics

topics_data = []
# pp(type(topics))

def load_topics():
    topics = get_topics()
    topics_data = []
    for topic_id, topic in enumerate(topics, start=1):
        topics_data.append({
            "topic_id": topic_id,
            "topic_name": topic
        })
    # pp(topics_data)

    return topics_data
