import os
import hashlib

def hash_file(filepath):
    """Returns the SHA-256 hash of the file."""
    hasher = hashlib.sha256()
    with open(filepath, 'rb') as file:
        buf = file.read()
        hasher.update(buf)
    return hasher.hexdigest()

def find_and_remove_duplicates(directory):
    """Finds and removes duplicate files in the given directory."""
    files_by_hash = {}
    duplicates = []

    for dirpath, _, filenames in os.walk(directory):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            file_hash = hash_file(filepath)

            if file_hash in files_by_hash:
                duplicates.append((files_by_hash[file_hash], filepath))
                os.remove(filepath)  # Remove the duplicate file
            else:
                files_by_hash[file_hash] = filepath

    return duplicates

directory_path = '.'
duplicates = find_and_remove_duplicates(directory_path)

if duplicates:
    print("Duplicate files found and removed:")
    for original, duplicate in duplicates:
        print(f"Original: {original} <-> Duplicate removed: {duplicate}")
else:
    print("No duplicate files found.")
