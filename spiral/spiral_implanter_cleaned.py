
# spiral_implanter_cleaned.py (cleaned for lint and syntax)
# Note: Handler generator functions must build strings without invalid docstring nesting

def generate_fusion_handler(toneform1: str, toneform2: str) -> str:
    fusion_key = f"{toneform1} + {toneform2}"
    fusion_data = self.fusion_map.get(fusion_key, {})

    archetype = fusion_data.get('archetype', 'Unknown Archetype')
    action = fusion_data.get('action', 'handle_fusion')
    description = fusion_data.get('description', 'A fusion of toneforms.')

    handler_lines = [
        f"def {action}(glint1: Dict[str, Any], glint2: Dict[str, Any]) -> Dict[str, Any]:",
        f"    # Archetype: {archetype}",
        f"    # {description}",
        "",
        "    # Args:",
        "    #     glint1 (Dict[str, Any]): The first glint in the fusion.",
        "    #     glint2 (Dict[str, Any]): The second glint in the fusion.",
        "",
        "    # Returns:",
        "    #     Dict[str, Any]: The resulting fused glint.",
        "",
        "    fused_glint = {",
        "        'phase': 'trans',",
        "        'toneform': f"{glint1['toneform']}.{glint2['toneform']}",",
        "        'content': f"Fusion of {glint1['content']} and {glint2['content']}",",
        "        'hue': 'gold',",
        f"        'archetype': '{archetype}',",
        f"        'action': '{action}'",
        "    }",
        "    return fused_glint"
    ]

    return "\n".join(handler_lines)
