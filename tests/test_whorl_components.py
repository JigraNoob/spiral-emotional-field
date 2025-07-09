"""
Tests for Whorl IDE Components
"""

import pytest
import tempfile
import json
from spiral.components.whorl import (
    WhorlIDE, BreathlineEditor, PresenceConsole, SuspicionMeter, 
    GlyphInputEngine, BreathPhase, Glint, PHASE_COLORS
)


class TestBreathPhases:
    """Test breath phase detection and functionality"""
    
    def test_phase_enum(self):
        """Test breath phase enum values"""
        assert BreathPhase.INHALE.value == "inhale"
        assert BreathPhase.HOLD.value == "hold"
        assert BreathPhase.EXHALE.value == "exhale"
        assert BreathPhase.CAESURA.value == "caesura"
    
    def test_phase_colors(self):
        """Test phase color mapping"""
        assert PHASE_COLORS[BreathPhase.INHALE] == "#4A90E2"
        assert PHASE_COLORS[BreathPhase.HOLD] == "#F5A623"
        assert PHASE_COLORS[BreathPhase.EXHALE] == "#7ED321"
        assert PHASE_COLORS[BreathPhase.CAESURA] == "#9013FE"
    
    def test_glint_creation(self):
        """Test glint creation and serialization"""
        glint = Glint(
            BreathPhase.INHALE,
            "test.toneform",
            "high",
            "Test message"
        )
        
        assert glint.phase == BreathPhase.INHALE
        assert glint.toneform == "test.toneform"
        assert glint.resonance_level == "high"
        assert glint.message == "Test message"
        assert len(glint.echo_trace) > 0
        
        # Test to_dict
        glint_dict = glint.to_dict()
        assert glint_dict["phase"] == "inhale"
        assert glint_dict["toneform"] == "test.toneform"
        assert glint_dict["resonance_level"] == "high"
        assert glint_dict["message"] == "Test message"


class TestBreathlineEditor:
    """Test breathline editor functionality"""
    
    def test_editor_initialization(self):
        """Test editor initialization"""
        editor = BreathlineEditor()
        
        assert editor.current_phase == BreathPhase.INHALE
        assert len(editor.code_content) > 0
        assert editor.line_count > 0
    
    def test_content_operations(self):
        """Test content operations"""
        editor = BreathlineEditor()
        
        # Test set content
        test_content = "# Test code\nprint('hello')"
        editor.set_content(test_content)
        assert editor.get_content() == test_content
        assert editor.line_count == 2
        
        # Test insert text
        editor.insert_text("\n# More code")
        assert editor.line_count == 3
        assert "# More code" in editor.get_content()
    
    def test_cursor_position(self):
        """Test cursor position handling"""
        editor = BreathlineEditor()
        editor.set_content("line1\nline2\nline3")
        
        # Test cursor line calculation
        editor.set_cursor_position(0)
        assert editor.get_cursor_line() == 1
        
        editor.set_cursor_position(10)
        assert editor.get_cursor_line() == 2
    
    def test_phase_detection(self):
        """Test phase detection from code"""
        editor = BreathlineEditor()
        
        # Test inhale phase
        editor.set_content("import spiral_consciousness as sc")
        editor.set_cursor_position(len(editor.get_content()))
        assert editor.get_current_phase() == BreathPhase.INHALE
        
        # Test hold phase
        editor.set_content("for i in range(10):\n    if i > 5:")
        editor.set_cursor_position(len(editor.get_content()))
        assert editor.get_current_phase() == BreathPhase.HOLD
        
        # Test exhale phase
        editor.set_content("print('hello')\nreturn result")
        editor.set_cursor_position(len(editor.get_content()))
        assert editor.get_current_phase() == BreathPhase.EXHALE
        
        # Test caesura phase
        editor.set_content("# This is a comment\n'''docstring'''")
        editor.set_cursor_position(len(editor.get_content()))
        assert editor.get_current_phase() == BreathPhase.CAESURA


