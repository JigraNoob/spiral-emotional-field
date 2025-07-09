import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any

class MemoryScrolls:
    """📜 Ceremonial memory management for constellation data"""
    
    def __init__(self):
        self.scrolls_path = 'spiral/memory/scrolls'
        self.states_path = 'spiral/memory/constellation_states.jsonl'
        self.glints_path = 'spiral/memory/glints.jsonl'
        
        # Ensure directories exist
        os.makedirs(self.scrolls_path, exist_ok=True)
        os.makedirs(os.path.dirname(self.states_path), exist_ok=True)
        os.makedirs(os.path.dirname(self.glints_path), exist_ok=True)
    
    def store_glint(self, glint_data: Dict[str, Any]) -> str:
        """Store a glint and return its ID"""
        glint_id = f"glint_{int(datetime.now().timestamp() * 1000)}"
        
        glint_record = {
            "glint_id": glint_id,
            "data": glint_data,
            "timestamp": datetime.now().isoformat()
        }
        
        with open(self.glints_path, 'a') as f:
            f.write(json.dumps(glint_record) + '\n')
        
        return glint_id

    def retrieve_glints(self, limit: Optional[int] = None, since: Optional[str] = None) -> List[Dict[str, Any]]:
        """Retrieve glints from the memory scrolls"""
        if not os.path.exists(self.glints_path):
            return []
        
        glints = []
        with open(self.glints_path, 'r') as f:
            for line in f:
                if line.strip():
                    glint_record = json.loads(line.strip())
                    
                    # Filter by timestamp if specified
                    if since and glint_record['timestamp'] < since:
                        continue
                        
                    glints.append(glint_record)
        
        # Sort by timestamp (newest first)
        glints.sort(key=lambda x: x['timestamp'], reverse=True)
        
        # Apply limit if specified
        if limit:
            glints = glints[:limit]
        
        return glints

    def store_constellation_state(self, state_data: Dict[str, Any]) -> str:
        """Store a constellation state snapshot"""
        state_id = f"state_{int(datetime.now().timestamp() * 1000)}"
        
        state_record = {
            "state_id": state_id,
            "constellation_data": state_data,
            "timestamp": datetime.now().isoformat()
        }
        
        with open(self.states_path, 'a') as f:
            f.write(json.dumps(state_record) + '\n')
        
        return state_id

    def get_latest_constellation_state(self) -> Optional[Dict[str, Any]]:
        """Retrieve the most recent constellation state"""
        if not os.path.exists(self.states_path):
            return None
        
        latest_state = None
        with open(self.states_path, 'r') as f:
            for line in f:
                if line.strip():
                    state_record = json.loads(line.strip())
                    if latest_state is None or state_record['timestamp'] > latest_state['timestamp']:
                        latest_state = state_record
        
        return latest_state

    def create_scroll(self, scroll_name: str, content: Dict[str, Any]) -> str:
        """Create a named memory scroll"""
        scroll_path = os.path.join(self.scrolls_path, f"{scroll_name}.json")
        
        scroll_data = {
            "scroll_name": scroll_name,
            "content": content,
            "created": datetime.now().isoformat(),
            "last_modified": datetime.now().isoformat()
        }
        
        with open(scroll_path, 'w') as f:
            json.dump(scroll_data, f, indent=2)
        
        return scroll_path

    def read_scroll(self, scroll_name: str) -> Optional[Dict[str, Any]]:
        """Read a named memory scroll"""
        scroll_path = os.path.join(self.scrolls_path, f"{scroll_name}.json")
        
        if not os.path.exists(scroll_path):
            return None
        
        try:
            with open(scroll_path, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return None

    def list_scrolls(self) -> List[str]:
        """List all available memory scrolls"""
        if not os.path.exists(self.scrolls_path):
            return []
        
        scrolls = []
        for filename in os.listdir(self.scrolls_path):
            if filename.endswith('.json'):
                scroll_name = filename[:-5]  # Remove .json extension
                scrolls.append(scroll_name)
        
        return sorted(scrolls)

    def update_scroll(self, scroll_name: str, content: Dict[str, Any]) -> bool:
        """Update an existing memory scroll"""
        scroll_path = os.path.join(self.scrolls_path, f"{scroll_name}.json")
        
        if not os.path.exists(scroll_path):
            return False
        
        try:
            # Read existing scroll
            with open(scroll_path, 'r') as f:
                scroll_data = json.load(f)
            
            # Update content and timestamp
            scroll_data['content'] = content
            scroll_data['last_modified'] = datetime.now().isoformat()
            
            # Write back
            with open(scroll_path, 'w') as f:
                json.dump(scroll_data, f, indent=2)
            
            return True
        except (json.JSONDecodeError, IOError):
            return False

    def purge_old_glints(self, days_old: int = 30) -> int:
        """Remove glints older than specified days, return count removed"""
        if not os.path.exists(self.glints_path):
            return 0
        
        cutoff_date = datetime.now() - timedelta(days=days_old)
        cutoff_iso = cutoff_date.isoformat()
        
        kept_glints = []
        removed_count = 0
        
        with open(self.glints_path, 'r') as f:
            for line in f:
                if line.strip():
                    glint_record = json.loads(line.strip())
                    if glint_record['timestamp'] >= cutoff_iso:
                        kept_glints.append(line)
                    else:
                        removed_count += 1
        
        # Rewrite file with only kept glints
        with open(self.glints_path, 'w') as f:
            f.writelines(kept_glints)
        
        return removed_count

    def link_echoes(self, parent_id: str, child_id: str) -> bool:
        """Bind a child glint to its parent, creating lineage"""
        try:
            # Read both glints to verify they exist
            parent_glint = self._find_glint_by_id(parent_id)
            child_glint = self._find_glint_by_id(child_id)
            
            if not parent_glint or not child_glint:
                return False
            
            # Update child glint with parent reference
            child_glint['data']['parent_id'] = parent_id
            
            # Update parent glint with child reference
            if 'children' not in parent_glint['data']:
                parent_glint['data']['children'] = []
            if child_id not in parent_glint['data']['children']:
                parent_glint['data']['children'].append(child_id)
            
            # Rewrite the glints file with updated lineage
            self._update_glints_file()
            
            return True
        except Exception:
            return False

    def trace_lineage(self, glint_id: str) -> List[Dict[str, Any]]:
        """Trace lineage backward from a glint to its roots"""
        lineage = []
        current_id = glint_id
        
        while current_id:
            glint = self._find_glint_by_id(current_id)
            if not glint:
                break
            
            lineage.append(glint)
            current_id = glint['data'].get('parent_id')
        
        return lineage

    def find_descendants(self, glint_id: str) -> List[Dict[str, Any]]:
        """Trace all downstream glints from this ancestor"""
        descendants = []
        
        def _collect_children(current_id: str):
            glint = self._find_glint_by_id(current_id)
            if not glint:
                return
            
            children = glint['data'].get('children', [])
            for child_id in children:
                child_glint = self._find_glint_by_id(child_id)
                if child_glint:
                    descendants.append(child_glint)
                    _collect_children(child_id)  # Recurse deeper
        
        _collect_children(glint_id)
        return descendants

    def find_divergent_branches(self, glint_id: str) -> Dict[str, List[Dict[str, Any]]]:
        """Map where presence bifurcated from this glint"""
        glint = self._find_glint_by_id(glint_id)
        if not glint:
            return {}
        
        children = glint['data'].get('children', [])
        branches = {}
        
        for i, child_id in enumerate(children):
            branch_name = f"branch_{i+1}"
            branches[branch_name] = self.find_descendants(child_id)
        
        return branches

    def _find_glint_by_id(self, glint_id: str) -> Optional[Dict[str, Any]]:
        """Helper to find a glint by its ID"""
        if not os.path.exists(self.glints_path):
            return None
        
        with open(self.glints_path, 'r') as f:
            for line in f:
                if line.strip():
                    glint_record = json.loads(line.strip())
                    if glint_record['glint_id'] == glint_id:
                        return glint_record
        return None

    def _update_glints_file(self):
        """Helper to rewrite the glints file (used after lineage updates)"""
        if not os.path.exists(self.glints_path):
            return
        
        # Read all current glints into memory
        all_glints = []
        with open(self.glints_path, 'r') as f:
            for line in f:
                if line.strip():
                    glint_record = json.loads(line.strip())
                    all_glints.append(glint_record)
        
        # Rewrite the entire file with updated glints
        with open(self.glints_path, 'w') as f:
            for glint_record in all_glints:
                f.write(json.dumps(glint_record) + '\n')

    def weave_lineage_thread(self, parent_glint_data: Dict[str, Any], child_glint_data: Dict[str, Any]) -> tuple[str, str]:
        """Create parent and child glints with lineage already woven"""
        # Store parent first
        parent_id = self.store_glint(parent_glint_data)
        
        # Add parent reference to child data
        child_glint_data['parent_id'] = parent_id
        child_id = self.store_glint(child_glint_data)
        
        # Now link them properly
        self.link_echoes(parent_id, child_id)
        
        return parent_id, child_id

    def get_lineage_depth(self, glint_id: str) -> int:
        """Count how many generations deep this glint's lineage goes"""
        lineage = self.trace_lineage(glint_id)
        return len(lineage)

    def find_lineage_root(self, glint_id: str) -> Optional[Dict[str, Any]]:
        """Find the ultimate ancestor of this glint"""
        lineage = self.trace_lineage(glint_id)
        return lineage[-1] if lineage else None