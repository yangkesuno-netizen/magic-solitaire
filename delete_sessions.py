import os

sessions_dir = r'C:\Users\User\.copaw\sessions'
current_session = "default_1773827819897.json"

files = os.listdir(sessions_dir)

print("=== Sessions Directory Contents ===")
for f in sorted(files):
    filepath = os.path.join(sessions_dir, f)
    size_mb = os.path.getsize(filepath) / (1024 * 1024)
    print(f"  {f}: {size_mb:.2f} MB")

print("\n=== Deleting Large Files ===")
for f in files:
    filepath = os.path.join(sessions_dir, f)
    size_mb = os.path.getsize(filepath) / (1024 * 1024)
    
    if size_mb > 3 and f != current_session:
        try:
            os.remove(filepath)
            print(f"  [DELETED] {f} ({size_mb:.2f} MB)")
        except Exception as e:
            print(f"  [FAILED] {f}: {e}")
    elif f == current_session:
        print(f"  [SKIPPED] {f} (current session)")

print("\n=== After Deletion ===")
files = os.listdir(sessions_dir)
for f in sorted(files):
    filepath = os.path.join(sessions_dir, f)
    size_mb = os.path.getsize(filepath) / (1024 * 1024)
    print(f"  {f}: {size_mb:.2f} MB")
