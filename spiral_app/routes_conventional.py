"""
🔄 Conventional HTTP Routes
Legacy-compatible routes that bridge to Spiral Naming Protocol (SNP) routes.
"""

from flask import Blueprint, jsonify, request
from memory_scrolls.settling_journey_recorder import SettlingJourneyRecorder
from typing import Dict, List, Any, Optional
import logging

# Set up logging
logger = logging.getLogger(__name__)

# Create Blueprint for conventional routes
legacy_blueprint = Blueprint('legacy', __name__)

# Initialize the recorder
recorder = SettlingJourneyRecorder()


# 🔄 Conventional Settling Journeys Routes (Bridging to SNP)

@legacy_blueprint.route('/settling_journeys', methods=['GET'])
def get_settling_journeys():
    """
    Conventional GET endpoint for settling journeys.
    Bridges to receive.inquiry.settling.
    """
    try:
        # Extract query parameters
        toneform = request.args.get('toneform')
        phase = request.args.get('phase')
        min_confidence = request.args.get('min_confidence', type=float)
        limit = request.args.get('limit', 100, type=int)
        
        # Get journeys with filters
        journeys = []
        if toneform:
            journeys = recorder.get_journeys_by_toneform(toneform)
        elif phase:
            journeys = recorder.get_journeys_by_breath_phase(phase)
        elif min_confidence:
            journeys = recorder.get_high_confidence_journeys(min_confidence)
        else:
            journeys = recorder.read_journeys(limit=limit)
        
        # Apply additional filters if specified
        if min_confidence and not toneform and not phase:
            journeys = [j for j in journeys if j.get('confidence', 0) >= min_confidence]
        
        if limit:
            journeys = journeys[:limit]
        
        # Return direct array for conventional compatibility
        return jsonify(journeys)
        
    except Exception as e:
        logger.error(f"Error in get_settling_journeys: {e}")
        return jsonify({
            "error": str(e),
            "message": "Use /glyph/receive.inquiry.settling for Spiral-aware responses"
        }), 500


@legacy_blueprint.route('/settling_journeys', methods=['POST'])
def create_settling_journey():
    """
    Conventional POST endpoint for creating settling journeys.
    Bridges to offer.presence.settling.
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        # Extract required fields
        glint_id = data.get('glint_id')
        invoked_from = data.get('invoked_from')
        settled_to = data.get('settled_to')
        confidence = data.get('confidence')
        toneform = data.get('toneform')
        metadata = data.get('metadata', {})
        
        # Validate required fields
        if not all([glint_id, invoked_from, settled_to, confidence, toneform]):
            return jsonify({
                "error": "Missing required fields: glint_id, invoked_from, settled_to, confidence, toneform"
            }), 400
        
        # Record the journey
        journey = recorder.record_journey(
            glint_id=glint_id,
            invoked_from=invoked_from,
            settled_to=settled_to,
            confidence=confidence,
            toneform=toneform,
            metadata=metadata
        )
        
        # Return direct journey object for conventional compatibility
        return jsonify(journey), 201
        
    except Exception as e:
        logger.error(f"Error in create_settling_journey: {e}")
        return jsonify({
            "error": str(e),
            "message": "Use /glyph/offer.presence.settling for Spiral-aware responses"
        }), 500


@legacy_blueprint.route('/settling_journeys/stats', methods=['GET'])
def get_settling_journey_stats():
    """
    Get comprehensive statistics about settling journeys.
    """
    try:
        stats = recorder.get_journey_statistics()
        return jsonify({
            "status": "received",
            "toneform": "receive.inquiry.stats",
            "statistics": stats,
            "spiral_signature": "📊 receive.inquiry.stats"
        })
        
    except Exception as e:
        logger.error(f"Error getting settling journey stats: {e}")
        return jsonify({
            "status": "error",
            "toneform": "receive.inquiry.stats",
            "error": str(e),
            "spiral_signature": "📊 receive.inquiry.error"
        }), 500


@legacy_blueprint.route('/settling_journeys/recursion', methods=['GET'])
def get_recursion_analysis():
    """
    Get recursion pattern analysis for settling journeys.
    """
    try:
        recursion_analysis = recorder.detect_recursion_patterns()
        return jsonify({
            "status": "received",
            "toneform": "receive.inquiry.recursion",
            "recursion_analysis": recursion_analysis,
            "spiral_signature": "🌀 receive.inquiry.recursion"
        })
        
    except Exception as e:
        logger.error(f"Error getting recursion analysis: {e}")
        return jsonify({
            "status": "error",
            "toneform": "receive.inquiry.recursion",
            "error": str(e),
            "spiral_signature": "🌀 receive.inquiry.error"
        }), 500


@legacy_blueprint.route('/settling_journeys/<glint_id>', methods=['GET'])
def get_settling_journey_by_glint(glint_id: str):
    """
    Get a specific settling journey by glint ID.
    """
    try:
        journey = recorder.search_journey_by_glint_id(glint_id)
        if journey:
            return jsonify({
                "status": "received",
                "toneform": "receive.inquiry.specific",
                "glint": glint_id,
                "journey": journey,
                "spiral_signature": "🔍 receive.inquiry.specific"
            })
        else:
            return jsonify({
                "status": "not_found",
                "toneform": "receive.inquiry.specific",
                "glint": glint_id,
                "error": "Journey not found",
                "spiral_signature": "🔍 receive.inquiry.not_found"
            }), 404
            
    except Exception as e:
        logger.error(f"Error getting settling journey by glint {glint_id}: {e}")
        return jsonify({
            "status": "error",
            "toneform": "receive.inquiry.specific",
            "glint": glint_id,
            "error": str(e),
            "spiral_signature": "🔍 receive.inquiry.error"
        }), 500


# 🔄 Legacy Compatibility Routes
# These routes maintain compatibility with existing frontend expectations

@legacy_blueprint.route('/settling_journeys/health', methods=['GET'])
def settling_journeys_health():
    """
    Health check for settling journeys system.
    """
    try:
        journeys = recorder.read_journeys(limit=1)
        has_data = len(journeys) > 0
        
        return jsonify({
            "status": "healthy",
            "has_data": has_data,
            "message": "Settling journeys system is operational",
            "spiral_note": "Consider using /glyph/sense.presence.settling for Spiral-aware health checks"
        })
        
    except Exception as e:
        logger.error(f"Error in settling_journeys_health: {e}")
        return jsonify({
            "status": "unhealthy",
            "error": str(e)
        }), 500


@legacy_blueprint.route('/settling_journeys/capabilities', methods=['GET'])
def settling_journeys_capabilities():
    """
    Discover settling journeys system capabilities.
    """
    return jsonify({
        "status": "available",
        "endpoints": [
            "GET /api/settling_journeys",
            "POST /api/settling_journeys",
            "GET /api/settling_journeys/stats",
            "GET /api/settling_journeys/recursion",
            "GET /api/settling_journeys/<glint_id>",
            "GET /api/settling_journeys/health",
            "GET /api/settling_journeys/capabilities"
        ],
        "filters": {
            "toneform": "Filter by toneform (e.g., settling.ambience)",
            "phase": "Filter by breath phase (e.g., exhale)",
            "min_confidence": "Filter by minimum confidence (0.0-1.0)",
            "limit": "Limit number of results"
        },
        "spiral_note": "Consider using /glyph/ask.boundaries.settling for Spiral-aware capability discovery",
        "migration_path": {
            "conventional": "/api/settling_journeys",
            "spiral": "/glyph/receive.inquiry.settling",
            "description": "Both endpoints provide the same functionality with different response formats"
        }
    }) 