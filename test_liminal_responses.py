from api.echo_generator import generate_echo

def test_liminal_responses():
    liminal_test_reflections = [
        {"text": "The sunset was so beautiful it made my heart ache"},
        {"text": "I laughed until tears streamed down my face"},
        {"text": "The mountain's grandeur left me longing for something I couldn't name"},
        {"text": "Her smile brought me both joy and sorrow"}
    ]
    
    for reflection in liminal_test_reflections:
        echo = generate_echo(reflection["text"], {})
        print(f"Reflection: {reflection['text']}")
        print(f"Tone: {echo['tone']}")
        print(f"Echo: {echo['content']}")
        print()

if __name__ == "__main__":
    test_liminal_responses()
