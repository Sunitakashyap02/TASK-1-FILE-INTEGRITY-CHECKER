import hashlib
import os
#Function to compute sha256 hash of a file
def  get_file_hash(filename):
    """Returns the SHA-256 hash of a file"""
    sha256_hash = hashlib.sha256()
    try:
        with open(filename, "rb") as f:

            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except FileNotFoundError:
        return None
#Function to save file
def save_hash(filename, hash_value, db="hashes.txt"):
    with open(db, "a") as f:
        f.write(f"{filename},{hash_value}\n")
#Function  to load all previously stored hashes from database file
def load_hashes(db="hashes.txt"):
    hashes = {}
    if os.path.exists(db):
        with open(db, "r") as f:
            for line in f:
                name, hash_value = line.strip().split(",")
                hashes[name] = hash_value
    return hashes

def check_integrity(filename, db="hashes.txt"):
    current_hash = get_file_hash(filename)
    if current_hash is None:
        print("File not found.")
        return
    stored_hashes = load_hashes(db)
    if filename in stored_hashes:
        if stored_hashes[filename] == current_hash:
            print("✅ File is intact.")
        else:
            print("⚠️ WARNING: File has been modified!")
    else:
        print("🆕 New file detected. Saving hash.")
        save_hash(filename, current_hash, db)

# Main Execution

file_to_check = input("Enter file name to check integrity: ")
check_integrity(file_to_check)
