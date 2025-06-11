#File Cleaning Utility Using Python Project
import os
import hashlib
from datetime import datetime

def get_file_hash(filepath):
    """Generate a SHA256 hash for the file content."""
    hasher = hashlib.sha256()
    with open(filepath, 'rb') as f:
        while chunk := f.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest()

def is_file_empty(filepath):
    """Check if file is empty or whitespace-only."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return not f.read().strip()
    except:
        # If file is binary or unreadable as text
        return os.stat(filepath).st_size == 0

def log_action(log_lines, action, filepath):
    log_lines.append(f"[{datetime.now()}] {action}: {filepath}")

def clean_directory(root_dir):
    log_lines = []
    seen_hashes = {}

    for dirpath, _, filenames in os.walk(root_dir):
        file_count = len(filenames)
        file_types = set()
        log_lines.append(f"\n[Folder] {dirpath}")
        log_lines.append(f" - Files: {file_count}")

        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            ext = os.path.splitext(filename)[1]
            file_types.add(ext.lower())

            # Handle empty files
            try:
                if is_file_empty(filepath):
                    os.remove(filepath)
                    log_action(log_lines, "Deleted empty file", filepath)
                    continue
            except Exception as e:
                log_action(log_lines, "Failed to check for empty file", f"{filepath} ({e})")
                continue

            # Handle duplicates by content
            try:
                file_hash = get_file_hash(filepath)
                if file_hash in seen_hashes:
                    os.remove(filepath)
                    log_action(log_lines, "Deleted duplicate file", filepath)
                else:
                    seen_hashes[file_hash] = filepath
            except Exception as e:
                log_action(log_lines, "Failed to process file", f"{filepath} ({e})")

        log_lines.append(f" - File Types: {', '.join(sorted(file_types)) if file_types else 'None'}")

    # Write log file
    log_path = os.path.join(root_dir, "cleanup_log.txt")
    with open(log_path, 'w', encoding='utf-8') as log_file:
        log_file.write("\n".join(log_lines))

    print(f"\nCleanup complete. Log saved to: {log_path}")

# === RUN HERE ===
target_directory = r"D:\stephen"  # Replace with your directory
clean_directory(target_directory)
