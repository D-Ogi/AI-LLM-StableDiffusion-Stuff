# Mass Tags Generator for Image Paths with Ooobabooga WebUI

This repository contains a script for generating tags (or captions) in JSON format based on file's full paths. The script uses the API of Ooobabooga LLM text-generation-webui to mass generate tags.

## Prerequisites

- Python (Python and other requirements are provided by the webui)
- [Ooobabooga LLM text-generation-webui](https://github.com/oobabooga/text-generation-webui/tree/main) installed.
- SQLite3
- The script uses a local SQLite database named `images.db` to store image paths. Make sure you have created the database and have populated it with your image paths.

## Overview of the Script

The script performs the following actions:

1. Connects to a local SQLite3 database named `images.db` to fetch image paths.
2. Sends requests to the Ooobabooga LLM text-generation-webui's API to generate tags based on the image paths.
3. Processes the API response and extracts tags.
4. Updates the database with the generated tags for each image path.

## Directory Structure

```
oobabooga_windows\
│
├── text-generation-webui\
│   ├── mass_tags_generator.py   # This is the Python script.
│
└── cmd_windows.bat          # Batch file for Ooobabooga Conda environment activation
```

## Database Schema

Before running the script, make sure you have created the SQLite3 database named `images.db` with the following schema:

```sql
CREATE TABLE image (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_path TEXT NOT NULL,
    caption TEXT,
    llm_path_caption TEXT,
    deleted INTEGER,
    ignore INTEGER,
    width INTEGER,
    height INTEGER
);
```

## Instructions

1. Clone this repository or download the script files.
2. Make sure Ooobabooga LLM text-generation-webui is installed and running.
3. Create the SQLite3 database (`images.db`) with the schema provided above.
4. Populate the database with image paths.
5. Open `cmd_windows.bat` from the webui.
7. Run the script by executing `python mass_tags_generator.py`.

## Note

- The script fetches records from the database where the fields `deleted` and `ignore` are NULL, `llm_path_caption` is NULL, `caption` is NOT NULL, and image width and height are greater than 1024.
- It processes up to 100,000 records in random order.

## License

This project is under the MIT License.

