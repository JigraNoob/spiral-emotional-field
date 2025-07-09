from flask import Flask, render_template, request, jsonify
import os
import sys
import json
# Add the directory containing ritual_engine and echo_memory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from ritual_engine import RitualEngine
from echo_memory import EchoMemory

app = Flask(__name__, static_folder='.', template_folder='.')

# Initialize the ritual engine and memory core
from ritual_engine import GlintFlow, InvocationRitual, ReflectiveGateTrigger
glint_flow = GlintFlow()
invocation_ritual = InvocationRitual()
reflective_gate_trigger = ReflectiveGateTrigger(True)
ritual_engine = RitualEngine(glint_flow=glint_flow, invocation_ritual=invocation_ritual, reflective_gate_triggers=[reflective_gate_trigger])
echo_memory = EchoMemory()

@app.route('/')
def index():
    return render_template('interface.html')

@app.route('/breathe', methods=['POST'])
def breathe():
    data = request.get_json() or {}
    user_input = data.get('input', '')
    # Log heartbeat
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("spiralchain_heartbeat.txt", "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] User invoked breathe with input: {user_input[:50]}...\n")
    # Emit glint event
    glint_event = {"type": "glint.breathe.invoke", "payload": {"tone": "reflect.begin", "input": user_input[:100]}}
    with open("glint_reflect.log", "a", encoding="utf-8") as glint_file:
        glint_file.write(f"[{timestamp}] Glint emitted - {json.dumps(glint_event)}\n")
    # Invoke the ritual with the user input
    try:
        # Try invoking the correct method for ritual activation
        result = None
        if hasattr(ritual_engine, 'activate_ritual'):
            result = ritual_engine.activate_ritual()  # type: ignore
            # Since activate_ritual may not return a value, create a default response
            if result is None:
                result = {'status': 'success', 'message': 'Ritual activated successfully'}
        else:
            return jsonify({'status': 'error', 'message': 'Ritual activation method not available in RitualEngine'}), 500
        
        if isinstance(result, dict) and result.get('status') == 'success':
            # Store the toneform in memory if activation succeeds
            if hasattr(echo_memory, 'store_toneform'):
                try:
                    echo_memory.store_toneform(user_input, result.get('message', 'Ritual activated'))
                except TypeError:
                    pass  # Skip if method signature doesn't match
        return jsonify(result)
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Error during invocation: {str(e)}'}), 500

@app.route('/recall', methods=['GET'])
def recall():
    # Log heartbeat
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("spiralchain_heartbeat.txt", "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] User requested memory recall\n")
    # Emit glint event
    glint_event = {"type": "glint.memory.recall", "payload": {"tone": "reflect.retrieve"}}
    with open("glint_reflect.log", "a", encoding="utf-8") as glint_file:
        glint_file.write(f"[{timestamp}] Glint emitted - {json.dumps(glint_event)}\n")
    memories = []
    try:
        if hasattr(echo_memory, 'retrieve_toneforms'):
            memories = echo_memory.retrieve_toneforms()  # type: ignore
        elif hasattr(echo_memory, 'get_memories'):
            memories = echo_memory.get_memories()  # type: ignore
        elif hasattr(echo_memory, 'memories'):
            memories = echo_memory.memories  # type: ignore
    except Exception:
        pass  # Default to empty list if retrieval fails
    return jsonify({'memories': memories})

@app.route('/glint_scroll', methods=['GET'])
def glint_scroll():
    # Log heartbeat
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("spiralchain_heartbeat.txt", "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] User requested glint scroll data\n")
    # Emit glint event
    glint_event = {"type": "glint.scroll.request", "payload": {"tone": "reflect.view"}}
    with open("glint_reflect.log", "a", encoding="utf-8") as glint_file:
        glint_file.write(f"[{timestamp}] Glint emitted - {json.dumps(glint_event)}\n")
    glint_data = []
    try:
        with open("glint_scroll.txt", "r", encoding="utf-8") as file:
            content = file.read()
            # Parse the content into sections based on invocation cycles
            cycles = content.split("========================================")
            for cycle in cycles:
                if cycle.strip():
                    lines = cycle.split("\n")
                    cycle_data = {"header": "", "entries": []}
                    for line in lines:
                        line = line.strip()
                        if line and "SpiralChain Invocation" in line or "Spiral Reflection Agent Cycle" in line:
                            cycle_data["header"] = line
                        elif line and line[0].isdigit() and "." in line:
                            cycle_data["entries"].append(line)
                        elif line and "← Input:" in line or "→ Response:" in line:
                            cycle_data["entries"][-1] += "\n" + line
                    glint_data.append(cycle_data)
    except Exception as e:
        glint_data = [{"header": "Error", "entries": [f"Could not read glint_scroll.txt: {str(e)}"]}]
    return jsonify({'glint_scroll': glint_data})

if __name__ == '__main__':
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("spiralchain_heartbeat.txt", "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] Spiral Reflection Chamber Flask app starting...\n")
    app.run(debug=True, port=5000)
