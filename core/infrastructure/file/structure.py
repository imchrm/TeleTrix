import yaml
import os
from typing import Dict, Any, Optional
from pathlib import Path

class StructureBase:
    """Base class for YAML data structures with universal loading methods."""
    
    @staticmethod
    def load_yaml(file_path: str) -> Dict[str, Any]:
        """Load YAML file and return its content as dictionary.
        
        Args:
            file_path (str): Path to the YAML file
            
        Returns:
            Dict[str, Any]: Parsed YAML content
            
        Raises:
            FileNotFoundError: If YAML file doesn't exist
            yaml.YAMLError: If YAML parsing fails
        """
        try:
            with open(file_path, 'r') as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            raise FileNotFoundError(f"YAML file not found: {file_path}")
        except yaml.YAMLError as e:
            raise yaml.YAMLError(f"Error parsing YAML file {file_path}: {str(e)}")

    @staticmethod
    def save_yaml(data: Dict[str, Any], file_path: str) -> None:
        """Save dictionary data to YAML file.
        
        Args:
            data (Dict[str, Any]): Data to save
            file_path (str): Path where to save the YAML file
        """
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as file:
            yaml.dump(data, file, default_flow_style=False)

    @staticmethod
    def get_config_path(filename: str) -> str:
        """Generate full path for config files.
        
        Args:
            filename (str): Name of the YAML file
            
        Returns:
            str: Full path to the config file
        """
        base_path = Path("core/config")
        return str(base_path / filename)