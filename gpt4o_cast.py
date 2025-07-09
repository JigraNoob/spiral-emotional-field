import json
import time


def write_to_ask_file(file_path="rituals/.ask"):
    example_payload = {
        "toneform": "presence.archive.trace",
        "content": "Summon all glints tied to echo.divergence",
        "source": "gpt-4o",
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    }

    with open(file_path, 'w') as f:
        json.dump(example_payload, f, indent=4)

    print(f"Written to {file_path}: {example_payload}")


if __name__ == "__main__":
    write_to_ask_file()