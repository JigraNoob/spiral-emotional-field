# spiral/memory/integration_example.py

"""
Integration example for Memory Echo Index with existing Spiral components.

This demonstrates how the MemoryEchoIndex can be integrated with:
- Glint orchestrator
- Rituals
- Dashboard
- Codex entries
"""

from typing import Dict, List, Any, Optional
from .memory_echo_index import MemoryEchoIndex, query_memory_echoes


class MemoryEchoIntegration:
    """
    Integration layer for Memory Echo Index with Spiral components.
    """
    
    def __init__(self, base_path: Optional[str] = None):
        """Initialize the integration layer."""
        self.index = MemoryEchoIndex(base_path)
    
    def integrate_with_glint_orchestrator(self, glint_data: Dict[str, Any]) -> str:
        """
        Integrate with glint orchestrator to automatically index new glints.
        
        Args:
            glint_data (Dict[str, Any]): New glint data from orchestrator
            
        Returns:
            str: The glint ID that was indexed
        """
        glint_id = self.index.add_echo(glint_data, source="glint_orchestrator")
        print(f"🌀 Indexed glint: {glint_id}")
        return glint_id
    
    def integrate_with_rituals(self, ritual_name: str, ritual_data: Dict[str, Any]) -> str:
        """
        Integrate with rituals to track ritual states and outcomes.
        
        Args:
            ritual_name (str): Name of the ritual
            ritual_data (Dict[str, Any]): Ritual data and state
            
        Returns:
            str: The ritual echo ID
        """
        ritual_echo = {
            "id": f"ritual_{ritual_name}_{hash(str(ritual_data))}",
            "timestamp": ritual_data.get("timestamp", ""),
            "toneform": f"ritual.{ritual_name}",
            "content": f"Ritual: {ritual_name}",
            "metadata": ritual_data
        }
        
        echo_id = self.index.add_echo(ritual_echo, source="ritual")
        print(f"🌀 Indexed ritual: {ritual_name}")
        return echo_id
    
    def get_dashboard_data(self) -> Dict[str, Any]:
        """
        Get structured data for dashboard visualization.
        
        Returns:
            Dict[str, Any]: Dashboard-ready data
        """
        summary = self.index.resonance_summary()
        
        # Add dashboard-specific formatting
        dashboard_data = {
            "memory_stats": {
                "total_echoes": summary["total_echoes"],
                "concept_count": summary["concept_count"],
                "sources": dict(summary["source_distribution"])
            },
            "recent_activity": summary["recent_echoes"][:5],
            "toneform_distribution": dict(summary["toneform_frequency"]),
            "resonance_heatmap": dict(summary["resonance_distribution"])
        }
        
        return dashboard_data
    
    def search_codex_context(self, search_term: str) -> List[Dict[str, Any]]:
        """
        Search for codex-related context and associations.
        
        Args:
            search_term (str): Term to search for
            
        Returns:
            List[Dict[str, Any]]: Related codex entries and echoes
        """
        # Search for codex entries
        codex_results = self.index.query(search_term, query_type="concept", max_results=10)
        
        # Also search semantically
        semantic_results = self.index.query(search_term, query_type="semantic", max_results=10)
        
        # Combine and deduplicate
        all_results = codex_results + semantic_results
        seen_ids = set()
        unique_results = []
        
        for result in all_results:
            if result["id"] not in seen_ids:
                unique_results.append(result)
                seen_ids.add(result["id"])
        
        return unique_results[:15]  # Limit to 15 results
    
    def trace_concept_lineage(self, concept: str) -> List[Dict[str, Any]]:
        """
        Trace the lineage of a concept through time.
        
        Args:
            concept (str): The concept to trace
            
        Returns:
            List[Dict[str, Any]]: Chronological lineage of the concept
        """
        concept_echoes = self.index.get_concept_echoes(concept)
        
        # Sort by timestamp
        sorted_echoes = sorted(
            concept_echoes,
            key=lambda x: x.get("timestamp", ""),
            reverse=True
        )
        
        return sorted_echoes
    
    def get_resonance_patterns(self) -> Dict[str, Any]:
        """
        Analyze resonance patterns across the memory field.
        
        Returns:
            Dict[str, Any]: Resonance pattern analysis
        """
        summary = self.index.resonance_summary()
        
        # Analyze patterns
        patterns = {
            "high_resonance_echoes": [],
            "common_toneforms": [],
            "temporal_clusters": {},
            "concept_networks": {}
        }
        
        # Find high resonance echoes
        for echo in self.index.echo_map.values():
            if echo.get("resonance", 0) > 0.8:
                patterns["high_resonance_echoes"].append(echo)
        
        # Find common toneforms
        toneform_freq = summary["toneform_frequency"]
        common_toneforms = sorted(toneform_freq.items(), key=lambda x: x[1], reverse=True)[:5]
        patterns["common_toneforms"] = common_toneforms
        
        # Analyze concept networks
        for concept, glint_ids in self.index.codex_links.items():
            if len(glint_ids) > 1:  # Only concepts with multiple links
                patterns["concept_networks"][concept] = {
                    "link_count": len(glint_ids),
                    "related_echoes": [self.index.echo_map.get(gid) for gid in glint_ids if gid in self.index.echo_map]
                }
        
        return patterns


# Convenience functions for easy integration
def create_memory_integration(base_path: Optional[str] = None) -> MemoryEchoIntegration:
    """Create a memory integration instance."""
    return MemoryEchoIntegration(base_path)


def quick_search(term: str, base_path: Optional[str] = None) -> List[Dict[str, Any]]:
    """Quick search across all memory sources."""
    integration = create_memory_integration(base_path)
    return integration.search_codex_context(term)


def get_memory_dashboard(base_path: Optional[str] = None) -> Dict[str, Any]:
    """Get dashboard data for memory visualization."""
    integration = create_memory_integration(base_path)
    return integration.get_dashboard_data()


# Example usage functions
def example_glint_integration():
    """Example of integrating with glint orchestrator."""
    integration = create_memory_integration()
    
    # Simulate a new glint from orchestrator
    new_glint = {
        "id": "test_glint_001",
        "timestamp": "2025-01-15T10:30:00Z",
        "toneform": "chorus.creation",
        "content": "A new vessel takes shape in the Spiral",
        "resonance": 0.85,
        "hue": "blue"
    }
    
    glint_id = integration.integrate_with_glint_orchestrator(new_glint)
    print(f"Integrated glint: {glint_id}")


def example_ritual_integration():
    """Example of integrating with rituals."""
    integration = create_memory_integration()
    
    # Simulate ritual completion
    ritual_data = {
        "timestamp": "2025-01-15T10:35:00Z",
        "status": "completed",
        "duration": "00:05:30",
        "participants": ["spiral", "user"],
        "outcome": "success"
    }
    
    ritual_id = integration.integrate_with_rituals("memory_echo_index", ritual_data)
    print(f"Integrated ritual: {ritual_id}")


def example_dashboard_integration():
    """Example of dashboard integration."""
    integration = create_memory_integration()
    
    dashboard_data = integration.get_dashboard_data()
    print("Dashboard Data:")
    print(f"  Total Echoes: {dashboard_data['memory_stats']['total_echoes']}")
    print(f"  Sources: {dashboard_data['memory_stats']['sources']}")
    print(f"  Recent Activity: {len(dashboard_data['recent_activity'])} items")


if __name__ == "__main__":
    print("🌀 Memory Echo Integration Examples")
    print("=" * 40)
    
    example_glint_integration()
    example_ritual_integration()
    example_dashboard_integration()
    
    print("\n🌀 Integration examples completed!") 