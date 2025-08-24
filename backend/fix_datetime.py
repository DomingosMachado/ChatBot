import os
import re
from pathlib import Path

def fix_datetime_in_file(filepath):
    """Replace deprecated datetime.utcnow() with datetime.now(timezone.utc)."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    patterns = [
        (r'from datetime import datetime\b', 
         'from datetime import datetime, timezone'),
        (r'from datetime import ([\w, ]+)(?<!timezone)\b', 
         r'from datetime import \1, timezone'),
        (r'datetime\.utcnow\(\)', 
         'datetime.now(timezone.utc)'),
        (r'datetime\.now\(datetime\.UTC\)', 
         'datetime.now(timezone.utc)')
    ]
    
    for pattern, replacement in patterns:
        if pattern == r'from datetime import datetime\b':
            if 'timezone' not in content:
                content = re.sub(pattern, replacement, content)
        elif pattern == r'from datetime import ([\w, ]+)(?<!timezone)\b':
            if 'from datetime import' in content and 'timezone' not in content:
                content = re.sub(pattern, replacement, content)
        else:
            content = re.sub(pattern, replacement, content)
    
    if 'datetime.now(timezone.utc)' in content and 'from datetime import' in content:
        if 'timezone' not in content.split('datetime.now(timezone.utc)')[0]:
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if 'from datetime import' in line and 'timezone' not in line:
                    if line.strip().endswith('datetime'):
                        lines[i] = line.replace('datetime', 'datetime, timezone')
                    else:
                        lines[i] = line.rstrip() + ', timezone'
                    break
            content = '\n'.join(lines)
    
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    """Fix datetime usage in all Python files."""
    backend_dir = Path('.')
    
    files_to_check = [
        'agents.py',
        'logger_config.py',
        'database.py',
        'app.py'
    ]
    
    fixed_files = []
    
    for filename in files_to_check:
        filepath = backend_dir / filename
        if filepath.exists():
            if fix_datetime_in_file(filepath):
                fixed_files.append(filename)
                print(f"✓ Fixed {filename}")
            else:
                print(f"  No changes needed in {filename}")
        else:
            print(f"  File not found: {filename}")
    
    if fixed_files:
        print(f"\nFixed datetime usage in {len(fixed_files)} file(s)")
    else:
        print("\nNo datetime fixes needed")

if __name__ == "__main__":
    main()