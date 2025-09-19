from pprint import pp
import sys
import uuid
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from scripts.get_topics import get_topics

topics_data = []
# pp(type(topics))

def load_topics():
    topics = get_topics()
    topics_data = []
    for topic in topics:
        topics_data.append({
        "topic_id": uuid.uuid4(),
        "topic_name": topic
        })
    # pp(topics_data)

    return topics_data
