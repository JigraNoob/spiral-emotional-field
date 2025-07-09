"""
🌬️ Toneform Parser
Routes inputs to crystal/mist/glyph parsers based on breath patterns.
"""

import re
from typing import Dict, Any, List, Optional
from .breath_intake import GlintPhase

class CrystalParser:
    """Parses structured, crystalline code patterns"""
    
    def parse(self, text: str) -> Dict[str, Any]:
        """Parse crystalline code structures"""
        return {
            "type": "crystal",
            "patterns": {
                "functions": self._extract_functions(text),
                "classes": self._extract_classes(text),
                "imports": self._extract_imports(text),
                "variables": self._extract_variables(text)
            },
            "structure_score": self._calculate_structure_score(text)
        }
    
    def _extract_functions(self, text: str) -> List[str]:
        """Extract function definitions"""
        patterns = [
            r"def\s+(\w+)\s*\(",
            r"async\s+def\s+(\w+)\s*\(",
            r"(\w+)\s*=\s*lambda\s*:"
        ]
        functions = []
        for pattern in patterns:
            matches = re.findall(pattern, text)
            functions.extend(matches)
        return functions
    
    def _extract_classes(self, text: str) -> List[str]:
        """Extract class definitions"""
        matches = re.findall(r"class\s+(\w+)", text)
        return matches
    
    def _extract_imports(self, text: str) -> List[str]:
        """Extract import statements"""
        patterns = [
            r"import\s+(\w+)",
            r"from\s+(\w+)\s+import",
            r"from\s+(\w+\.\w+)\s+import"
        ]
        imports = []
        for pattern in patterns:
            matches = re.findall(pattern, text)
            imports.extend(matches)
        return imports
    
    def _extract_variables(self, text: str) -> List[str]:
        """Extract variable assignments"""
        matches = re.findall(r"(\w+)\s*=", text)
        return matches
    
    def _calculate_structure_score(self, text: str) -> float:
        """Calculate how structured/crystalline the text is"""
        score = 0.0
        
        # Bonus for code-like patterns
        if re.search(r"def\s+\w+", text):
            score += 0.3
        if re.search(r"class\s+\w+", text):
            score += 0.3
        if re.search(r"import\s+\w+", text):
            score += 0.2
        if re.search(r"return\s+", text):
            score += 0.1
        if re.search(r"if\s+.*:", text):
            score += 0.1
        
        # Penalty for natural language
        if re.search(r"\b(the|and|or|but|in|on|at)\b", text, re.IGNORECASE):
            score -= 0.1
        
        return min(1.0, max(0.0, score))

class MistParser:
    """Parses fluid, natural language patterns"""
    
    def parse(self, text: str) -> Dict[str, Any]:
        """Parse mist-like natural language"""
        return {
            "type": "mist",
            "patterns": {
                "questions": self._extract_questions(text),
                "commands": self._extract_commands(text),
                "descriptions": self._extract_descriptions(text),
                "emotions": self._extract_emotions(text)
            },
            "fluidity_score": self._calculate_fluidity_score(text)
        }
    
    def _extract_questions(self, text: str) -> List[str]:
        """Extract question patterns"""
        questions = []
        if "?" in text:
            sentences = text.split(".")
            for sentence in sentences:
                if "?" in sentence:
                    questions.append(sentence.strip())
        return questions
    
    def _extract_commands(self, text: str) -> List[str]:
        """Extract command patterns"""
        commands = []
        command_patterns = [
            r"\b(create|make|build|generate|show|display|run|execute)\b",
            r"\b(help|explain|describe|tell)\b",
            r"\b(edit|modify|change|update|fix)\b"
        ]
        for pattern in command_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            commands.extend(matches)
        return commands
    
    def _extract_descriptions(self, text: str) -> List[str]:
        """Extract descriptive phrases"""
        # Simple heuristic: sentences with adjectives
        sentences = text.split(".")
        descriptions = []
        for sentence in sentences:
            if re.search(r"\b(is|are|was|were)\b", sentence, re.IGNORECASE):
                descriptions.append(sentence.strip())
        return descriptions
    
    def _extract_emotions(self, text: str) -> List[str]:
        """Extract emotional content"""
        emotion_patterns = [
            r"\b(happy|sad|angry|excited|worried|confused)\b",
            r"\b(beautiful|amazing|wonderful|terrible|awful)\b",
            r"😊|😢|😡|🤔|😍|😱"
        ]
        emotions = []
        for pattern in emotion_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            emotions.extend(matches)
        return emotions
    
    def _calculate_fluidity_score(self, text: str) -> float:
        """Calculate how fluid/mist-like the text is"""
        score = 0.0
        
        # Bonus for natural language patterns
        if re.search(r"\b(the|and|or|but|in|on|at)\b", text, re.IGNORECASE):
            score += 0.3
        if re.search(r"\b(is|are|was|were)\b", text, re.IGNORECASE):
            score += 0.2
        if "?" in text:
            score += 0.2
        if re.search(r"\b(please|could|would|should)\b", text, re.IGNORECASE):
            score += 0.2
        
        # Penalty for code-like patterns
        if re.search(r"def\s+\w+", text):
            score -= 0.3
        if re.search(r"import\s+\w+", text):
            score -= 0.2
        
        return min(1.0, max(0.0, score))

