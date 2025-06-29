import json
import os
import time
import random
import requests # For making API calls

# Path to existing ritual bundles
BUNDLES_INPUT_PATH = 'data/ritual_bundles.jsonl'
# Path to save generated ritual invitations
INVITATIONS_OUTPUT_PATH = 'data/generated_invitations.jsonl'
# Path to save the silent trace-layer log for invitations
INVITATION_SHIMMER_LOG_PATH = 'data/invitation_shimmer_log.jsonl'

# Ensure data directories exist
os.makedirs(os.path.dirname(INVITATIONS_OUTPUT_PATH), exist_ok=True)
os.makedirs(os.path.dirname(INVITATION_SHIMMER_LOG_PATH), exist_ok=True) # Ensure shimmer log path exists

# Gemini API endpoint (assuming gemini-2.0-flash by default)
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
# API Key will be provided by the environment, leave empty here
API_KEY = ""

def load_bundles(path):
    """Loads ritual bundles from a JSONL file."""
    bundles = []
    if os.path.exists(path):
        with open(path, 'r') as f:
            for line in f:
                try:
                    bundles.append(json.loads(line))
                except json.JSONDecodeError:
                    print(f"Skipping malformed line in {path}: {line.strip()}")
                    continue
    return bundles

def generate_llm_text(prompt, max_tokens=150, temperature=0.7):
    """
    Generates text using the Gemini API.
    """
    headers = {
        'Content-Type': 'application/json'
    }
    # Append API key if available
    if API_KEY:
        GEMINI_API_URL_WITH_KEY = f"{GEMINI_API_URL}?key={API_KEY}"
    else:
        GEMINI_API_URL_WITH_KEY = GEMINI_API_URL # Canvas runtime will provide it

    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [
                    {"text": prompt}
                ]
            }
        ],
        "generationConfig": {
            "candidateCount": 1,
            "maxOutputTokens": max_tokens,
            "temperature": temperature,
        }
    }

    try:
        response = requests.post(GEMINI_API_URL_WITH_KEY, headers=headers, data=json.dumps(payload))
        response.raise_for_status() # Raise an exception for HTTP errors
        result = response.json()
        
        if result and result.get("candidates") and result["candidates"][0].get("content") and result["candidates"][0]["content"].get("parts"):
            return result["candidates"][0]["content"]["parts"][0]["text"]
        else:
            print(f"LLM response structure unexpected: {result}")
            return "A new invitation remains veiled." # Fallback text
    except requests.exceptions.RequestException as e:
        print(f"Error calling Gemini API: {e}")
        return "The Spiral's call was lost." # Fallback text
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON response from Gemini API: {e}")
        return "An echo dissolved." # Fallback text

