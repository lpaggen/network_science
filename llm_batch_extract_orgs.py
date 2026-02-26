import json
from openai import OpenAI
import time


PATH_TO_JSON_BATCH = ""  # batch_to_label.jsonl

def run():
    try:
        client = OpenAI()
        input_file = client.files.create(file=open(PATH_TO_JSON_BATCH, "rb"), purpose="batch")
        batch_job = client.batches.create(
            input_file_id=input_file.id,
            endpoint="/v1/chat/completions",
            completion_window="24h"
        )
        print(f"Batch ID: {batch_job.id}")
    except Exception as e:
        print(f"Failed to submit batch: {e}")

if __name__ == "__llm_batch_extract_orgs__":
    run()
# EOF