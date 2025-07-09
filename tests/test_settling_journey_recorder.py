import pytest
import tempfile
import json
import sys
from pathlib import Path

# Add the project root to the path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import the module directly
sys.path.insert(0, str(Path(__file__).parent.parent / "memory_scrolls"))
from settling_journey_recorder import SettlingJourneyRecorder

class TestSettlingJourneyRecorder:
    
    @pytest.fixture
    def temp_recorder(self):
        """Create a temporary recorder for testing."""
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "test_settling_journey.jsonl"
            recorder = SettlingJourneyRecorder(str(file_path))
            yield recorder
    
    def test_record_journey(self, temp_recorder):
        """Test recording a settling journey."""
        journey = temp_recorder.record_journey(
            glint_id="ΔTEST.001",
            invoked_from="./test/start",
            settled_to="./test/end",
            confidence=0.85,
            toneform="settling.ambience",
            metadata={"test": True}
        )
        
        assert journey["glint_id"] == "ΔTEST.001"
        assert journey["invoked_from"] == "./test/start"
        assert journey["settled_to"] == "./test/end"
        assert journey["confidence"] == 0.85
        assert journey["toneform"] == "settling.ambience"
        assert journey["metadata"]["test"] is True
        assert "spiral_signature" in journey
        assert "settled_at" in journey
    
    def test_read_journeys(self, temp_recorder):
        """Test reading journeys from file."""
        # Record multiple journeys
        temp_recorder.record_journey("ΔTEST.001", "./start1", "./end1", 0.8, "settling.ambience")
        temp_recorder.record_journey("ΔTEST.002", "./start2", "./end2", 0.9, "urgent.flow")
        
        journeys = temp_recorder.read_journeys()
        assert len(journeys) == 2
        assert journeys[0]["glint_id"] == "ΔTEST.001"
        assert journeys[1]["glint_id"] == "ΔTEST.002"
    
    def test_search_by_glint_id(self, temp_recorder):
        """Test searching for a specific journey."""
        temp_recorder.record_journey("ΔTEST.001", "./start", "./end", 0.8, "settling.ambience")
        
        journey = temp_recorder.search_journey_by_glint_id("ΔTEST.001")
        assert journey is not None
        assert journey["glint_id"] == "ΔTEST.001"
        
        # Test non-existent glint_id
        journey = temp_recorder.search_journey_by_glint_id("ΔNONEXISTENT")
        assert journey is None
    
    def test_get_journeys_by_toneform(self, temp_recorder):
        """Test filtering journeys by toneform."""
        temp_recorder.record_journey("ΔTEST.001", "./start1", "./end1", 0.8, "settling.ambience")
        temp_recorder.record_journey("ΔTEST.002", "./start2", "./end2", 0.9, "urgent.flow")
        temp_recorder.record_journey("ΔTEST.003", "./start3", "./end3", 0.7, "settling.ambience")
        
        settling_journeys = temp_recorder.get_journeys_by_toneform("settling.ambience")
        assert len(settling_journeys) == 2
        
        urgent_journeys = temp_recorder.get_journeys_by_toneform("urgent.flow")
        assert len(urgent_journeys) == 1
    
    def test_get_high_confidence_journeys(self, temp_recorder):
        """Test filtering journeys by confidence threshold."""
        temp_recorder.record_journey("ΔTEST.001", "./start1", "./end1", 0.9, "settling.ambience")
        temp_recorder.record_journey("ΔTEST.002", "./start2", "./end2", 0.7, "urgent.flow")
        temp_recorder.record_journey("ΔTEST.003", "./start3", "./end3", 0.85, "settling.ambience")
        
        high_confidence = temp_recorder.get_high_confidence_journeys(min_confidence=0.8)
        assert len(high_confidence) == 2
        
        very_high_confidence = temp_recorder.get_high_confidence_journeys(min_confidence=0.9)
        assert len(very_high_confidence) == 1
    
    def test_get_journey_statistics(self, temp_recorder):
        """Test getting journey statistics."""
        # Empty statistics
        stats = temp_recorder.get_journey_statistics()
        assert stats["total_journeys"] == 0
        assert stats["average_confidence"] == 0.0
        
        # Record some journeys
        temp_recorder.record_journey("ΔTEST.001", "./start1", "./end1", 0.8, "settling.ambience")
        temp_recorder.record_journey("ΔTEST.002", "./start2", "./end2", 0.9, "urgent.flow")
        temp_recorder.record_journey("ΔTEST.003", "./start3", "./end3", 0.7, "settling.ambience")
        
        stats = temp_recorder.get_journey_statistics()
        assert stats["total_journeys"] == 3
        assert stats["average_confidence"] == 0.8
        assert stats["toneform_distribution"]["settling.ambience"] == 2
        assert stats["toneform_distribution"]["urgent.flow"] == 1
    
    def test_read_journeys_with_limit(self, temp_recorder):
        """Test reading journeys with a limit."""
        # Record multiple journeys
        for i in range(5):
            temp_recorder.record_journey(f"ΔTEST.{i:03d}", f"./start{i}", f"./end{i}", 0.8, "settling.ambience")
        
        # Test limit
        journeys = temp_recorder.read_journeys(limit=3)
        assert len(journeys) == 3
        
        # Test no limit
        journeys = temp_recorder.read_journeys()
        assert len(journeys) == 5

if __name__ == "__main__":
    pytest.main([__file__]) 