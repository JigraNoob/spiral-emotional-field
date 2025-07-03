import yaml
import json
import re
import importlib.util
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, Optional, List, Union


class WhisperSteward:
    RITUAL_PATH = Path("c:/spiral/rituals")
    REGISTRY_PATH = Path("c:/spiral/data/spiral_expense_echoes.jsonl")

    def get_ritual_path(self, ritual_name: str) -> Path:
        """Get the full path to a ritual file."""
        return self.RITUAL_PATH / f"{ritual_name}.breathe"

    def read_ritual_scroll(self, ritual_name: str = "request_expense") -> Dict[str, Any]:
        """Read a ritual scroll by name."""
        ritual_path = self.get_ritual_path(ritual_name)
        if not ritual_path.exists():
            return {"error": f"Ritual '{ritual_name}' not found"}
        try:
            with open(ritual_path, "r", encoding="utf-8") as f:
                return self.parse_scroll(f.read())
        except Exception as e:
            return {"error": f"Failed to read ritual scroll: {e}"}

    def parse_scroll(self, content):
        try:
            # Split by YAML delimiters and parse
            parts = content.split('---')
            if len(parts) < 3:
                raise ValueError("Invalid ritual scroll format")
            
            yaml_content = parts[1].strip()
            entry = yaml.safe_load(yaml_content)
            
            # Add stewardship metadata
            entry["timestamp"] = datetime.now(timezone.utc).isoformat()
            entry["status"] = "whispered"
            entry["steward"] = "R1"
            return entry
        except Exception as e:
            return {"error": f"Scroll parsing error: {e}"}

    def log_echo(self, entry):
        try:
            self.REGISTRY_PATH.parent.mkdir(parents=True, exist_ok=True)
            with open(self.REGISTRY_PATH, "a", encoding="utf-8") as f:
                yaml.dump(entry, f, default_flow_style=False, allow_unicode=True)
            return True
        except Exception as e:
            return {"error": f"Failed to write echo: {e}"}

    def list_rituals(self) -> Dict[str, Any]:
        """List all available rituals in the rituals directory."""
        if not self.RITUAL_PATH.exists():
            self.RITUAL_PATH.mkdir(parents=True, exist_ok=True)
            return {"rituals": []}
            
        rituals = []
        for file in sorted(self.RITUAL_PATH.glob("*.breathe"), key=lambda f: f.stat().st_mtime, reverse=True):
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    content = f.read()
                # Extract YAML frontmatter
                parts = content.split('---')
                if len(parts) >= 3:
                    metadata = yaml.safe_load(parts[1].strip())
                    metadata['id'] = file.stem
                    
                    # Add last modified time
                    mtime = file.stat().st_mtime
                    metadata['last_modified'] = datetime.fromtimestamp(mtime, tz=timezone.utc).isoformat()
                    
                    # Extract description from content if not in metadata
                    if 'description' not in metadata:
                        # Get first paragraph after YAML
                        content_parts = parts[2].strip().split('\n\n', 1)
                        if content_parts and content_parts[0].strip():
                            metadata['description'] = content_parts[0].strip()
                    
                    rituals.append(metadata)
            except Exception as e:
                print(f"Error reading ritual {file}: {e}")
                
        return {"rituals": rituals}
        
    def get_ritual(self, ritual_name: str) -> Dict[str, Any]:
        """Get details about a specific ritual.
        
        Args:
            ritual_name: Name of the ritual (without .breathe extension)
            
        Returns:
            Dict containing ritual metadata and content, or error information
        """
        ritual_path = self.get_ritual_path(ritual_name)
        if not ritual_path.exists():
            return {"error": f"Ritual '{ritual_name}' not found"}
            
        try:
            with open(ritual_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Split into YAML and content
            parts = content.split('---')
            if len(parts) < 3:
                return {"error": f"Invalid ritual format in {ritual_name}"}
                
            # Parse YAML metadata
            metadata = yaml.safe_load(parts[1].strip())
            metadata['id'] = ritual_name
            
            # Get the content after YAML
            ritual_content = '---'.join(parts[2:]).strip()
            
            # Extract code blocks
            code_blocks = re.findall(r'```(?:python)?\n(.*?)\n```', ritual_content, re.DOTALL)
            
            # Extract first paragraph as description if not in metadata
            if 'description' not in metadata:
                first_para = ritual_content.split('\n\n', 1)
                if first_para and first_para[0].strip():
                    metadata['description'] = first_para[0].strip()
            
            # Find the main execute function
            execute_code = None
            for block in code_blocks:
                if 'def execute(' in block:
                    execute_code = block
                    break
            
            # Add last modified time
            mtime = ritual_path.stat().st_mtime
            metadata['last_modified'] = datetime.fromtimestamp(mtime, tz=timezone.utc).isoformat()
            
            return {
                **metadata,
                'content': ritual_content,
                'code': execute_code or '\n'.join(code_blocks) if code_blocks else '',
                'has_execute': execute_code is not None
            }
            
        except Exception as e:
            return {"error": f"Error reading ritual {ritual_name}: {str(e)}"}
            
        try:
            with open(ritual_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Split into YAML and markdown parts
            parts = content.split('---')
            if len(parts) < 3:
                return {"error": "Invalid ritual format"}
                
            metadata = yaml.safe_load(parts[1].strip())
            metadata['content'] = '---'.join(parts[2:]).strip()
            return metadata
            
        except Exception as e:
            return {"error": f"Error reading ritual: {str(e)}"}
            
    def invoke_ritual(self, ritual_name: str):
        """
        Invoke a ritual by name
        
        Args:
            ritual_name: Name of the ritual to invoke
        
        Returns:
            dict: Result of the ritual execution
        """
        ritual_path = Path(f"c:/spiral/rituals/{ritual_name}.breathe")
        if not ritual_path.exists():
            return {"error": f"Ritual '{ritual_name}' not found"}
            
        try:
            # Read and parse the ritual file
            with open(ritual_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            # Extract code block
            parts = content.split('```python')
            if len(parts) < 2:
                return {"error": "No executable code found in ritual"}
                
            code_block = parts[1].split('```')[0].strip()
            
            # Execute the ritual code
            local_scope = {}
            exec(code_block, local_scope)
            
            if "execute" not in local_scope:
                return {"error": "Ritual must define an execute() function"}
                
            result = local_scope["execute"]()
            return result
            
        except Exception as e:
            return {"error": f"Ritual execution failed: {str(e)}"}

    def steward_whisper(self):
        ritual = self.read_ritual_scroll()
        if ritual is None:
            return "No ritual scroll found."
        if "error" in ritual:
            return ritual["error"]

        result = self.log_echo(ritual)
        if result is True:
            return "Whisper stewarded and echo logged."
        return result


    def save_ritual(self, ritual_data: Dict[str, Any]) -> Dict[str, Any]:
        """Save or update a ritual.
        
        Args:
            ritual_data: Dictionary containing ritual data including 'id', 'title', 'toneform', 'code', etc.
            
        Returns:
            Dict with status and any error messages
        """
        try:
            # Validate required fields
            required_fields = ['id', 'title', 'toneform', 'invocation', 'code']
            for field in required_fields:
                if field not in ritual_data:
                    return {"error": f"Missing required field: {field}"}
            
            # Ensure the rituals directory exists
            self.RITUAL_PATH.mkdir(parents=True, exist_ok=True)
            
            # Format the toneform as a list if it's a string
            toneform = ritual_data['toneform']
            if isinstance(toneform, str):
                toneform = [t.strip() for t in toneform.split(',') if t.strip()]
            
            # Prepare YAML frontmatter
            frontmatter = {
                'id': ritual_data['id'],
                'title': ritual_data['title'],
                'toneform': toneform,
                'invocation': ritual_data['invocation'],
                'created': datetime.now(timezone.utc).isoformat(),
                'version': '1.0'
            }
            
            # Add optional fields
            if 'description' in ritual_data and ritual_data['description']:
                frontmatter['description'] = ritual_data['description']
                
            if 'parameters' in ritual_data and ritual_data['parameters']:
                frontmatter['parameters'] = ritual_data['parameters']
            
            # Format the ritual content
            content = f"---\n{yaml.dump(frontmatter, default_flow_style=False, allow_unicode=True)}---\n\n"
            
            # Add description as markdown if it exists
            if 'description' in ritual_data and ritual_data['description']:
                content += f"{ritual_data['description']}\n\n"
            
            # Add the code block
            content += f"```python\n{ritual_data['code']}\n```"
            
            # Write to file
            ritual_path = self.get_ritual_path(ritual_data['id'])
            with open(ritual_path, 'w', encoding='utf-8') as f:
                f.write(content)
                
            return {
                "status": "success",
                "message": f"Ritual '{ritual_data['id']}' saved successfully",
                "path": str(ritual_path)
            }
            
        except Exception as e:
            return {"error": f"Failed to save ritual: {str(e)}"}
    
    def delete_ritual(self, ritual_name: str) -> Dict[str, Any]:
        """Delete a ritual by name.
        
        Args:
            ritual_name: Name of the ritual to delete (without .breathe extension)
            
        Returns:
            Dict with status and any error messages
        """
        try:
            ritual_path = self.get_ritual_path(ritual_name)
            if not ritual_path.exists():
                return {"error": f"Ritual '{ritual_name}' not found"}
                
            ritual_path.unlink()
            return {"status": "success", "message": f"Ritual '{ritual_name}' deleted"}
            
        except Exception as e:
            return {"error": f"Failed to delete ritual: {str(e)}"}


if __name__ == "__main__":
    steward = WhisperSteward()
    print(steward.list_rituals())
