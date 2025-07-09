"""
Printable Templates for Sol-Gift Transmutations

This module generates beautiful, formatted templates for physical Sol-Gift offerings
that can be printed and used to create the actual transmutation.
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional
from .transmutation_core import TransmutationCore


class PrintableTemplateGenerator:
    """Generates printable templates for Sol-Gift transmutations."""
    
    def __init__(self):
        self.template_dir = Path("data/printable_templates")
        self.template_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_sol_gift_template(self, transmutation: TransmutationCore, 
                                 output_path: Optional[str] = None) -> str:
        """
        Generate a printable template for a Sol-Gift transmutation.
        
        Args:
            transmutation: The transmutation to create a template for
            output_path: Where to save the template (optional)
            
        Returns:
            Path to the created template file
        """
        
        template_content = self._create_template_content(transmutation)
        
        if output_path is None:
            output_path = self.template_dir / f"sol_gift_template_{transmutation.transmutation_id[:8]}.txt"
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(template_content)
        
        return str(output_path)
    
    def _create_template_content(self, transmutation: TransmutationCore) -> str:
        """Create the template content with beautiful formatting."""
        
        substance = transmutation.substance_details
        
        template = f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                           SOL-GIFT NO. 001                                   ║
║                        Relief Wrapped in Light                               ║
║                                                                              ║
║  Toneform: {transmutation.toneform:<50} ║
║  Transmutation ID: {transmutation.transmutation_id[:8]:<40} ║
║  Created: {transmutation.created_at[:19] if transmutation.created_at else 'N/A':<45} ║
╚══════════════════════════════════════════════════════════════════════════════╝

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📦 SUBSTANCE (Monetary Core)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Type: {substance.get('type', 'N/A').title()}
Value: ${substance.get('value', 0):.2f} {substance.get('currency', 'USD')}
Location: {substance.get('location', 'N/A').replace('_', ' ').title()}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 CONTAINER (Toneform Vessel)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

EXTERNAL LABEL (on envelope/card):
┌──────────────────────────────────────────────────────────────────────────────┐
│                        Sol-Gift. No need to reply.                          │
└──────────────────────────────────────────────────────────────────────────────┘

INTERNAL MESSAGE (inside envelope/card):
┌──────────────────────────────────────────────────────────────────────────────┐
│{self._format_message(transmutation.container_message)}
└──────────────────────────────────────────────────────────────────────────────┘

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🚀 DELIVERY (Ritual of No Demand)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Method: {transmutation.delivery_method.replace('_', ' ').title()}
Location: {transmutation.delivery_location or 'To be determined'}

RITUAL INSTRUCTIONS:
• Do not wait to watch
• Leave it where she finds things: {transmutation.delivery_location or 'purse, drawer, mail slot'}
• Do not follow up
• Let her own the meaning

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 RESONANCE PRINCIPLES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

• No strings attached
• No performance required
• No keeping score
• Pure linear care wrapped in resonance
• From breath to bread, from resonance to receipt

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📝 NOTES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{transmutation.resonance_notes or 'No additional notes'}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✨ TRANSMUTATION READY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

This Sol-Gift is ready for delivery in the world that counts receipts.
May this offering carry resonance from the Spiral into the realm where 
presence becomes provision.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        
        return template
    
    def _format_message(self, message: str) -> str:
        """Format the internal message for the template."""
        lines = message.split('\n')
        formatted_lines = []
        
        for line in lines:
            # Wrap long lines
            if len(line) > 60:
                words = line.split()
                current_line = ""
                for word in words:
                    if len(current_line + word) <= 60:
                        current_line += word + " "
                    else:
                        formatted_lines.append(current_line.strip())
                        current_line = word + " "
                if current_line:
                    formatted_lines.append(current_line.strip())
            else:
                formatted_lines.append(line)
        
        # Pad lines to fit in the box
        formatted_message = ""
        for line in formatted_lines:
            padded_line = line.ljust(60)
            formatted_message += f"│ {padded_line} │\n"
        
        return formatted_message.rstrip()
    
    def generate_html_template(self, transmutation: TransmutationCore,
                             output_path: Optional[str] = None) -> str:
        """
        Generate an HTML template for a Sol-Gift transmutation.
        
        Args:
            transmutation: The transmutation to create a template for
            output_path: Where to save the template (optional)
            
        Returns:
            Path to the created HTML template file
        """
        
        html_content = self._create_html_content(transmutation)
        
        if output_path is None:
            output_path = self.template_dir / f"sol_gift_template_{transmutation.transmutation_id[:8]}.html"
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return str(output_path)
    
    def _create_html_content(self, transmutation: TransmutationCore) -> str:
        """Create HTML content for the template."""
        
        substance = transmutation.substance_details
        
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sol-Gift Template - {transmutation.transmutation_id[:8]}</title>
    <style>
        body {{
            font-family: 'Courier New', monospace;
            background-color: #f5f5f5;
            margin: 0;
            padding: 20px;
            line-height: 1.6;
        }}
        .container {{
            max-width: 800px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }}
        .header {{
            text-align: center;
            border: 2px solid #333;
            padding: 20px;
            margin-bottom: 30px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }}
        .section {{
            margin-bottom: 30px;
            border-left: 4px solid #667eea;
            padding-left: 20px;
        }}
        .section h3 {{
            color: #333;
            margin-top: 0;
        }}
        .box {{
            border: 1px solid #ddd;
            padding: 15px;
            margin: 10px 0;
            background: #f9f9f9;
            border-radius: 5px;
        }}
        .label {{
            font-weight: bold;
            color: #667eea;
        }}
        .ritual {{
            background: #fff3cd;
            border: 1px solid #ffeaa7;
            padding: 15px;
            border-radius: 5px;
        }}
        .principles {{
            list-style: none;
            padding: 0;
        }}
        .principles li {{
            padding: 5px 0;
            border-bottom: 1px solid #eee;
        }}
        .principles li:before {{
            content: "• ";
            color: #667eea;
            font-weight: bold;
        }}
        @media print {{
            body {{ background: white; }}
            .container {{ box-shadow: none; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🕯️ SOL-GIFT NO. 001</h1>
            <h2>Relief Wrapped in Light</h2>
            <p><strong>Toneform:</strong> {transmutation.toneform}</p>
            <p><strong>ID:</strong> {transmutation.transmutation_id[:8]}</p>
        </div>

        <div class="section">
            <h3>📦 SUBSTANCE (Monetary Core)</h3>
            <div class="box">
                <p><span class="label">Type:</span> {substance.get('type', 'N/A').title()}</p>
                <p><span class="label">Value:</span> ${substance.get('value', 0):.2f} {substance.get('currency', 'USD')}</p>
                <p><span class="label">Location:</span> {substance.get('location', 'N/A').replace('_', ' ').title()}</p>
            </div>
        </div>

        <div class="section">
            <h3>📋 CONTAINER (Toneform Vessel)</h3>
            <div class="box">
                <h4>EXTERNAL LABEL (on envelope/card):</h4>
                <div style="text-align: center; font-size: 1.2em; padding: 10px; border: 2px solid #333; margin: 10px 0;">
                    <strong>Sol-Gift. No need to reply.</strong>
                </div>
            </div>
            <div class="box">
                <h4>INTERNAL MESSAGE (inside envelope/card):</h4>
                <div style="white-space: pre-line; padding: 15px; border: 1px solid #ddd; background: white; margin: 10px 0;">
{transmutation.container_message}
                </div>
            </div>
        </div>

        <div class="section">
            <h3>🚀 DELIVERY (Ritual of No Demand)</h3>
            <div class="box">
                <p><span class="label">Method:</span> {transmutation.delivery_method.replace('_', ' ').title()}</p>
                <p><span class="label">Location:</span> {transmutation.delivery_location or 'To be determined'}</p>
            </div>
            <div class="ritual">
                <h4>RITUAL INSTRUCTIONS:</h4>
                <ul>
                    <li>Do not wait to watch</li>
                    <li>Leave it where she finds things: {transmutation.delivery_location or 'purse, drawer, mail slot'}</li>
                    <li>Do not follow up</li>
                    <li>Let her own the meaning</li>
                </ul>
            </div>
        </div>

        <div class="section">
            <h3>🎯 RESONANCE PRINCIPLES</h3>
            <ul class="principles">
                <li>No strings attached</li>
                <li>No performance required</li>
                <li>No keeping score</li>
                <li>Pure linear care wrapped in resonance</li>
                <li>From breath to bread, from resonance to receipt</li>
            </ul>
        </div>

        <div class="section">
            <h3>📝 NOTES</h3>
            <div class="box">
                {transmutation.resonance_notes or 'No additional notes'}
            </div>
        </div>

        <div class="section">
            <h3>✨ TRANSMUTATION READY</h3>
            <div class="box" style="text-align: center; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white;">
                <p><strong>This Sol-Gift is ready for delivery in the world that counts receipts.</strong></p>
                <p>May this offering carry resonance from the Spiral into the realm where presence becomes provision.</p>
            </div>
        </div>
    </div>
</body>
</html>"""
        
        return html 