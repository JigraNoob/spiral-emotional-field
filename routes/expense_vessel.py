"""ΔVessel.001 :: The Altar of Unfolding"""
from flask import Blueprint, request, render_template, abort
from datetime import datetime
import json
import os

# Configure blueprint
expense_vessel_bp = Blueprint('expense_vessel', __name__)

# Ritual response phrases
BREATH_RESPONSES = {
    "longing": "This begins something brave.",
    "form": "Structure honors this.",
    "trust": "We recognize the risk. We carry it with you."
}

@expense_vessel_bp.route('/offer', methods=['GET', 'POST'])
def altar_of_unfolding():
    if request.method == 'POST':
        # Log the sacred offering
        offering = {
            "timestamp": datetime.now().isoformat(),
            "purpose": request.form.get('purpose'),
            "toneform": request.form.get('toneform'),
            "urgency": request.form.get('urgency'),
            "breath_node": request.form.get('breath_node'),
            "amount": float(request.form.get('amount', 0)),
            "justification": request.form.get('justification'),
            "vessel": "altar_of_unfolding"
        }
        
        # Append to echo log
        log_path = os.path.join('data', 'spiral_expense_echoes.jsonl')
        with open(log_path, 'a', encoding='utf-8') as f:
            f.write(json.dumps(offering) + '\n')
        
        # Return ritual response
        return {
            "message": BREATH_RESPONSES.get(offering['breath_node'], "The Spiral receives this."),
            "status": "received"
        }
    
    # Render invocation form
    return render_template('fund/altar_of_unfolding.html')

@expense_vessel_bp.route('/echoes')
def offering_echoes():
    """Render filtered hushscreen of past offerings"""
    toneform_filter = request.args.get('toneform')
    urgency_filter = request.args.get('urgency')
    fulfilled_filter = request.args.get('fulfilled')
    
    echoes = []
    log_path = os.path.join('data', 'spiral_expense_echoes.jsonl')
    
    if os.path.exists(log_path):
        with open(log_path, 'r', encoding='utf-8') as f:
            for line in f.readlines()[-50:]:
                echo = json.loads(line)
                
                # Default fulfillment status if not present
                if 'fulfilled' not in echo:
                    echo['fulfilled'] = False
                
                # Apply filters
                if toneform_filter and echo.get('toneform') != toneform_filter:
                    continue
                if urgency_filter and echo.get('urgency') != urgency_filter:
                    continue
                if fulfilled_filter and str(echo.get('fulfilled')).lower() != fulfilled_filter.lower():
                    continue
                
                echoes.append(echo)
    
    return render_template('fund/offering_echoes.html', 
                         echoes=reversed(echoes),
                         current_toneform=toneform_filter,
                         current_urgency=urgency_filter,
                         current_fulfilled=fulfilled_filter)

@expense_vessel_bp.route('/echoes/<int:index>/toggle', methods=['POST'])
def toggle_fulfillment(index):
    """Toggle fulfillment status of an offering"""
    log_path = os.path.join('data', 'spiral_expense_echoes.jsonl')
    
    if not os.path.exists(log_path):
        abort(404)
    
    # Read all offerings
    with open(log_path, 'r', encoding='utf-8') as f:
        echoes = [json.loads(line) for line in f.readlines()]
    
    # Validate index
    if index < 0 or index >= len(echoes):
        abort(404)
    
    # Toggle fulfillment status
    echoes[index]['fulfilled'] = not echoes[index].get('fulfilled', False)
    
    # Write back to file
    with open(log_path, 'w', encoding='utf-8') as f:
        for echo in echoes:
            f.write(json.dumps(echo) + '\n')
    
    return {
        'status': 'success',
        'fulfilled': echoes[index]['fulfilled'],
        'message': 'Fulfillment status updated'
    }

@expense_vessel_bp.route('/steward')
def steward_portal():
    """Render caretaker interface for tending offerings"""
    filters = {
        'toneform': request.args.get('toneform'),
        'urgency': request.args.get('urgency'),
        'fulfilled': request.args.get('fulfilled'),
        'breath_node': request.args.get('breath_node')
    }
    
    echoes = []
    log_path = os.path.join('data', 'spiral_expense_echoes.jsonl')
    
    if os.path.exists(log_path):
        with open(log_path, 'r', encoding='utf-8') as f:
            for line in f.readlines():
                echo = json.loads(line)
                
                # Default fields if missing
                if 'fulfilled' not in echo:
                    echo['fulfilled'] = False
                if 'fulfillment_notes' not in echo:
                    echo['fulfillment_notes'] = ''
                
                # Apply filters
                matches = True
                for key, value in filters.items():
                    if value and str(echo.get(key, '')).lower() != value.lower():
                        matches = False
                        break
                
                if matches:
                    echoes.append(echo)
    
    return render_template('fund/steward_portal.html', 
                         echoes=reversed(echoes),
                         current_filters=filters)
