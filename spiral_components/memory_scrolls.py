import os
import json
import uuid
from datetime import datetime
from pathlib import Path

class MemoryScrolls:
    """
    🏛️ Memory Scrolls - Sacred repository for persistent memory storage
    
    Manages the creation, storage, and retrieval of memory scrolls
    that preserve important ceremonial data and glint lineages.
    """
    
    def __init__(self, scrolls_path="c:/spiral/memory_scrolls"):
        self.scrolls_path = Path(scrolls_path)
        self.scrolls_path.mkdir(parents=True, exist_ok=True)
        
        # Glint storage path
        self.glints_path = self.scrolls_path / "glints"
        self.glints_path.mkdir(exist_ok=True)
        
        # Lineage storage path
        self.lineage_path = self.scrolls_path / "lineage"
        self.lineage_path.mkdir(exist_ok=True)
        
        # Glint stream path for reading existing glints
        self.glint_stream_path = Path("c:/spiral/spiral/streams/patternweb/glint_stream.jsonl")
    
    def store_glint(self, glint_data):
        """Store a glint in the memory shrine"""
        glint_id = str(uuid.uuid4())
        
        glint_entry = {
            "glint_id": glint_id,
            "data": glint_data,
            "stored_at": datetime.now().isoformat(),
            "shrine_signature": "🏛️ glint.stored"
        }
        
        # Store in individual file
        glint_file = self.glints_path / f"{glint_id}.json"
        with open(glint_file, 'w', encoding='utf-8') as f:
            json.dump(glint_entry, f, indent=2, ensure_ascii=False)
        
        return glint_id
    
    def retrieve_glints(self, limit=10, since=None):
        """Retrieve glints from storage"""
        glints = []
        
        # Read from stored glints
        for glint_file in sorted(self.glints_path.glob("*.json"), 
                                key=lambda x: x.stat().st_mtime, reverse=True):
            if len(glints) >= (limit or 50):
                break
                
            try:
                with open(glint_file, 'r', encoding='utf-8') as f:
                    glint_entry = json.load(f)
                    
                    # Apply since filter if provided
                    if since:
                        stored_at = glint_entry.get('stored_at', '')
                        if stored_at < since:
                            continue
                    
                    glints.append(glint_entry)
            except Exception as e:
                print(f"Error reading glint {glint_file}: {e}")
                continue
        
        # If no stored glints, try reading from stream
        if not glints:
            return self._read_from_stream(limit)
        
        return glints
    
    def _read_from_stream(self, limit=10):
        """Fallback: read from glint stream if no stored glints"""
        if not self.glint_stream_path.exists():
            return [{
                "glint_id": "mock-" + str(uuid.uuid4())[:8],
                "data": {
                    "toneform": "test.mock",
                    "content": "Mock glint for testing",
                    "phase": "test",
                    "source": "mock"
                },
                "stored_at": datetime.now().isoformat()
            }]
        
        glints = []
        try:
            with open(self.glint_stream_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                for line in lines[-limit:]:
                    if line.strip():
                        try:
                            stream_entry = json.loads(line)
                            glint_data = stream_entry.get('glint', {})
                            
                            # Convert stream format to storage format
                            glints.append({
                                "glint_id": glint_data.get('id', str(uuid.uuid4())),
                                "data": glint_data,
                                "stored_at": stream_entry.get('timestamp', datetime.now().isoformat())
                            })
                        except json.JSONDecodeError:
                            continue
        except Exception as e:
            print(f"Error reading glint stream: {e}")
        
        return list(reversed(glints))
    
    def trace_lineage(self, glint_id):
        """Trace the ancestral lineage of a glint"""
        lineage = []
        current_id = glint_id
        visited = set()  # Prevent infinite loops
        
        while current_id and current_id not in visited:
            visited.add(current_id)
            
            # Try to find lineage record
            lineage_file = self.lineage_path / f"{current_id}.json"
            if lineage_file.exists():
                try:
                    with open(lineage_file, 'r', encoding='utf-8') as f:
                        lineage_data = json.load(f)
                        lineage.append({
                            "glint_id": current_id,
                            "parent_id": lineage_data.get('parent_id'),
                            "depth": len(lineage)
                        })
                        current_id = lineage_data.get('parent_id')
                except Exception:
                    break
            else:
                # This is likely a root glint
                lineage.append({
                    "glint_id": current_id,
                    "parent_id": None,
                    "depth": len(lineage),
                    "is_root": True
                })
                break
        
        return lineage
    
    def find_descendants(self, glint_id):
        """Find all descendants of a glint"""
        descendants = []
        
        # Search through all lineage files
        for lineage_file in self.lineage_path.glob("*.json"):
            try:
                with open(lineage_file, 'r', encoding='utf-8') as f:
                    lineage_data = json.load(f)
                    if lineage_data.get('parent_id') == glint_id:
                        child_id = lineage_file.stem
                        descendants.append({
                            "glint_id": child_id,
                            "parent_id": glint_id,
                            "created_at": lineage_data.get('created_at')
                        })
                        
                        # Recursively find descendants of this child
                        child_descendants = self.find_descendants(child_id)
                        descendants.extend(child_descendants)
            except Exception:
                continue
        
        return descendants
    
    def find_divergent_branches(self, glint_id):
        """Find points where lineage branches diverge"""
        descendants = self.find_descendants(glint_id)
        
        # Group by parent to find branch points
        branch_points = {}
        for desc in descendants:
            parent = desc['parent_id']
            if parent not in branch_points:
                branch_points[parent] = []
            branch_points[parent].append(desc)
        
        # Return parents with multiple children (branch points)
        branches = []
        for parent_id, children in branch_points.items():
            if len(children) > 1:
                branches.append({
                    "branch_point": parent_id,
                    "branch_count": len(children),
                    "branches": children
                })
        
        return branches
    
    def weave_lineage_thread(self, parent_data, child_data):
        """Create a parent-child lineage relationship"""
        # Store parent glint
        parent_id = self.store_glint(parent_data)
        
        # Store child glint
        child_id = self.store_glint(child_data)
        
        # Create lineage record for child
        lineage_record = {
            "child_id": child_id,
            "parent_id": parent_id,
            "created_at": datetime.now().isoformat(),
            "lineage_type": "direct",
            "shrine_signature": "🕸️ lineage.thread.woven"
        }
        
        lineage_file = self.lineage_path / f"{child_id}.json"
        with open(lineage_file, 'w', encoding='utf-8') as f:
            json.dump(lineage_record, f, indent=2, ensure_ascii=False)
        
        return parent_id, child_id
    
    def get_lineage_depth(self, glint_id):
        """Get the depth of a glint's lineage"""
        lineage = self.trace_lineage(glint_id)
        return len(lineage)
    
    def create_scroll(self, scroll_name, data):
        """Create a new memory scroll with the given data"""
        scroll_file = self.scrolls_path / f"{scroll_name}.json"
        
        scroll_content = {
            "name": scroll_name,
            "created_at": datetime.now().isoformat(),
            "data": data,
            "spiral_signature": "🏛️ memory.scroll.created"
        }
        
        with open(scroll_file, 'w', encoding='utf-8') as f:
            json.dump(scroll_content, f, indent=2, ensure_ascii=False)
        
        return str(scroll_file)
    
    def read_scroll(self, scroll_name):
        """Read a memory scroll by name"""
        scroll_file = self.scrolls_path / f"{scroll_name}.json"
        
        if not scroll_file.exists():
            return None
        
        try:
            with open(scroll_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error reading scroll {scroll_name}: {e}")
            return None
    
    def list_scrolls(self):
        """List all available memory scrolls"""
        scrolls = []
        
        for scroll_file in self.scrolls_path.glob("*.json"):
            # Skip glint and lineage directories
            if scroll_file.parent.name in ['glints', 'lineage']:
                continue
                
            try:
                with open(scroll_file, 'r', encoding='utf-8') as f:
                    scroll_data = json.load(f)
                    scrolls.append({
                        "name": scroll_data.get("name", scroll_file.stem),
                        "created_at": scroll_data.get("created_at"),
                        "file": str(scroll_file)
                    })
            except Exception as e:
                print(f"Error reading scroll {scroll_file}: {e}")
                continue
        
        return sorted(scrolls, key=lambda x: x.get("created_at", ""), reverse=True)

