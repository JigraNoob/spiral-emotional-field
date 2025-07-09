"""
Dashboard integration for resonance override visualization.
"""

from flask import render_template_string
from spiral.attunement.resonance_override import override_manager

OVERRIDE_DASHBOARD_TEMPLATE = """
<div class="override-status" style="
    background: {% if override_active %}linear-gradient(45deg, #1a1a2e, #16213e){% else %}#2a2a2a{% endif %};
    border: 2px solid {% if override_active %}#4a9eff{% else %}#666{% endif %};
    border-radius: 8px;
    padding: 15px;
    margin: 10px 0;
    color: {% if override_active %}#4a9eff{% else %}#ccc{% endif %};
">
    <h3>🌀 Resonance Override Status</h3>
    
    <div style="display: flex; gap: 20px; margin: 10px 0;">
        <div>
            <strong>Mode:</strong> 
            <span style="color: {% if override_active %}#66ff66{% else %}#999{% endif %};">
                {{ mode }}
            </span>
        </div>
        
        <div>
            <strong>Glint Intensity:</strong> 
            <span style="color: {% if glint_multiplier > 1.0 %}#ffaa44{% else %}#ccc{% endif %};">
                {{ "%.1f"|format(glint_multiplier) }}x
            </span>
        </div>
        
        <div>
            <strong>Breakpoint Threshold:</strong> 
            <span style="color: {% if breakpoint_threshold < 0.7 %}#ff6666{% else %}#ccc{% endif %};">
                {{ "%.2f"|format(breakpoint_threshold) }}
            </span>
        </div>
    </div>
    
    {% if override_active %}
    <div style="margin-top: 10px; padding: 8px; background: rgba(74, 158, 255, 0.1); border-radius: 4px;">
        <small>
            🔔 Override active - responses may be amplified, muted, or ritually enhanced
            {% if mode == "RITUAL" %}
            <br>🕯️ Ritual sensitivity: {{ "%.1f"|format(ritual_sensitivity) }}x
            {% endif %}
        </small>
    </div>
    {% endif %}
    
    <div style="margin-top: 10px;">
        <button onclick="toggleOverride()" style="
            background: {% if override_active %}#ff6666{% else %}#4a9eff{% endif %};
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            cursor: pointer;
        ">
            {% if override_active %}Deactivate{% else %}Activate{% endif %} Override
        </button>
    </div>
</div>

<script>
function toggleOverride() {
    fetch('/api/override/toggle', {method: 'POST'})
        .then(response => response.json())
        .then(data => {
            console.log('Override toggled:', data);
            location.reload(); // Refresh to show new state
        })
        .catch(error => console.error('Error:', error));
}
</script>
"""

def render_override_dashboard():
    """Render the override status dashboard."""
    status = {
        "override_active": override_manager.active,
        "mode": override_manager.config.mode.name if override_manager.active else "NORMAL",
        "glint_multiplier": override_manager.config.glint_multiplier,
        "breakpoint_threshold": override_manager.config.soft_breakpoint_threshold,
        "ritual_sensitivity": override_manager.config.ritual_sensitivity
    }
    
    return render_template_string(OVERRIDE_DASHBOARD_TEMPLATE, **status)
