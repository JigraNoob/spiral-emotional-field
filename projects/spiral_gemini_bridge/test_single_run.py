# C:/spiral/projects/spiral_gemini_bridge/test_single_run.py
from ritual_gemini_loop import handle_new_whisper

print("Performing a single run of the whisper handler...")

try:
    with open("whisper_in.txt", "r", encoding="utf-8") as f:
        content = f.read()
        if content and content.strip():
            print("Found whisper content, processing...")
            handle_new_whisper(content)
            print("Processing complete.")
        else:
            print("whisper_in.txt is empty. Nothing to process.")
except FileNotFoundError:
    print("Error: whisper_in.txt not found.")
except Exception as e:
    print(f"An error occurred: {e}")

