import sqlite3 # Paths are stored in local SQLITE3 database
import requests
import json  
import ast

# API endpoint for generating captions
#API_ENDPOINT = "https://martin-mostly-long-maiden.trycloudflare.com/api/v1/generate"
API_ENDPOINT = "http://127.0.0.1:5000/api/v1/generate"

# Function to fetch records from the database
def fetch_records():
    conn = sqlite3.connect("images.db")
    cursor = conn.cursor()

    # SQL query to select undeleted and not ignored records
    query = """
        SELECT id, full_path
        FROM image
        WHERE deleted IS NULL
          AND ignore IS NULL
          AND llm_path_caption IS NULL
          AND caption IS NOT NULL
          AND width>1024
          AND height>1024
        ORDER BY RANDOM()
        LIMIT 100000
    """

    cursor.execute(query)
    records = cursor.fetchall()
    cursor.close()
    conn.close()
    return records

# Function to generate caption using the API
def generate_caption(full_path):
    prompt = """*INSTRUCTIONS*
Generate 3 tags (max 6) based on the given full_path by following these guidelines and examples:

1. Extract relevant information from the full_path and consider folder names as potential tags.
2. Look for descriptive keywords or phrases within the full_path that indicate the content or theme of the image.
3. Identify specific series, magazine names, or photo sets mentioned in the full_path.
4. Consider geographic references, such as country or region names, as potential tags.
6. Do not generate tags which are not related to full_path!!!

Use the above guidelines to generate tags for each image based on its full_path. Provide the generated tags (max 6) in *VALID JSON* format ONLY, as shown below. No side comments or introduction allowed! JSON Response must be fully parsable in Python.
TASK OUTPUT [JSON] example:
{{
	"tags": ["tag1","tag2","tag3","tag4","tag5","tag6"]
}}

*TASK INPUT [JSON]:*
{{
	"full_path ": "{}"
}}

*TASK OUTPUT [JSON]:*

""".format(full_path)

    request = {
        "prompt": prompt,
        "max_new_tokens": 120,
        'do_sample': True,
        'temperature': 1.07,
        'top_p': 1,
        'typical_p': 1,
        'repetition_penalty': 1.05,
        'top_k': 100,
        'min_length': 0,
        'no_repeat_ngram_size': 0,
        'num_beams': 1,
        'penalty_alpha': 0,
        'length_penalty': 1,
        'early_stopping': False,
        'seed': -1,
        'add_bos_token': True,
        'truncation_length': 2048,
        'ban_eos_token': False,
        'skip_special_tokens': True,
        'stopping_strings': []
    }

    headers = {     
        "Content-Type": "application/json" 
    }

    max_retries = 1
    retry_count = 0

    while retry_count < max_retries:
        response = requests.post(API_ENDPOINT, data=json.dumps(request), headers=headers)

        if response.status_code == 200:
            try:
                text = response.json()['results'][0]['text']

                # Extract the JSON string from the text
                json_start = text.find('{')
                json_end = text.rfind('}')
                if json_start != -1 and json_end != -1:
                    json_string = text[json_start:json_end + 1]

                    # Remove surrounding glitches if present
                    json_string = json_string.strip('`')
                    # Check if JSON string is enclosed in single quotes instead of double quotes
                    if json_string.startswith("'") and json_string.endswith("'"):
                        json_string = json_string.replace("'", '"')

                    # Parse JSON string
                    inner_json = json.loads(json_string)
                    if isinstance(inner_json, dict) and "tags" in inner_json:
                        tags = inner_json["tags"]
                        tags_list = ", ".join(str(tag) for tag in tags)
                        print(f"Generated caption for image: {full_path} | {tags_list}")
                        return tags_list

                print(f"Invalid response. 'tags' key not found. Retrying... (Attempt {retry_count + 1}/{max_retries}) | {text}")
                retry_count += 1

            except (json.JSONDecodeError, ValueError, KeyError) as e:
                print(f"Failed to parse inner JSON: {e}. Retrying... (Attempt {retry_count + 1}/{max_retries}) | {text}")
                retry_count += 1
        else:
            print(f"Failed to generate caption for image: {full_path}. Error: {response.text}")
            return None

    print(f"Max retries reached. Failed to generate caption for image: {full_path}")
    return None



# Function to update the llm_path_caption field in the database
def update_llm_path_caption(record_id, caption):
    conn = sqlite3.connect("images.db")
    cursor = conn.cursor()

    # SQL query to update the llm_path_caption field
    query = """
        UPDATE image
        SET llm_path_caption = ?
        WHERE id = ?
    """

    cursor.execute(query, (caption, record_id))
    conn.commit()
    cursor.close()
    conn.close()

# Main function to fetch records, generate captions, and update the database
def main():
    records = fetch_records()

    total_records = len(records)
    print(f"Processing {total_records} records...")

    count = 0

    for record in records:
        count += 1
        record_id, full_path = record
        print(f"Processing record {count}/{total_records}")

        caption = generate_caption(full_path)

        if caption:
            update_llm_path_caption(record_id, caption)
            print(f"Updated llm_path_caption for record ID {record_id}")

    print("Processing completed.")

if __name__ == "__main__":
    main()