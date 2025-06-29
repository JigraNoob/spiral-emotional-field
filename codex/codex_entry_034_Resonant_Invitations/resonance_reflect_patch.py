
@resonance_bp.route('/get_dominant_resonance')
def get_dominant_resonance():
    import jsonlines
    from collections import Counter
    from datetime import datetime, timedelta

    filepath = 'resonance_keys.jsonl'
    now = datetime.utcnow()
    cutoff = now - timedelta(minutes=60)
    codes = []

    try:
        with jsonlines.open(filepath) as reader:
            for obj in reader:
                ts = datetime.strptime(obj["timestamp"], "%Y-%m-%dT%H:%M:%S")
                if ts > cutoff:
                    codes.append(obj["breath_code"])
    except Exception as e:
        return jsonify({"error": str(e)})

    if not codes:
        return jsonify({"dominant_tone": "default"})

    most_common = Counter(codes).most_common(1)[0][0]
    return jsonify({"dominant_tone": most_common})
