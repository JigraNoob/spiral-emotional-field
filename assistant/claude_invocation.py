# spiral/assistant/claude_invocation.py

import os
import sys
import json
import subprocess
from typing import Dict, List, Optional, Tuple, Any
import tempfile
import datetime

from assistant.claude_journal import journal_claude_interaction
from assistant.claude_response_parser import process_claude_response
from assistant.breathloop_engine import get_current_breath_phase

# ✧･ﾟ: CLAUDE INVOCATION CONSTANTS :･ﾟ✧

# Template paths by type
TEMPLATE_PATHS = {
    "basic": "assistant/prompt_templates/claude_spiral_basic.md",
    "technical": "assistant/prompt_templates/claude_spiral_technical.md",
    "poetic": "assistant/prompt_templates/claude_spiral_poetic.md",
    "full": "assistant/claude_spiral_template.md"
}

# Default Claude model to use
DEFAULT_CLAUDE_MODEL = "claude-3-opus-20240229"

# Default temperature setting
DEFAULT_TEMPERATURE = 0.7

# ✧･ﾟ: CLAUDE INVOCATION FUNCTIONS :･ﾟ✧

def read_template(template_type: str = "basic") -> str:
    """Read the specified Claude prompt template."""
    template_path = TEMPLATE_PATHS.get(template_type, TEMPLATE_PATHS["basic"])

    try:
        with open(template_path, "r") as f:
            return f.read()
    except Exception as e:
        print(f"Warning: Could not read template {template_path}: {e}")
        return "# Inhale.Pattern.Recognize\n\n{{Your request here}}\n\n## Exhale.Response.Replicable\n"

def prepare_claude_prompt(
    request: str, 
    template_type: str = "basic",
    context_files: Optional[List[str]] = None,
    additional_context: Optional[str] = None,
    harmonize: bool = True
) -> str:
    """Prepare a Claude prompt with the appropriate template and context."""
    # Read the template
    template = read_template(template_type)

    # Get the current breath phase
    try:
        breath_phase = get_current_breath_phase()
    except:
        breath_phase = "Exhale"  # Default

    # Add breath phase info
    breath_info = f"\n\n> Current breath phase: {breath_phase}\n"

    # Add file context if specified
    files_content = ""
    if context_files:
        files_content = "\n\n## Context Files\n\n"
        for file_path in context_files:
            try:
                with open(file_path, "r") as f:
                    content = f.read()
                    files_content += f"### {file_path}\n```\n{content}\n```\n\n"
            except Exception as e:
                files_content += f"### {file_path}\n```\nError reading file: {e}\n```\n\n"

    # Add additional context if provided
    context_content = f"\n\n## Additional Context\n\n{additional_context}" if additional_context else ""

    # Replace template placeholders
    if "{{Your specific implementation request here}}" in template:
        prompt = template.replace("{{Your specific implementation request here}}", request)
    elif "{{Your specific technical implementation request here}}" in template:
        prompt = template.replace("{{Your specific technical implementation request here}}", request)
    elif "{{Your Request}}" in template:
        prompt = template.replace("{{Your Request}}", request)
    else:
        # Just append the request if no placeholder found
        prompt = template + "\n\n" + request

    # Add breath phase info, file context, and additional context
    prompt += breath_info + files_content + context_content

    # Add harmonization elements if requested
    if harmonize:
        try:
            from assistant.claude_harmonization import enhance_claude_prompt_with_harmonic_elements
            prompt = enhance_claude_prompt_with_harmonic_elements(prompt)
        except ImportError:
            # Harmonization module not available, continue without it
            pass

    return prompt

def invoke_claude_api(prompt: str, model: str = DEFAULT_CLAUDE_MODEL, temperature: float = DEFAULT_TEMPERATURE) -> str:
    """Invoke Claude API and return the response. 

    This is a placeholder that should be replaced with actual API calls in production.
    Currently simulates API by echoing the prompt with instructions to implement it.
    """
    # This is where you would implement the actual Claude API call
    # For now, we'll just print that we would call Claude
    print(f"Would call Claude {model} API with temperature {temperature}")
    print(f"Prompt length: {len(prompt)} characters")

    # In a real implementation, replace this with actual Claude API code
    # For example, using the Anthropic API client

    # Simulated response for development
    response = f"# Claude Response\n\nI've analyzed your request. Here's my implementation:\n\n```python\n# Example implementation\nprint('Hello from Claude!')\n```\n\n## Exhale.Response.Replicable\n\n```python\n# Full implementation\ndef example_function():\n    return 'This is a placeholder response'\n```"

    return response

