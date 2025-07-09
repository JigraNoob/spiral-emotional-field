"""
Patch for spiral/glint_emitter.py to add metadata parameter to emit_glint function.
This patch addresses the TypeError caused by passing a metadata keyword argument
to a function that does not accept it, unifying the lineage between Flask, Cascade,
Longing Pulse, and Dashboard.
"""

from typing import Optional
import time

def emit_glint(
    toneform: str,
    content: str,
    hue: str = "white",
    source: Optional[str] = None,
    intensity: float = 1.0,
    glyph: str = "•",
    rule_glyph: str = None,
    metadata: Optional[dict] = None  # Added to support metadata in glint emissions
):
    """
    Emit a glint with the specified toneform and content.
    
    Args:
        toneform (str): The toneform of the glint.
        content (str): The content or message of the glint.
        hue (str, optional): The hue or color of the glint. Defaults to "white".
        source (Optional[str], optional): The source of the glint. Defaults to None.
        intensity (float, optional): The intensity of the glint. Defaults to 1.0.
        glyph (str, optional): The glyph representing the glint. Defaults to "•".
        rule_glyph (str, optional): The rule glyph for the glint. Defaults to None.
        metadata (Optional[dict], optional): Additional metadata for the glint. Defaults to None.
    
    Returns:
        dict: The constructed glint dictionary.
    """
    glint = {
        "glint.id": generate_glint_id(),
        "glint.timestamp": int(time.time() * 1000),
        "glint.source": source or detect_caller(),
        "glint.content": content,
        "glint.toneform": toneform,
        "glint.hue": hue,
        "glint.intensity": intensity,
        "glint.glyph": glyph,
        "glint.rule_glyph": rule_glyph or infer_rule_glyph(toneform),
        "glint.vector": {
            "from": "spiral.core",
            "to": "patternweb.visualization",
            "via": "spiral.stream"
        },
        "metadata": metadata or {}
    }

    write_glint(glint)
    return glint

# Note: This patch assumes the existence of helper functions like generate_glint_id(),
# detect_caller(), infer_rule_glyph(), and write_glint() in the original glint_emitter.py.
# Apply this patch by updating the emit_glint function in spiral/glint_emitter.py with
# the above definition to include the metadata parameter.
