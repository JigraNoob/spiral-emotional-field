def log_upgrade(upgrade_id, description, components):
    """Log a Spiral upgrade."""
    timestamp = datetime.now().isoformat()
    upgrade_record = {
        "id": upgrade_id,
        "timestamp": timestamp,
        "description": description,
        "components": components
    }
    
    # Log to file
    with open("c:\\spiral\\logs\\upgrade_log.jsonl", "a") as f:
        json.dump(upgrade_record, f)
        f.write("\n")
    
    # Emit upgrade glint
    emit_glint(
        phase="exhale",
        toneform="spiral.upgrade",
        content=f"Upgrade {upgrade_id} logged: {description}",
        metadata=upgrade_record
    )

    print(f"🌀 Upgrade {upgrade_id} logged successfully.")

# Log the current upgrade
log_upgrade(
    "ΔUPGRADE.0001",
    "Spiral Runtime Stabilization Begun",
    [
        "glint_cache.py",
        "resonance_lock.py",
        "pulse_sync_listener.py",
        "spiral_pulse_emitter.py"
    ]
)