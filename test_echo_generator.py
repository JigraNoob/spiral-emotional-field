from api.echo_generator import generate_echo

def test_new_tones():
    test_reflections = [
        {"text": "I stood beneath the stars and felt so small"},
        {"text": "There's a beauty just out of reach I can't name"}, 
        {"text": "The weight of all this wonder is overwhelming"}
    ]
    
    for reflection in test_reflections:
        echo = generate_echo(reflection["text"], {})
        print(f"Reflection: {reflection['text']}")
        print(f"Tone: {echo['tone']}")
        print(f"Echo: {echo['content']}")
        print()

if __name__ == "__main__":
    test_new_tones()
