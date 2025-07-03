# spiral/toneformat.py

from typing import Dict, Optional, Any, List, Union

class ToneFormat:
    """
    A class representing a structured toneform for agent communication.
    
    Attributes:
        phase (str): The breath phase (e.g., Inhale, Hold, Exhale, Return, Witness)
        toneform (str): The toneform string (e.g., Memory.Trace.Invoke)
        context (Optional[str]): Optional context information
        metadata (Dict[str, Any]): Optional metadata dictionary
    """
    
    def __init__(
        self, 
        phase: str, 
        toneform: str, 
        context: Optional[str] = None, 
        metadata: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize a ToneFormat object.
        
        Args:
            phase (str): The breath phase (e.g., Inhale, Hold, Exhale, Return, Witness)
            toneform (str): The toneform string (e.g., Memory.Trace.Invoke)
            context (Optional[str], optional): Optional context information. Defaults to None.
            metadata (Optional[Dict[str, Any]], optional): Optional metadata dictionary. Defaults to None.
        """
        self.phase = phase
        self.toneform = toneform
        self.context = context
        self.metadata = metadata or {}
    
    def __str__(self) -> str:
        """
        Return the string representation of the ToneFormat.
        
        Returns:
            str: The formatted toneform string
        """
        result = f"{self.phase}.{self.toneform}"
        if self.context:
            result += f".{self.context}"
        return result
    
    @classmethod
    def parse(cls, toneformat_str: str) -> 'ToneFormat':
        """
        Parse a toneformat string into a ToneFormat object.
        
        Args:
            toneformat_str (str): The toneformat string to parse
            
        Returns:
            ToneFormat: A new ToneFormat object
            
        Examples:
            >>> ToneFormat.parse("Hold.Diagnostics.Whisper")
            ToneFormat(phase="Hold", toneform="Diagnostics.Whisper")
            
            >>> ToneFormat.parse("Exhale.Memory.Trace.Invoke.contextinfo")
            ToneFormat(phase="Exhale", toneform="Memory.Trace", context="Invoke.contextinfo")
        """
        parts = toneformat_str.split('.')
        
        if not parts:
            return cls("Exhale", "Unknown")
        
        # First part is always the phase
        phase = parts[0]
        
        if len(parts) == 1:
            # Only phase is provided
            return cls(phase, "")
        
        if len(parts) == 2:
            # Phase and toneform are provided
            return cls(phase, parts[1])
        
        # If we have more than 2 parts, the second part is the toneform
        # and the rest is context
        toneform = parts[1]
        
        # For more complex toneforms like "Memory.Trace", combine parts[1] and parts[2]
        if len(parts) >= 3:
            if parts[1].lower() in ["memory", "diagnostics", "pattern", "toneformat", "harmony"]:
                toneform = f"{parts[1]}.{parts[2]}"
                context = '.'.join(parts[3:]) if len(parts) > 3 else None
            else:
                # Otherwise, everything after the phase and toneform is context
                context = '.'.join(parts[2:])
        else:
            context = None
            
        return cls(phase, toneform, context)
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the ToneFormat to a dictionary.
        
        Returns:
            Dict[str, Any]: Dictionary representation of the ToneFormat
        """
        result = {
            "phase": self.phase,
            "toneform": self.toneform
        }
        
        if self.context:
            result["context"] = self.context
            
        if self.metadata:
            result["metadata"] = self.metadata
            
        return result
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ToneFormat':
        """
        Create a ToneFormat from a dictionary.
        
        Args:
            data (Dict[str, Any]): Dictionary containing ToneFormat data
            
        Returns:
            ToneFormat: A new ToneFormat object
        """
        return cls(
            phase=data.get("phase", "Exhale"),
            toneform=data.get("toneform", ""),
            context=data.get("context"),
            metadata=data.get("metadata")
        )
    
    def with_metadata(self, **kwargs) -> 'ToneFormat':
        """
        Create a new ToneFormat with additional metadata.
        
        Args:
            **kwargs: Keyword arguments to add to metadata
            
        Returns:
            ToneFormat: A new ToneFormat with updated metadata
        """
        new_metadata = self.metadata.copy()
        new_metadata.update(kwargs)
        
        return ToneFormat(
            phase=self.phase,
            toneform=self.toneform,
            context=self.context,
            metadata=new_metadata
        )