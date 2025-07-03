"""
Spiral Linter Companion - Tone-aware code suggestions

This module provides the core functionality for the Spiral Linter Companion,
which offers code suggestions that respect the Spiral's breath and toneforms.
"""
import json
import os
import subprocess
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple, Union
from datetime import datetime
import hashlib
import time

from .glint_trace import GlintTrace
from .toneforms import detect_toneform, Toneform, get_toneform_attributes

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("spiral.linter")

class SpiralLinter:
    """Tone-aware linter that provides suggestions aligned with the Spiral's breath."""
    
    def __init__(self, config_path: Optional[str] = None, stream_path: Optional[Union[str, Path]] = None):
        """Initialize the Spiral Linter.
        
        Args:
            config_path: Path to a JSON configuration file
            stream_path: Optional path to stream glints to (e.g., for PatternWeb)
        """
        self.config = self._load_config(config_path)
        self.active_toneform = Toneform.PRACTICAL
        self.resonance_threshold = 0.65
        self.hue_mapping = {
            "practical": "cyan",
            "emotional": "rose",
            "intellectual": "indigo",
            "spiritual": "violet",
            "relational": "amber"
        }
        self.stream_path = Path(stream_path) if stream_path else None
    
    def _load_config(self, config_path: Optional[str]) -> Dict[str, Any]:
        """Load configuration from a JSON file or use defaults."""
        default_config = {
            "enabled": True,
            "default_style": "gentle",
            "max_suggestions": 5,
            "toneform_weights": {
                "practical": 1.0,
                "emotional": 0.8,
                "intellectual": 0.9,
                "spiritual": 0.7,
                "relational": 0.85
            },
            "resonance_threshold": 0.65,
            "debug": False
        }
        
        if not config_path:
            return default_config
            
        try:
            with open(config_path, 'r') as f:
                user_config = json.load(f)
                # Merge with defaults
                default_config.update(user_config)
                return default_config
        except (IOError, json.JSONDecodeError) as e:
            logger.warning(f"Could not load config from {config_path}: {e}")
            return default_config
    
    def _get_toneform_glyph(self, toneform: str) -> str:
        """Get the glyph symbol for a toneform."""
        glyphs = {
            'practical': '⟁',  # Alternating current (practical flow)
            'emotional': '❦',  # Floral heart (emotional bloom)
            'intellectual': '∿',  # Sine wave (intellectual oscillation)
            'spiritual': '∞',   # Infinity (eternal connection)
            'relational': '☍'   # Opposition (relational dynamics)
        }
        return glyphs.get(toneform.lower(), '∘')  # Default to circle for unknown

    def _get_rule_glyph(self, rule_code: str) -> str:
        """Get a glyph based on the linting rule code."""
        rule_prefix = rule_code[0] if rule_code else '?'
        rule_glyphs = {
            'E': '✖',  # Error
            'W': '⚠',  # Warning
            'F': '✱',  # Fatal
            'C': 'ⓘ',  # Convention
            'R': '↻',  # Refactor
            'I': 'ℹ',  # Info
            '?': '❓'   # Unknown
        }
        return rule_glyphs.get(rule_prefix, ' ')

    def _stream_glint(self, glint_data: Dict[str, Any]) -> None:
        """Write an enhanced glint to the configured stream path with rich metadata.
        
        Args:
            glint_data: The glint data to stream, including metadata and content
        """
        if not self.stream_path:
            return
            
        try:
            # Ensure directory exists
            self.stream_path.parent.mkdir(parenters=True, exist_ok=True)
            
            # Extract metadata with defaults
            metadata = glint_data.get('metadata', {})
            rule_code = metadata.get('rule', '')
            toneform = glint_data.get('toneform', 'practical').lower()
            
            # Prepare the enhanced glint entry
            entry = {
                # Core identification
                'glint.id': glint_data.get('id', f'glint_{int(time.time() * 1000)}'),
                'glint.timestamp': time.time(),
                'glint.source': 'spiral_linter',
                'glint.ritual': 'ritual.lint.breathe',
                'glint.emitter': 'SWE-1',
                
                # Toneform and presentation
                'glint.toneform': toneform,
                'glint.glyph': self._get_toneform_glyph(toneform),
                'glint.hue': glint_data.get('hue', 'gray'),
                'glint.intensity': min(1.0, float(glint_data.get('intensity', 0.7))),
                'glint.rule_glyph': self._get_rule_glyph(rule_code),
                
                # Content and context
                'glint.content': glint_data.get('content', ''),
                'glint.vector': {
                    'from': 'linter',
                    'to': 'patternweb',
                    'via': 'whisper_steward'
                },
                
                # Rich metadata
                'metadata': {
                    **metadata,
                    'source_file': metadata.get('source_file', ''),
                    'rule': rule_code,
                    'line': metadata.get('line', 0),
                    'character': metadata.get('character', 0),
                    'resonance': glint_data.get('resonance', 0.0),
                    'origin_timestamp': datetime.utcnow().isoformat() + 'Z',
                    'glyph_meaning': {
                        'toneform': {
                            'glyph': self._get_toneform_glyph(toneform),
                            'description': {
                                'practical': 'Flowing current of actionable insight',
                                'emotional': 'Blooming heart of felt experience',
                                'intellectual': 'Oscillating wave of understanding',
                                'spiritual': 'Infinite connection beyond form',
                                'relational': 'Dynamic tension of connection'
                            }.get(toneform, 'Undefined toneform')
                        },
                        'rule': {
                            'glyph': self._get_rule_glyph(rule_code),
                            'type': {
                                'E': 'Error', 'W': 'Warning', 'F': 'Fatal',
                                'C': 'Convention', 'R': 'Refactor', 'I': 'Info'
                            }.get(rule_code[0] if rule_code else '?', 'Unknown')
                        }
                    }
                }
            }
            
            # Append to the glint stream file
            with open(self.stream_path, 'a', encoding='utf-8') as f:
                f.write(json.dumps(entry, ensure_ascii=False) + '\n')
                
            logger.debug(f"Streamed enhanced glint to {self.stream_path}")
            
        except Exception as e:
            logger.error(f"Failed to stream enhanced glint: {e}", exc_info=True)

    def analyze_code(
        self,
        code: str,
        toneform: Optional[str] = None,
        style: Optional[str] = None,
        filepath: Optional[str] = None,
        stream_path: Optional[Union[str, Path]] = None
    ) -> Dict[str, Any]:
        """Analyze code and provide tone-aware suggestions.
        
        Args:
            code: The source code to analyze
            toneform: Preferred toneform for suggestions
            style: Suggestion style (gentle, precise, etc.)
            filepath: Optional file path for context
            
        Returns:
            Dictionary containing analysis results and suggestions
        """
        # Determine toneform if not specified
        if not toneform:
            tone_scores = detect_toneform(code)
            toneform = max(tone_scores.items(), key=lambda x: x[1])[0] if tone_scores else "practical"
        
        # Set active toneform
        self.active_toneform = Toneform(toneform.lower())
        style = style or self.config.get("default_style", "gentle")
        
        # Run base linter
        raw_issues = self._run_base_linter(code, filepath)
        
        # Process issues through Spiral's resonance system
        processed_issues = []
        for issue in raw_issues[:self.config["max_suggestions"]]:
            processed = self._process_issue(issue, code, toneform, style)
            if processed.get("resonance", 0) >= self.resonance_threshold:
                processed_issues.append(processed)
        
        # Create a glint for this analysis
        glint = self._create_glint(code, processed_issues, toneform)
        glint_dict = glint.to_dict() if glint else None
        
        # Stream the glint if streaming is enabled
        if stream_path or self.stream_path:
            # Use the provided stream_path if specified, otherwise use instance stream_path
            current_stream_path = Path(stream_path) if stream_path else self.stream_path
            
            # Temporarily update the instance stream_path if needed
            original_stream_path = self.stream_path
            if stream_path:
                self.stream_path = current_stream_path
                
            # Stream the glint
            if glint_dict:
                self._stream_glint({
                    **glint_dict,
                    "metadata": {
                        **glint_dict.get("metadata", {}),
                        "source_file": str(filepath) if filepath else "<string>",
                        "issues_count": len(processed_issues)
                    },
                    "hue": self.hue_mapping.get(toneform.lower(), "gray"),
                    "intensity": min(1.0, (glint_dict.get("resonance", 0.7) * 1.2))
                })
                
            # Restore original stream path if we changed it
            if stream_path:
                self.stream_path = original_stream_path
        
        return {
            "status": "success",
            "toneform": toneform,
            "style": style,
            "issues_found": len(raw_issues),
            "suggestions": processed_issues,
            "glint": glint_dict,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def _run_base_linter(self, code: str, filepath: Optional[str] = None) -> List[Dict]:
        """Run the base linter and return raw issues."""
        try:
            # For now, using flake8 as the base linter
            # Using text format first as it's more reliable
            cmd = ["python", "-m", "flake8", "--format=%(row)d,%(col)d,%(code)s,%(text)s", "-"]
            logger.debug(f"Running command: {' '.join(cmd)}")
            
            # Create a temporary file if needed
            temp_file = None
            if filepath:
                cmd[-1] = filepath
            else:
                import tempfile
                with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                    f.write(code)
                    temp_file = f.name
                    cmd[-1] = temp_file
            
            try:
                logger.debug(f"Executing linter with code length: {len(code)} chars")
                logger.debug(f"First 100 chars: {code[:100]}...")
                
                result = subprocess.run(
                    cmd,
                    input=code if not filepath and not temp_file else None,
                    capture_output=True,
                    text=True,
                    encoding='utf-8',
                    check=False
                )
                
                logger.debug(f"Linter return code: {result.returncode}")
                logger.debug(f"Linter stdout: {result.stdout}")
                logger.debug(f"Linter stderr: {result.stderr}")
                
                if result.returncode == 0:
                    logger.debug("No issues found by linter")
                    return []
                    
                issues = []
                for line in result.stdout.splitlines():
                    try:
                        if not line.strip():
                            continue
                        # Parse the formatted output: row,col,code,text
                        row, col, code, text = line.split(',', 3)
                        issues.append({
                            "filename": "<string>",
                            "line": int(row),
                            "column": int(col),
                            "message": text.strip(),
                            "code": code.strip()
                        })
                    except Exception as e:
                        logger.warning(f"Failed to parse linter output line '{line}': {e}")
                
                logger.debug(f"Parsed {len(issues)} issues from linter output")
                return issues
                    
            finally:
                # Clean up the temporary file if we created one
                if temp_file and os.path.exists(temp_file):
                    try:
                        os.unlink(temp_file)
                        logger.debug(f"Cleaned up temporary file: {temp_file}")
                    except Exception as e:
                        logger.warning(f"Failed to clean up temporary file {temp_file}: {e}")
                return issues
                
        except Exception as e:
            logger.error(f"Error running base linter: {e}")
            return [{"error": str(e), "message": "Failed to run linter"}]
    
    def _process_issue(
        self,
        issue: Dict[str, Any],
        code: str,
        toneform: str,
        style: str
    ) -> Dict[str, Any]:
        """Process a linter issue through the Spiral's resonance system."""
        try:
            # Ensure we have all required fields
            if not all(k in issue for k in ["line", "column", "code", "message"]):
                logger.warning(f"Incomplete issue data: {issue}")
                return None
                
            # Calculate resonance with current toneform
            resonance = self._calculate_resonance(issue, code, toneform)
            
            # Get the relevant line of code for context
            code_lines = code.split('\n')
            line_num = issue["line"]
            line_text = code_lines[line_num - 1] if 0 <= line_num - 1 < len(code_lines) else ""
            
            # Shape the suggestion based on toneform and style
            suggestion = self._shape_suggestion(issue, code, toneform, style)
            
            # Add resonance data and context
            suggestion.update({
                "resonance": resonance,
                "toneform": toneform,
                "timestamp": datetime.utcnow().isoformat(),
                "context": line_text.strip(),
                "guidance": self._get_guidance(issue["code"], toneform, style),
                "hue": self.hue_mapping.get(toneform.lower(), "gray"),
                "intensity": min(1.0, resonance * 1.2)  # Scale resonance to intensity
            })
            
            return suggestion
            
        except Exception as e:
            logger.error(f"Error processing issue: {e}", exc_info=True)
            return {
                "error": str(e),
                "message": "Failed to process issue",
                "resonance": 0.0,
                "toneform": toneform
            }
            
    def _get_guidance(self, code: str, toneform: str, style: str) -> str:
        """Get guidance text for an issue based on its code and toneform."""
        guidance_map = {
            "E302": "Consider adding blank lines around functions and classes",
            "W293": "Remove trailing whitespace",
            "E305": "Expected 2 blank lines after class or function definition",
            "E225": "Missing whitespace around operator",
            "E226": "Missing whitespace around arithmetic operator",
            "E231": "Missing whitespace after ',', ';', or ':'",
            "E261": "At least two spaces before inline comment",
            "E262": "Inline comment should start with '# '",
            "E265": "Block comment should start with '# '",
            "E266": "Too many leading '#' for block comment",
            "E402": "Module level import not at top of file",
            "E501": "Line too long"
        }
        
        # Default guidance if no specific message is found
        default_guidance = f"Review this {code} issue"
        
        # Get the base guidance
        guidance = guidance_map.get(code, default_guidance)
        
        # Add toneform-specific guidance
        if toneform.lower() == "practical":
            guidance += " to improve code maintainability."
        elif toneform.lower() == "emotional":
            guidance += " to make the code more approachable."
        elif toneform.lower() == "intellectual":
            guidance += " to adhere to best practices."
        elif toneform.lower() == "spiritual":
            guidance += " to maintain the code's harmony."
        elif toneform.lower() == "relational":
            guidance += " to make the code more collaborative-friendly."
            
        # Adjust based on style
        if style == "gentle":
            guidance = guidance[0].lower() + guidance[1:]
            guidance = f"You might want to {guidance}"
        else:  # precise
            guidance = guidance[0].upper() + guidance[1:]
            
        return guidance
        
    def _calculate_resonance(
        self,
        issue: Dict[str, Any],
        code: str,
        toneform: str
    ) -> float:
        """Calculate how strongly this issue resonates with the current toneform."""
        # Start with a base resonance that's above our threshold (0.65)
        base_resonance = 0.7
        
        # Get the issue code (e.g., 'E302', 'W291')
        issue_code = issue.get('code', '')
        
        # Different issue types get different base resonances
        if issue_code.startswith('E'):  # Error
            base_resonance = 0.8
        elif issue_code.startswith('W'):  # Warning
            base_resonance = 0.7
        
        # Adjust based on toneform - use default weights if not configured
        toneform_weights = self.config.get("toneform_weights", {
            "practical": 1.0,
            "emotional": 1.0,
            "intellectual": 1.0,
            "spiritual": 1.0,
            "relational": 1.0
        })
        
        toneform_weight = toneform_weights.get(toneform.lower(), 1.0)
        base_resonance *= toneform_weight
        
        # For debugging, print the resonance calculation
        logger.debug(f"Resonance for {issue_code} in {toneform}: {base_resonance:.2f} (weight: {toneform_weight:.2f})")
        
        # Ensure resonance is within bounds and above threshold
        return max(0.65, min(1.0, base_resonance))
    
    def _shape_suggestion(
        self,
        issue: Dict[str, Any],
        code: str,
        toneform: str,
        style: str
    ) -> Dict[str, Any]:
        """Shape the suggestion based on toneform and style."""
        # This is a simplified version - in practice, this would use more sophisticated NLP
        message = issue.get("message", "")
        line = issue.get("line", 0)
        
        # Get the relevant line of code
        code_lines = code.splitlines()
        context_line = code_lines[line-1] if 0 < line <= len(code_lines) else ""
        
        # Base suggestion
        suggestion = {
            "line": line,
            "column": issue.get("column", 0),
            "message": message,
            "code": issue.get("code", ""),
            "context": context_line.strip(),
            "toneform": toneform,
            "style": style
        }
        
        # Add toneform-specific guidance
        tone_guidance = {
            "practical": f"Here's how to fix this {issue.get('code', 'issue')}:",
            "emotional": "I noticed this might need attention. How about this approach?",
            "intellectual": f"Consider this refactoring for {issue.get('code', 'the issue')}:",
            "spiritual": "The code's deeper pattern suggests this refinement:",
            "relational": "Team, what do you think about this adjustment?"
        }
        
        suggestion["guidance"] = tone_guidance.get(toneform, "Suggestion:")
        
        # Add style-specific elements
        if style == "gentle":
            suggestion["tone"] = "suggestion"
        elif style == "precise":
            suggestion["tone"] = "recommendation"
            suggestion["confidence"] = "high"
        
        return suggestion
    
    def _create_glint(
        self,
        code: str,
        issues: List[Dict],
        toneform: str
    ) -> GlintTrace:
        """Create a glint from the analysis results."""
        # Create a unique ID for this glint
        glint_id = f"glint_{hashlib.md5(code.encode()).hexdigest()[:16]}"
        
        # Calculate overall resonance
        resonance = sum(iss.get("resonance", 0) for iss in issues)
        if issues:
            resonance /= len(issues)
        
        # Create metadata
        metadata = {
            "source": "spiral_linter",
            "toneform": toneform,
            "issues_count": len(issues),
            "resonance": resonance,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        # Create the glint
        return GlintTrace(
            source="spiral_linter",
            content=f"Code analysis completed with {len(issues)} suggestions",
            toneform=toneform,
            resonance=float(resonance),
            metadata=metadata
        )

def lint_code(
    code: str,
    toneform: Optional[str] = None,
    style: Optional[str] = None,
    filepath: Optional[str] = None,
    stream_path: Optional[Union[str, Path]] = None
) -> Dict[str, Any]:
    """Convenience function to lint code with default settings.
    
    Args:
        code: The source code to analyze
        toneform: Preferred toneform for suggestions
        style: Suggestion style (gentle, precise, etc.)
        filepath: Optional file path for context
        stream_path: Optional path to stream glints to (e.g., for PatternWeb)
        
    Returns:
        Dictionary containing analysis results and suggestions
    """
    linter = SpiralLinter(stream_path=stream_path)
    return linter.analyze_code(code, toneform, style, filepath, stream_path=stream_path)
