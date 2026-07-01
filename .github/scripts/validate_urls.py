"""
Validate urls.json to ensure it contains proper JSON with 'school' and 'url' keys.
"""
import json
import sys
from pathlib import Path


def validate_urls_json(file_path: str) -> bool:
    """
    Validate the urls.json file structure.
    
    Returns:
        bool: True if validation passes, False otherwise
    """
    try:
        # Read and parse JSON file
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Check if data is a list
        if not isinstance(data, list):
            print("❌ ERROR: Root element must be an array")
            return False
        
        # Check if list is not empty
        if len(data) == 0:
            print("❌ ERROR: Array cannot be empty")
            return False
        
        # Validate each entry
        errors = []
        for idx, entry in enumerate(data):
            # Check if entry is a dictionary
            if not isinstance(entry, dict):
                errors.append(f"Entry {idx}: Must be an object, got {type(entry).__name__}")
                continue
            
            # Check for required keys
            required_keys = {'school', 'url'}
            actual_keys = set(entry.keys())
            
            if actual_keys != required_keys:
                missing = required_keys - actual_keys
                extra = actual_keys - required_keys
                
                if missing:
                    errors.append(f"Entry {idx}: Missing required keys: {missing}")
                if extra:
                    errors.append(f"Entry {idx}: Unexpected keys found: {extra}")
                continue
            
            # Validate 'school' field
            school = entry.get('school')
            if not isinstance(school, str):
                errors.append(f"Entry {idx}: 'school' must be a string, got {type(school).__name__}")
            elif not school.strip():
                errors.append(f"Entry {idx}: 'school' cannot be empty")
            
            # Validate 'url' field
            url = entry.get('url')
            if not isinstance(url, str):
                errors.append(f"Entry {idx}: 'url' must be a string, got {type(url).__name__}")
            elif not url.strip():
                errors.append(f"Entry {idx}: 'url' cannot be empty")
            elif not url.startswith(('http://', 'https://', '//')): # comments allowed
                errors.append(f"Entry {idx}: 'url' must start with http://, https://, or //")
        
        # Report results
        if errors:
            print("❌ VALIDATION FAILED\n")
            for error in errors:
                print(f"  • {error}")
            return False
        
        print(f"✅ VALIDATION PASSED")
        print(f"   • File is valid JSON")
        print(f"   • Contains {len(data)} entries")
        print(f"   • All entries have required 'school' and 'url' keys")
        return True
    
    except json.JSONDecodeError as e:
        print(f"❌ ERROR: Invalid JSON format")
        print(f"   {e}")
        return False
    
    except FileNotFoundError:
        print(f"❌ ERROR: File not found: {file_path}")
        return False
    
    except Exception as e:
        print(f"❌ ERROR: Unexpected error occurred")
        print(f"   {type(e).__name__}: {e}")
        return False


if __name__ == "__main__":
    # Path to urls.json (relative to repository root)
    urls_file = Path(__file__).parent.parent.parent / "urls.json"
    
    is_valid = validate_urls_json(urls_file)
    
    # Exit with appropriate code
    sys.exit(0 if is_valid else 1)
