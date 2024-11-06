import requests
import json

BASE_URL = "http://127.0.0.1:8000"
#BASE_URL = "https://pecha.org"


def fetch_commentary_content(commentary_ref, headers=None):
    
    if headers is None:
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
    
    try:
        api_url = f"{BASE_URL}/api/texts/{commentary_ref}"
        
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        
        data = response.json()
        
        # Extract only text and he fields
        extracted_content = {
            'text': data.get('text', ''),
            'he': data.get('he', '')
        }
        
        return extracted_content
            
    except requests.exceptions.RequestException as e:
        print(f"Error fetching commentary content: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON response: {e}")
        return None
    
    
def call_root_text_related_content(url, method='GET', data=None, headers=None):
    if headers is None:
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
    
    try:
        if method == 'GET':
            response = requests.get(url, headers=headers)
        
        response.raise_for_status()
        
        try:
            return response.json()
        except json.JSONDecodeError:
            return response.text
            
    except requests.exceptions.RequestException as e:
        print(f"Error making API call: {e}")
        return None

def extract_commentary_refs(response_data):
    commentary_refs = []
    
    # Check if 'links' exists in the response
    if 'links' in response_data:
        # Filter links for items where type is 'commentary'
        for item in response_data['links']:
            if item.get('type') == 'commentary':
                commentary_refs.append(item.get('sourceRef'))
    
    return commentary_refs

if __name__ == "__main__":
    # text title and segments
    root_text_name = "The Way of the Boddhisattva"
    root_text_segments = "2.1"  # 2.1-5 (ie, from segment 1 to 5 of chapter 2)
    root_text_segment_path = f'{root_text_name}.{root_text_segments}'
    
    commentaries_list = []
    root_commentary_dict = {}

    api_url = f'{BASE_URL}/api/related/{root_text_segment_path}'
    
    root_text_response = call_root_text_related_content(api_url)
    
    # Extract list of comententary refs for input text
    if root_text_response:
        
        commentary_refs = extract_commentary_refs(root_text_response)
        for ref in commentary_refs:
            content = fetch_commentary_content(ref)
            commentaries_list.append(content)
        
    #return roots and and its commentaries
    root_commentary_dict[f'{root_text_segment_path}'] = commentaries_list
    print(root_commentary_dict)
        
    