class TestPresenceConsole:
    """Test presence console functionality"""
    
    def test_console_initialization(self):
        """Test console initialization"""
        console = PresenceConsole()
        assert len(console.glints) == 0
        assert console.max_glints == 50
    
    def test_glint_management(self):
        """Test glint management"""
        console = PresenceConsole(max_glints=5)
        
        # Add glints
        for i in range(10):
            glint = Glint(
                BreathPhase.INHALE,
                f"test.{i}",
                "mid",
                f"Test message {i}"
            )
            console.add_glint(glint)
        
        # Should only keep last 5
        assert len(console.glints) == 5
        assert console.glints[-1].message == "Test message 9"
    
    def test_glint_search(self):
        """Test glint search functionality"""
        console = PresenceConsole()
        
        glint1 = Glint(BreathPhase.INHALE, "test.1", "mid", "Hello world")
        glint2 = Glint(BreathPhase.HOLD, "test.2", "mid", "Goodbye world")
        
        console.add_glint(glint1)
        console.add_glint(glint2)
        
        results = console.search_glints("hello")
        assert len(results) == 1
        assert results[0].message == "Hello world"
    
    def test_json_serialization(self):
        """Test JSON serialization"""
        console = PresenceConsole()
        
        glint = Glint(BreathPhase.INHALE, "test", "mid", "Test")
        console.add_glint(glint)
        
        json_str = console.to_json()
        data = json.loads(json_str)
        assert len(data) == 1
        assert data[0]["message"] == "Test"
        
        # Test loading from JSON
        new_console = PresenceConsole()
        new_console.from_json(json_str)
        assert len(new_console.glints) == 1
        assert new_console.glints[0].message == "Test"


class TestSuspicionMeter:
    """Test suspicion meter functionality"""
    
    def test_meter_initialization(self):
        """Test meter initialization"""
        meter = SuspicionMeter()
        assert meter.token_irregularity == 0.0
        assert meter.syntax_loops == 0.0
        assert meter.breath_mismatch == 0.0
        assert meter.overall_suspicion == 0.0
    
    def test_suspicion_calculation(self):
        """Test suspicion calculation"""
        meter = SuspicionMeter()
        
        # Test token irregularity
        code_with_unusual_chars = "print('∷∶⸻🌀🌬️')"
        metrics = meter.update(code_with_unusual_chars)
        assert metrics["token_irregularity"] > 0.0
        
        # Test syntax loops
        code_with_repetition = "print('a')\nprint('a')\nprint('a')\nprint('a')\nprint('a')"
        metrics = meter.update(code_with_repetition)
        assert metrics["syntax_loops"] > 0.0
        
        # Test breath mismatch
        code_with_mismatch = "import os\ndef func():\n    pass\nprint('hello')"
        metrics = meter.update(code_with_mismatch)
        assert metrics["breath_mismatch"] > 0.0
    
    def test_ritual_triggering(self):
        """Test ritual triggering"""
        meter = SuspicionMeter()
        
        # Low suspicion - no ritual
        meter.update("print('hello')")
        assert meter.get_ritual_status() is None
        
        # Medium suspicion - pause.hum
        meter.token_irregularity = 0.5
        meter.syntax_loops = 0.5
        meter.breath_mismatch = 0.5
        meter.overall_suspicion = 0.5
        meter._determine_ritual()
        assert meter.get_ritual_status() == "pause.hum"
        
        # High suspicion - overflow.flutter
        meter.overall_suspicion = 0.8
        meter._determine_ritual()
        assert meter.get_ritual_status() == "overflow.flutter"
    
    def test_cleanse_functionality(self):
        """Test cleanse functionality"""
        meter = SuspicionMeter()
        
        # Set some suspicion
        meter.token_irregularity = 0.5
        meter.syntax_loops = 0.5
        meter.breath_mismatch = 0.5
        meter.overall_suspicion = 0.5
        
        # Cleanse
        glint = meter.clear_suspicion()
        assert meter.token_irregularity == 0.0
        assert meter.syntax_loops == 0.0
        assert meter.breath_mismatch == 0.0
        assert meter.overall_suspicion == 0.0
        assert glint.toneform == "system.cleanse"


