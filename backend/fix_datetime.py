import fileinput
import sys

files_to_fix = ['agents.py', 'logger_config.py']

for filename in files_to_fix:
    with fileinput.FileInput(filename, inplace=True) as file:
        for line in file:
            if 'datetime.utcnow()' in line:
                line = line.replace('datetime.utcnow()', 'datetime.now(datetime.UTC)')
            sys.stdout.write(line)

print("✅ Fixed datetime deprecation warnings")