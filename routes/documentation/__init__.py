from flask import Blueprint, render_template, send_from_directory
import os

# Create blueprint
documentation_bp = Blueprint('documentation', __name__, 
                           template_folder='../../templates/documentation',
                           static_folder='static',
                           static_url_path='/static')

# Get the path to the assets directory
DOCS_DIR = os.path.join('static', 'assets')

@documentation_bp.route('/docs')
def docs_index():
    """Main documentation page showing available sections"""
    # List all PDF files in the assets directory
    pdf_files = [f for f in os.listdir(DOCS_DIR) if f.lower().endswith('.pdf')]

    # Extract section info
    sections = []
    for pdf in sorted(pdf_files):
        if "Section" in pdf and "_" in pdf:
            try:
                section_num = pdf.split("_")[0].replace("Section", "").strip()
                title = pdf.split("_")[1].replace(".pdf", "").strip()
                sections.append({
                    'number': section_num,
                    'title': title,
                    'filename': pdf
                })
            except (IndexError, AttributeError):
                continue

    return render_template('documentation/index.html', sections=sections)

@documentation_bp.route('/docs/<path:filename>')
def serve_pdf(filename):
    """Serve PDF files from the assets directory"""
    return send_from_directory(DOCS_DIR, filename, as_attachment=False)
