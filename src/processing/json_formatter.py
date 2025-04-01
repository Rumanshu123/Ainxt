# In src/processing/json_formatter.py
import json
from typing import Dict, Any

class JSONFormatter:
    def __init__(self, data: Dict[str, Any]):
        self.data = self._clean_data(data)
    
    def _clean_data(self, data: Any) -> Any:
        """Recursively clean data for JSON serialization"""
        if isinstance(data, (str, int, float, bool)):
            return data
        elif isinstance(data, dict):
            return {k: self._clean_data(v) for k, v in data.items()}
        elif isinstance(data, (list, tuple)):
            return [self._clean_data(item) for item in data]
        elif hasattr(data, 'to_dict'):  # Handle pandas DataFrames
            return data.to_dict()
        elif data is None:
            return None
        else:
            return str(data)  # Fallback to string representation
    
    def format(self, indent: int = 4) -> str:
        """Convert data to JSON string"""
        return json.dumps(self.data, indent=indent, ensure_ascii=False, default=str)