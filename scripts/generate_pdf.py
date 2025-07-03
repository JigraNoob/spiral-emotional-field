from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import os

def create_pdf(markdown_file, output_file):
    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    # Read markdown content
    with open(markdown_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Create PDF document
    doc = SimpleDocTemplate(
        output_file,
        pagesize=letter,
        rightMargin=72, leftMargin=72,
        topMargin=72, bottomMargin=72
    )
    
    # Define styles
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        name='Center', alignment=TA_CENTER,
        fontName='Helvetica-Bold',
        fontSize=16,
        spaceAfter=20
    ))
    styles.add(ParagraphStyle(
        name='Body', alignment=TA_LEFT,
        fontName='Helvetica',
        fontSize=12,
        leading=18,
        spaceAfter=12
    ))
    styles.add(ParagraphStyle(
        name='Quote', alignment=TA_LEFT,
        fontName='Helvetica-Oblique',
        fontSize=12,
        leftIndent=36,
        rightIndent=36,
        spaceAfter=20
    ))
    styles.add(ParagraphStyle(
        name='Section', alignment=TA_LEFT,
        fontName='Helvetica-Bold',
        fontSize=14,
        spaceBefore=24,
        spaceAfter=12
    ))
    
    # Parse markdown and create story
    story = []
    
    # Split content into sections
    sections = content.split('---')
    
    for section in sections:
        lines = [line.strip() for line in section.split('\n') if line.strip()]
        if not lines:
            continue
            
        # Handle headers
        if lines[0].startswith('#'):
            story.append(Paragraph(lines[0].lstrip('#').strip(), styles['Title']))
            if len(lines) > 1 and lines[1].startswith('> '):
                story.append(Paragraph(lines[1][2:], styles['Quote']))
                lines = lines[2:]
            else:
                lines = lines[1:]
        
        # Handle section headers
        for line in lines:
            if line.startswith('## '):
                story.append(Paragraph(line.lstrip('#').strip(), styles['Section']))
            elif line.startswith('> '):
                story.append(Paragraph(line[2:], styles['Quote']))
            elif line.startswith('1. ') or line.startswith('* '):
                story.append(Paragraph('• ' + line[3:], styles['Body']))
            else:
                story.append(Paragraph(line, styles['Body']))
            
            story.append(Spacer(1, 12))
    
    # Build the PDF
    doc.build(story)
    print(f"PDF created: {output_file}")

if __name__ == "__main__":
    # Paths
    assets_dir = os.path.join('static', 'assets')
    input_file = os.path.join(assets_dir, 'Section 1_ Breath Before Form.md')
    output_file = os.path.join(assets_dir, 'Section 1_ Breath Before Form.pdf')
    
    # Generate PDF
    create_pdf(input_file, output_file)