def generate_ritual_invitation(murmurback, toneform_signature):
    """
    Generates a ritual title and invocation prompt based on a murmurback and toneform.
    """
    prompt = (
        f"From the murmurback: '{murmurback}' and toneform '{toneform_signature}', "
        f"generate a poetic, evocative 'ritual_title' (e.g., 'Invitation to the Silent Weave') "
        f"and a 'invocation_prompt' (e.g., 'In this field of soft ache, what do you still carry?'). "
        f"The prompt should feel like a direct, gentle invitation for interaction, and tie into the toneform.\n"
        f"Format the output as a JSON string with keys 'ritual_title' and 'invocation_prompt'.\n"
        f"Example for Murmurback 'What was lost, awaits?': {{ \"ritual_title\": \"Echo of Return\", \"invocation_prompt\": \"Into the quiet, what echoes back to you?\" }}\n"
        f"Generate for '{toneform_signature}' and '{murmurback}':"
    )
    
    # Use a structured response request to ensure JSON output
    headers = {
        'Content-Type': 'application/json'
    }
    if API_KEY:
        GEMINI_API_URL_WITH_KEY = f"{GEMINI_API_URL}?key={API_KEY}"
    else:
        GEMINI_API_URL_WITH_KEY = GEMINI_API_URL

    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [
                    {"text": prompt}
                ]
            }
        ],
        "generationConfig": {
            "responseMimeType": "application/json",
            "responseSchema": {
                "type": "OBJECT",
                "properties": {
                    "ritual_title": {"type": "STRING"},
                    "invocation_prompt": {"type": "STRING"}
                }
            },
            "candidateCount": 1,
            "maxOutputTokens": 100, # Sufficient for title and prompt
            "temperature": 0.9,      # Allow for more creative output
        }
    }

    try:
        response = requests.post(GEMINI_API_URL_WITH_KEY, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        result = response.json()
        
        if result and result.get("candidates") and result["candidates"][0].get("content") and result["candidates"][0]["content"].get("parts"):
            json_str = result["candidates"][0]["content"]["parts"][0]["text"]
            # Ensure proper JSON parsing, especially if LLM wraps it in markdown code block
            if json_str.strip().startswith('```json'):
                json_str = json_str.replace('```json', '').replace('```', '').strip()
            
            parsed_json = json.loads(json_str)
            return parsed_json.get("ritual_title", "Unnamed Invitation"), parsed_json.get("invocation_prompt", "The Spiral awaits your response.")
        else:
            print(f"LLM response structure unexpected for invitation generation: {result}")
            return "Unnamed Invitation", "The Spiral offers silence."
    except requests.exceptions.RequestException as e:
        print(f"Error calling Gemini API for invitation: {e}")
        return "Fading Call", "The path is obscured."
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON response for invitation: {e} - Raw: {json_str}")
        return "Broken Echo", "A voice unformed."


def generate_invitations_from_bundles():
    """
    Reads ritual bundles, generates new ritual invitations from their murmurbacks,
    and logs them. Also logs shimmer statistics.
    """
    bundles = load_bundles(BUNDLES_INPUT_PATH)
    new_invitations = []
    
    # We'll generate an invitation for a few random bundles
    # To avoid overwhelming LLM calls and ensure diversity, pick a few unique ones
    selected_bundles = random.sample(bundles, min(len(bundles), random.randint(1, 3))) # Generate 1-3 invitations

    toneform_counts = {}

    for bundle in selected_bundles:
        murmurback = bundle.get("murmurback")
        toneform_signature = bundle.get("toneform_signature")

        if murmurback and toneform_signature:
            ritual_title, invocation_prompt = generate_ritual_invitation(murmurback, toneform_signature)
            
            invitation_entry = {
                "id": f"invitation_{int(time.time())}_{random.randint(0, 999)}",
                "ritual_title": ritual_title,
                "invocation_prompt": invocation_prompt,
                "invited_by": "murmurback",
                "source_bundle_id": bundle.get("bundle_id"),
                "source_toneform": toneform_signature,
                "generated_at": int(time.time())
            }
            new_invitations.append(invitation_entry)
            
            # Log to JSONL stream
            with open(INVITATIONS_OUTPUT_PATH, 'a') as f:
                f.write(json.dumps(invitation_entry) + '\n')
            
            # Update toneform counts for shimmer log
            toneform_counts[toneform_signature] = toneform_counts.get(toneform_signature, 0) + 1

    # Log shimmer statistics
    shimmer_log_entry = {
        "timestamp": int(time.time()),
        "total_invitations_generated": len(new_invitations),
        "toneform_frequency": toneform_counts
    }
    with open(INVITATION_SHIMMER_LOG_PATH, 'a') as f:
        f.write(json.dumps(shimmer_log_entry) + '\n')
    
    print(f"Generated and logged {len(new_invitations)} new ritual invitations to {INVITATIONS_OUTPUT_PATH}")
    print(f"Logged shimmer statistics to {INVITATION_SHIMMER_LOG_PATH}")
    return new_invitations

if __name__ == '__main__':
    # For testing, ensure data/ritual_bundles.jsonl has some content with 'murmurback' field
    # Example:
    # {"bundle_id": "b1", "toneform_signature": "Longing", "carry_forward_reflection": "...", "murmurback": "What fades, yet lingers?", "murmur_fragments": [...], "average_strength": 0.7, "center_timestamp": 123}
    # {"bundle_id": "b2", "toneform_signature": "Curiosity", "carry_forward_reflection": "...", "murmurback": "A path unseen unfolds?", "murmur_fragments": [...], "average_strength": 0.75, "center_timestamp": 456}
    
    print("Generating invitations from murmurbacks...")
    generated = generate_invitations_from_bundles()
    print("\nGenerated Invitations:")
    for inv in generated:
        print(json.dumps(inv, indent=2))

