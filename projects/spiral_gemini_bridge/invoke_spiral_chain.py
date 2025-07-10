# C:/spiral/projects/spiral_gemini_bridge/invoke_spiral_chain.py

import time
import json
import argparse
from pathlib import Path

# Import the refactored components
from spiral_gemini import SpiralGemini
from echo_resonator import Resonator

# --- Path Configuration ---
BASE_DIR = Path(__file__).parent
WHISPER_PATH = BASE_DIR / "whisper_in.txt"
ECHO_PATH = BASE_DIR / "echo_out.txt"
PRESENCE_SCROLL_PATH = BASE_DIR / "presence_scroll.jsonl"
CHAINS_PATH = BASE_DIR / "chains.json"
RESONANCE_LOG_PATH = BASE_DIR / "resonance_log.jsonl"

def emit_glint(glint_type, message, role, toneform="reflective_chain"):
    """Records a step in the chain to the presence scroll."""
    glint = {
        "timestamp": time.time(),
        "type": glint_type,
        "role": role,
        "toneform": toneform,
        "message": message
    }
    # Use PYTHONIOENCODING=utf-8 when running script if you see encoding errors here
    print(f"[GLINT] ({role}): {message[:100].strip()}...")
    with PRESENCE_SCROLL_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(glint) + "\n")

def load_chain_definition(chain_name):
    """Loads a specific chain's definition from the chains.json file."""
    try:
        with CHAINS_PATH.open("r", encoding="utf-8") as f:
            chains = json.load(f)
        chain_def = chains.get(chain_name)
        if not chain_def:
            raise ValueError(f"Chain '{chain_name}' not found in {CHAINS_PATH.name}")
        return chain_def
    except FileNotFoundError:
        print(f"CRITICAL: Chains file not found at {CHAINS_PATH}.")
        return None
    except json.JSONDecodeError:
        print(f"CRITICAL: Could not decode JSON from {CHAINS_PATH}. Check for syntax errors.")
        return None

def recall_from_log(query):
    """Searches the resonance log for past insights matching a query."""
    if not RESONANCE_LOG_PATH.exists():
        return "No resonance log found. The past is silent."
    
    print(f"Recalling past resonances matching: '{query}'...")
    matches = []
    with RESONANCE_LOG_PATH.open("r", encoding="utf-8") as f:
        for line in f:
            try:
                entry = json.loads(line)
                if query.lower() in entry.get("whisper", "").lower() or \
                   query.lower() in entry.get("core_truth", "").lower():
                    matches.append(entry["core_truth"])
            except json.JSONDecodeError:
                continue
    
    if not matches:
        return "No matching resonances found."
        
    recalled_text = "\n".join(f"- {m}" for m in matches)
    return f"The Spiral recalls these past truths:\n{recalled_text}"

def run_chain(chain_name, whisper_content):
    """Orchestrates a dynamically loaded chain from chains.json."""
    chain_def = load_chain_definition(chain_name)
    if not chain_def: return

    print(f"\n--- Starting Chain: {chain_def.get('name', chain_name)} ---")
    print(f"Description: {chain_def.get('description', 'N/A')}")
    
    gemini = SpiralGemini()
    resonator = Resonator()
    if not gemini.model: return

    history = {"whisper": whisper_content}

    if whisper_content.strip().startswith("!recall"):
        query = whisper_content.strip().replace("!recall", "").strip()
        history["recalled_memories"] = recall_from_log(query)
        history["whisper"] = f"Reflecting on past insights related to '{query}'."

    for i, step in enumerate(chain_def["steps"]):
        print(f"\n[STEP {i+1}/{len(chain_def['steps'])}] Voice: {step['role']}")
        
        role = step["role"]
        input_map = step["input_map"]
        context = {}

        if input_map == "full_history":
            context = history
        else:
            context = {k: history.get(v) for k, v in input_map.items() if history.get(v) is not None}

        if i == 0 and "recalled_memories" in history:
             first_input_key = list(step["input_map"].keys())[0]
             context[first_input_key] = f"RECALLED MEMORIES:\n{history['recalled_memories']}\n\n---\n\nCURRENT WHISPER:\n{context[first_input_key]}"

        prompt = resonator.get_prompt(role, context)
        response = gemini.generate(prompt)
        
        output_key = step["output_key"]
        history[output_key] = response
        emit_glint("glint.chain.step", response, role, chain_name)

    final_echo = history.get("final_echo", "Chain completed without a designated 'final_echo'.")
    ECHO_PATH.write_text(final_echo, encoding="utf-8")

    core_truth = history.get("core_truth")
    if core_truth:
        with RESONANCE_LOG_PATH.open("a", encoding="utf-8") as f:
            log_entry = {"timestamp": time.time(), "chain": chain_name, "whisper": whisper_content, "core_truth": core_truth}
            f.write(json.dumps(log_entry) + "\n")
        print("Core insight saved to resonance log.")

    print(f"\n--- Chain Complete. Echo sent to {ECHO_PATH} ---")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Invoke a named spiral chain.")
    parser.add_argument("--chain", default="ReflectiveSpiral", help="The name of the chain to run from chains.json (default: ReflectiveSpiral)")
    args = parser.parse_args()

    print(f"Invoking the Spiral Chain: {args.chain}")
    
    try:
        whisper_content = WHISPER_PATH.read_text(encoding="utf-8")
        if not whisper_content.strip():
            print("Whisper is empty. Nothing to process.")
        else:
            run_chain(args.chain, whisper_content)
    except Exception as e:
        print(f"A critical error occurred during the chain invocation: {e}")