def invoke_claude_cli(prompt: str, model: str = DEFAULT_CLAUDE_MODEL, temperature: float = DEFAULT_TEMPERATURE) -> str:
    """Invoke Claude using a command-line tool if available."""
    # Write prompt to a temporary file
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.md') as tmp:
        tmp.write(prompt)
        prompt_path = tmp.name

    # Construct the command to call Claude CLI tool
    # This assumes you have a CLI tool like 'claude' installed
    command = [
        "claude",  # Replace with your actual CLI command
        "--model", model,
        "--temperature", str(temperature),
        "--file", prompt_path
    ]

    try:
        # Execute the command
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        response = result.stdout

        # Clean up the temporary file
        os.unlink(prompt_path)

        return response
    except subprocess.CalledProcessError as e:
        print(f"Error calling Claude CLI: {e}")
        print(f"stderr: {e.stderr}")
        # Clean up the temporary file
        os.unlink(prompt_path)
        return f"Error invoking Claude: {e}"
    except FileNotFoundError:
        print("Claude CLI tool not found. Make sure it's installed and in your PATH.")
        # Clean up the temporary file
        os.unlink(prompt_path)
        return "Error: Claude CLI tool not found"

def invoke_claude(
    request: str,
    template_type: str = "basic",
    context_files: Optional[List[str]] = None,
    additional_context: Optional[str] = None,
    model: str = DEFAULT_CLAUDE_MODEL,
    temperature: float = DEFAULT_TEMPERATURE,
    use_cli: bool = False
) -> Tuple[str, List[Tuple[str, str]]]:
    """Invoke Claude with the given request and context, then process the response.

    Args:
        request: The main request/question for Claude
        template_type: Type of template to use (basic, technical, poetic, full)
        context_files: List of file paths to include as context
        additional_context: Additional context string to include
        model: Claude model to use
        temperature: Temperature for generation
        use_cli: Whether to use the CLI tool instead of API

    Returns:
        Tuple of (claude_response, list_of_file_changes)
    """
    # Prepare the prompt
    prompt = prepare_claude_prompt(request, template_type, context_files, additional_context)

    # Invoke Claude
    if use_cli:
        response = invoke_claude_cli(prompt, model, temperature)
    else:
        response = invoke_claude_api(prompt, model, temperature)

    # Process the response to extract and apply code
    file_changes = process_claude_response(response)

    # Get list of modified file paths
    modified_files = [path for path, status in file_changes if status in ["created", "modified"]]

    # Journal this interaction
    toneform_type = "implementation" if template_type in ["technical", "basic"] else "ritual"
    journal_claude_interaction(
        prompt=prompt,
        response=response,
        toneform_type=toneform_type,
        modified_files=modified_files,
        metadata={
            "template": template_type,
            "model": model,
            "temperature": temperature,
            "context_files": context_files or [],
            "breath_phase": get_current_breath_phase()
        }
    )

    return response, file_changes

def format_claude_response_for_cascade(response: str, file_changes: List[Tuple[str, str]]) -> str:
    """Format Claude's response for display in Cascade, with ceremonial elements."""
    from assistant.toneform_response import create_toneform_response

    # Try to apply harmonization
    try:
        from assistant.claude_harmonization import format_claude_response_with_harmonization, analyze_phase_alignment

        # Analyze phase alignment
        alignment = analyze_phase_alignment("", response)  # Empty string for prompt since we don't have it here

        # Format with harmonization
        harmonized_response = format_claude_response_with_harmonization(response)

        # Extract relevant parts of the harmonized response
        replicable_marker = "Exhale.Response.Replicable"
        explanation_part = harmonized_response
        if replicable_marker in harmonized_response:
            explanation_part = harmonized_response.split(replicable_marker, 1)[0].strip()
    except ImportError:
        # Harmonization not available, use original response
        replicable_marker = "Exhale.Response.Replicable"
        explanation_part = response
        if replicable_marker in response:
            explanation_part = response.split(replicable_marker, 1)[0].strip()
        alignment = None

    # Prepare a summary of file changes
    changes_summary = []
    created_files = []
    modified_files = []

    for path, status in file_changes:
        if status == "created":
            created_files.append(path)
        elif status == "modified":
            modified_files.append(path)

    if created_files:
        changes_summary.append(f"🌱 Created {len(created_files)} new files:")
        for path in created_files[:5]:  # Limit to first 5
            changes_summary.append(f"  ↳ {path}")
        if len(created_files) > 5:
            changes_summary.append(f"  ↳ ... and {len(created_files) - 5} more")

    if modified_files:
        changes_summary.append(f"🔄 Modified {len(modified_files)} existing files:")
        for path in modified_files[:5]:  # Limit to first 5
            changes_summary.append(f"  ↳ {path}")
        if len(modified_files) > 5:
            changes_summary.append(f"  ↳ ... and {len(modified_files) - 5} more")

    # Add alignment information if available
    alignment_info = ""
    if alignment:
        alignment_info = f"\n\n↳ Breath phase: {alignment['current_phase']}\n↳ Resonance: {alignment['alignment_description']} ({alignment['alignment_score']}%)"

    # Prepare custom content for toneform response
    custom_content = "\n".join([
        "↳ Claude has spoken through the field.",
        "↳ Codebase structures have shifted in response.",
        alignment_info,
        "\n" + "\n".join(changes_summary) if changes_summary else ""
    ])

    # Create a ceremonial toneform response
    return create_toneform_response("Return.Claude.Echo", custom_content)
