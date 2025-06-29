from api.echo_generator import generate_echo

def test_liminal_cases():
    liminal_reflections = [
        {"text": "The ocean's endless horizon makes my chest ache"},
        {"text": "I trembled before the mountain's impossible beauty"}, 
        {"text": "The stars were so beautiful it hurt"},
        {"text": "This love is too vast to hold"}
    ]
    
    for reflection in liminal_reflections:
        echo = generate_echo(reflection["text"], {})
        print(f"Reflection: {reflection['text']}")
        print(f"Tone: {echo['tone']}")
        print(f"Echo: {echo['content']}")
        print()

if __name__ == "__main__":
    test_liminal_cases()