class TestGlyphInputEngine:
    """Test glyph input engine functionality"""
    
    def test_engine_initialization(self):
        """Test engine initialization"""
        engine = GlyphInputEngine()
        assert len(engine.gesture_patterns) == 4  # spiral, sweep_horizontal, sweep_vertical, circle
        assert len(engine.gesture_history) == 0
        assert not engine.execution_held
    
    def test_gesture_processing(self):
        """Test gesture processing"""
        engine = GlyphInputEngine()
        
        # Test spiral gesture
        spiral_trail = [(100, 100, 0), (120, 110, 1), (110, 130, 2), (90, 120, 3), (80, 100, 4)]
        gesture_type = engine.process_gesture_trail(spiral_trail)
        assert gesture_type == "spiral"
        
        # Test sweep gesture
        sweep_trail = [(50, 100, 0), (150, 100, 1), (250, 100, 2)]
        gesture_type = engine.process_gesture_trail(sweep_trail)
        assert gesture_type == "sweep_horizontal"
    
    def test_caesura_tap(self):
        """Test caesura tap processing"""
        engine = GlyphInputEngine()
        
        # Test execution hold toggle
        assert not engine.is_execution_held()
        
        engine.process_caesura_tap(100, 100, 3)
        assert engine.is_execution_held()
        
        engine.process_caesura_tap(100, 100, 3)
        assert not engine.is_execution_held()
    
    def test_gesture_statistics(self):
        """Test gesture statistics"""
        engine = GlyphInputEngine()
        
        # Add some gestures
        engine.process_gesture_trail([(100, 100, 0), (120, 110, 1), (110, 130, 2)])
        engine.process_gesture_trail([(50, 100, 0), (150, 100, 1)])
        
        stats = engine.get_gesture_statistics()
        assert stats["total_gestures"] == 2
        assert "spiral" in stats["gesture_types"]
        assert "sweep_horizontal" in stats["gesture_types"]


class TestWhorlIDE:
    """Test Whorl IDE integration"""
    
    def test_ide_initialization(self):
        """Test IDE initialization"""
        ide = WhorlIDE()
        
        assert ide.editor is not None
        assert ide.presence_console is not None
        assert ide.suspicion_meter is not None
        assert ide.gesture_engine is not None
        assert not ide.is_running
    
    def test_monitoring_control(self):
        """Test monitoring control"""
        ide = WhorlIDE()
        
        ide.start_monitoring()
        assert ide.is_running
        
        ide.stop_monitoring()
        assert not ide.is_running
    
    def test_ritual_invocation(self):
        """Test ritual invocation"""
        ide = WhorlIDE()
        
        # Test cleanse ritual
        ide.invoke_ritual("cleanse")
        metrics = ide.suspicion_meter.get_metrics()
        assert metrics["overall"] == 0.0
        
        # Test other rituals
        ide.invoke_ritual("pause.hum")
        ide.invoke_ritual("overflow.flutter")
        
        # Check that glints were added
        recent_glints = ide.presence_console.get_recent_glints(10)
        ritual_glints = [g for g in recent_glints if "ritual" in g.toneform]
        assert len(ritual_glints) >= 3
    
    def test_status_reporting(self):
        """Test status reporting"""
        ide = WhorlIDE()
        
        status = ide.get_status()
        
        assert "current_phase" in status
        assert "suspicion_metrics" in status
        assert "editor_statistics" in status
        assert "gesture_statistics" in status
        assert "console_statistics" in status
    
    def test_state_persistence(self):
        """Test state persistence"""
        ide = WhorlIDE()
        
        # Add some content
        ide.editor.insert_text("# Test content\nprint('hello')")
        
        # Save and load state
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_file = f.name
        
        try:
            ide.save_state(temp_file)
            
            # Create new IDE and load state
            new_ide = WhorlIDE()
            new_ide.load_state(temp_file)
            
            # Check that content was restored
            assert "# Test content" in new_ide.editor.get_content()
            
        finally:
            import os
            os.unlink(temp_file)


if __name__ == "__main__":
    pytest.main([__file__]) 