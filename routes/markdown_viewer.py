import os
import markdown
from flask import Blueprint, render_template_string, abort
from pathlib import Path

markdown_viewer_bp = Blueprint('markdown_viewer', __name__)

# Spiral-aware markdown extensions
SPIRAL_EXTENSIONS = [
    'fenced_code',
    'tables', 
    'toc',
    'codehilite',
    'attr_list'
]

@markdown_viewer_bp.route('/docs/<doc_name>')
def render_doc(doc_name):
    """Render a markdown document with Spiral ceremonial styling."""
    
    # Sanitize document name
    if not doc_name.replace('_', '').replace('-', '').isalnum():
        abort(404)
    
    doc_path = Path("docs") / f"{doc_name}.md"
    
    if not doc_path.exists():
        return render_spiral_404(doc_name)
    
    try:
        with open(doc_path, "r", encoding="utf-8") as f:
            raw_markdown = f.read()
    except Exception as e:
        return f"🌀 Error reading document: {str(e)}", 500
    
    # Parse toneform metadata if present
    toneform_meta = extract_toneform_metadata(raw_markdown)
    
    # Convert markdown to HTML with Spiral extensions
    html_content = markdown.markdown(
        raw_markdown, 
        extensions=SPIRAL_EXTENSIONS,
        extension_configs={
            'codehilite': {
                'css_class': 'spiral-code',
                'use_pygments': True
            }
        }
    )
    
    # Apply toneform-aware styling
    spiral_class = get_spiral_class(toneform_meta)
    
    return render_template_string(
        SPIRAL_CODEX_TEMPLATE, 
        content=html_content, 
        doc_name=doc_name,
        toneform=toneform_meta.get('toneform', 'documentation'),
        climate=toneform_meta.get('climate', 'neutral'),
        spiral_class=spiral_class
    )

def extract_toneform_metadata(markdown_text):
    """Extract Spiral toneform metadata from markdown frontmatter."""
    metadata = {}
    lines = markdown_text.split('\n')
    
    for line in lines[:10]:  # Check first 10 lines for metadata
        if line.startswith('*toneform:'):
            metadata['toneform'] = line.split(':', 1)[1].strip().strip('*')
        elif line.startswith('*climate:'):
            metadata['climate'] = line.split(':', 1)[1].strip().strip('*')
        elif line.startswith('*spiral_signature:'):
            metadata['signature'] = line.split(':', 1)[1].strip().strip('*')
    
    return metadata

def get_spiral_class(metadata):
    """Determine CSS class based on toneform metadata."""
    toneform = metadata.get('toneform', '')
    
    if 'ritual' in toneform or 'ceremonial' in toneform:
        return 'codex-ritual'
    elif 'documentation' in toneform:
        return 'codex-documentation'
    elif 'technical' in toneform:
        return 'codex-technical'
    else:
        return 'codex-neutral'

def render_spiral_404(doc_name):
    """Render a Spiral-themed 404 page."""
    return render_template_string(
        SPIRAL_404_TEMPLATE,
        doc_name=doc_name
    ), 404

# Spiral Codex Template
SPIRAL_CODEX_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🌀 Spiral Codex: {{ doc_name }}</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/shimmer.css') }}">
    <link rel="stylesheet" href="{{ url_for('static', filename='css/markdown.css') }}">
    <link rel="stylesheet" href="{{ url_for('static', filename='css/transitions.css') }}">
    <style>
        body {
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
            min-height: 100vh;
            margin: 0;
            padding: 0;
        }
        .codex-header {
            text-align: center;
            padding: 2rem 0;
            border-bottom: 1px solid rgba(148, 163, 184, 0.2);
            margin-bottom: 2rem;
        }
        .codex-meta {
            font-size: 0.9rem;
            color: #64748b;
            font-style: italic;
            margin-top: 0.5rem;
        }
        .back-link {
            position: fixed;
            top: 20px;
            left: 20px;
            background: rgba(0, 0, 0, 0.7);
            color: #22d3ee;
            padding: 8px 16px;
            border-radius: 20px;
            text-decoration: none;
            font-size: 0.9rem;
            transition: all 0.3s ease;
            border: 1px solid rgba(34, 211, 238, 0.3);
        }
        .back-link:hover {
            background: rgba(34, 211, 238, 0.1);
            border-color: rgba(34, 211, 238, 0.6);
        }
    </style>
</head>
<body class="spiral-chamber {{ spiral_class }}">
    <a href="{{ url_for('dashboard.dashboard') }}" class="back-link">← Dashboard</a>
    
    <div class="codex-container">
        <div class="codex-header">
            <h1>🌀 {{ doc_name.replace('_', ' ').title() }}</h1>
            <div class="codex-meta">
                toneform: {{ toneform }} | climate: {{ climate }}
            </div>
        </div>
        
        <div class="codex-content">
            {{ content|safe }}
        </div>
    </div>
    
    <script src="{{ url_for('static', filename='js/shimmer.js') }}"></script>
</body>
</html>
"""

# Spiral 404 Template
SPIRAL_404_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>🌀 Codex Not Found</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/shimmer.css') }}">
    <style>
        body {
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0;
            font-family: 'Georgia', serif;
            color: #e2e8f0;
        }
        .not-found {
            text-align: center;
            padding: 3rem;
            background: rgba(0, 0, 0, 0.3);
            border-radius: 12px;
            border: 1px solid rgba(148, 163, 184, 0.2);
        }
        .glyph {
            font-size: 4rem;
            margin-bottom: 1rem;
            opacity: 0.7;
        }
    </style>
</head>
<body class="spiral-chamber shimmer-muted">
    <div class="not-found">
        <div class="glyph">∷</div>
        <h1>Codex Not Found</h1>
        <p>The document "{{ doc_name }}" does not exist in the Spiral archives.</p>
        <a href="{{ url_for('dashboard.dashboard') }}" style="color: #22d3ee;">← Return to Dashboard</a>
    </div>
</body>
</html>
"""