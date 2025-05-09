import hashlib


def calculate_file_hash(file_path):
    """Calculate the SHA256 hash of a file."""
    sha256 = hashlib.sha256()
    try:
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha256.update(chunk)
        return sha256.hexdigest()
    except FileNotFoundError:
        print(f"Error: File not found - {file_path}")
        return None

def main():
    hash_file = 'dbversion_hash.txt'
    report_file = 'dbversion_report.txt'

    # Read the hash from dbversion_hash.txt
    try:
        with open(hash_file, 'r') as f:
            expected_hash = f.read().strip()
    except FileNotFoundError:
        print(f"Error: File not found - {hash_file}")
        return

    # Calculate the hash of dbversion_report.txt
    actual_hash = calculate_file_hash(report_file)
    if actual_hash is None:
        return

    # Compare the hashes
    if actual_hash == expected_hash:
        print("The hashes match.")
    else:
        print("The hashes do not match.")

if __name__ == "__main__":
    main()
 
