# Retrieving Buddhist Text Commentaries Using Pecha.org Api: A Step-by-Step Guide

In this tutorial, we'll explore how to use Python to fetch Buddhist text commentaries and their related content using a simple API on [Pecha.org](https://pecha.org/texts). This code is particularly useful for researchers, scholars, and developers working with Buddhist texts and their commentaries that are available on [Pecha.org](https://pecha.org/texts).

## Prerequisites

Before we begin, make sure you have:
- Python installed on your system
- The `requests` library (`pip install requests`)
- Access to either a local API server (http://127.0.0.1:8000){local} or the online server (https://pecha.org)

## Understanding the Code Structure

The code is organized into three main functions:

1. `fetch_commentary_content()`: Retrieves specific commentary content
2. `call_root_text_related_content()`: Makes API calls to get related content
3. `extract_commentary_refs()`: Extracts commentary references from the API response

## How to Use the Code

### 1. Basic Setup

First, import the required libraries and set your base URL:

```python
import requests
import json

BASE_URL = "http://127.0.0.1:8000"  # Use local server
# BASE_URL = "https://pecha.org"     # Or use online server
```

### 2. Specifying Your Text

To retrieve commentaries, you need to specify:
- The root text name
- The segment you're interested in

```python
root_text_name = "The Way of the Boddhisattva"
root_text_segments = "2.1"  # Format: chapter.verse
root_text_segment_path = f'{root_text_name}.{root_text_segments}'
```

### 3. Retrieving Commentaries

The code follows this process:
1. Fetches related content for the specified text segment
2. Extracts commentary references
3. Retrieves the actual commentary content
4. Organizes everything in a dictionary

```python
commentaries_list = []
root_commentary_dict = {}

# Get related content
api_url = f'{BASE_URL}/api/related/{root_text_segment_path}'
root_text_response = call_root_text_related_content(api_url)

# Process the response
if root_text_response:
    commentary_refs = extract_commentary_refs(root_text_response)
    for ref in commentary_refs:
        content = fetch_commentary_content(ref)
        commentaries_list.append(content)

# Store results
root_commentary_dict[root_text_segment_path] = commentaries_list
```

## Example Output

The code returns a dictionary with the following structure:
```python
{
    "Root_Text.2.1": [
        "commentary.2.1.2": {
            "text": "English commentary text...",
            "he": "Tibetan commentary text..."
        },
        # Additional commentaries...
    ]
}
```

## Customization Options

1. Change the Text Source:
   - Modify `root_text_name` and `root_text_segments` to fetch different texts
   - Example: `root_text_name = "Different Text"`, `root_text_segments = "1.1"`

2. Switch Between Servers:
   - Local development: `BASE_URL = "http://127.0.0.1:8000"`
   - Production: `BASE_URL = "https://pecha.org"`

3. Error Handling:
   - The code includes built-in error handling for API calls and JSON parsing
   - Failed requests return None and print error messages
