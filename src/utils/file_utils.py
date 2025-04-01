import os
from typing import Optional

def ensure_directory_exists(path: str):
    """Ensure a directory exists, create if it doesn't"""
    os.makedirs(path, exist_ok=True)

def get_output_path(input_path: str, output_dir: str) -> Optional[str]:
    """Generate output path based on input path"""
    if not input_path or not os.path.exists(input_path):
        return None
    
    base_name = os.path.basename(input_path)
    name_without_ext = os.path.splitext(base_name)[0]
    return os.path.join(output_dir, f"{name_without_ext}.json")