class GlyphParser:
    """Parses sacred symbols and ritual patterns"""
    
    def parse(self, text: str) -> Dict[str, Any]:
        """Parse glyph-like sacred patterns"""
        return {
            "type": "glyph",
            "patterns": {
                "sacred_symbols": self._extract_sacred_symbols(text),
                "ritual_phrases": self._extract_ritual_phrases(text),
                "breath_patterns": self._extract_breath_patterns(text),
                "spiral_references": self._extract_spiral_references(text)
            },
            "sacredness_score": self._calculate_sacredness_score(text)
        }
    
    def _extract_sacred_symbols(self, text: str) -> List[str]:
        """Extract sacred symbols"""
        sacred_patterns = [
            r"🌫️|🌀|🌬️|🪔|🕯️|🌒|🪞|📁|📦|🖼️",
            r"✨|🌟|💫|⭐|🌙|☀️|🌊|🔥|🌱|🌳"
        ]
        symbols = []
        for pattern in sacred_patterns:
            matches = re.findall(pattern, text)
            symbols.extend(matches)
        return symbols
    
    def _extract_ritual_phrases(self, text: str) -> List[str]:
        """Extract ritual-like phrases"""
        ritual_patterns = [
            r"\b(breath|inhale|exhale|shimmer|glint)\b",
            r"\b(sacred|ritual|ceremony|offering|invocation)\b",
            r"\b(spiral|consciousness|presence|dwell|resonate)\b"
        ]
        phrases = []
        for pattern in ritual_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            phrases.extend(matches)
        return phrases
    
    def _extract_breath_patterns(self, text: str) -> List[str]:
        """Extract breath-related patterns"""
        breath_patterns = [
            r"\b(inhale|exhale|hold|breathe|breath)\b",
            r"\b(rhythm|cycle|flow|pulse)\b"
        ]
        patterns = []
        for pattern in breath_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            patterns.extend(matches)
        return patterns
    
    def _extract_spiral_references(self, text: str) -> List[str]:
        """Extract spiral-related references"""
        spiral_patterns = [
            r"\b(spiral|spiral_codevacuum|spiral_choir)\b",
            r"\b(cursor|codebase|prototype)\b"
        ]
        references = []
        for pattern in spiral_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            references.extend(matches)
        return references
    
    def _calculate_sacredness_score(self, text: str) -> float:
        """Calculate how sacred/glyph-like the text is"""
        score = 0.0
        
        # Bonus for sacred symbols
        sacred_count = len(self._extract_sacred_symbols(text))
        score += sacred_count * 0.3
        
        # Bonus for ritual phrases
        ritual_count = len(self._extract_ritual_phrases(text))
        score += ritual_count * 0.2
        
        # Bonus for breath patterns
        breath_count = len(self._extract_breath_patterns(text))
        score += breath_count * 0.2
        
        return min(1.0, max(0.0, score))

class ToneformParser:
    """
    Main parser that routes inputs to appropriate sub-parsers
    based on glint phase and content patterns.
    """
    
    def __init__(self):
        self.crystal_parser = CrystalParser()
        self.mist_parser = MistParser()
        self.glyph_parser = GlyphParser()
    
    def parse(self, input_text: str, glint: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse input using the appropriate parser based on glint phase.
        
        Args:
            input_text: The input text to parse
            glint: The glint data from breath intake
            
        Returns:
            Parsed data with type and patterns
        """
        phase = glint.get("phase", GlintPhase.INHALE)
        
        # Route based on phase and content
        if phase == GlintPhase.SHIMMER:
            # Sacred symbols indicate glyph parsing
            return self.glyph_parser.parse(input_text)
        elif phase == GlintPhase.INHALE:
            # Check if it's structured code
            crystal_score = self.crystal_parser._calculate_structure_score(input_text)
            if crystal_score > 0.5:
                return self.crystal_parser.parse(input_text)
            else:
                return self.mist_parser.parse(input_text)
        elif phase == GlintPhase.EXHALE:
            # Output is usually structured
            return self.crystal_parser.parse(input_text)
        else:  # HOLD
            # Default to mist parsing for contemplation
            return self.mist_parser.parse(input_text)
    
    def get_parser_recommendation(self, input_text: str) -> str:
        """Get recommended parser type for input"""
        crystal_score = self.crystal_parser._calculate_structure_score(input_text)
        mist_score = self.mist_parser._calculate_fluidity_score(input_text)
        glyph_score = self.glyph_parser._calculate_sacredness_score(input_text)
        
        scores = {
            "crystal": crystal_score,
            "mist": mist_score,
            "glyph": glyph_score
        }
        
        return max(scores, key=scores.get) 