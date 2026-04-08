import os
import glob

sessions_dir = r'C:\Users\User\.copaw\sessions'

print("=== Sessions Directory Contents ===")
files = os.listdir(sessions_dir)
for f in sorted(files):
    filepath = os.path.join(sessions_dir, f)
    size_mb = os.path.getsize(filepath) / (1024 * 1024)
    print(f"  {f}: {size_mb:.2f} MB")

# Find large files (> 3MB)
large_files = []
for f in files:
    filepath = os.path.join(sessions_dir, f)
    size_mb = os.path.getsize(filepath) / (1024 * 1024)
    if size_mb > 3:
        large_files.append((f, size_mb))

print(f"\n=== Large Files (>3MB) ===")
for f, size in large_files:
    print(f"  {f}: {size:.2f} MB")

# Delete large files (except current session)
current_session = "default_1773827819897.json"
print(f"\n=== Deleting Large Files ===")
for f, size in large_files:
    if f != current_session:
        filepath = os.path.join(sessions_dir, f)
        try:
            os.remove(filepath)
            print(f"  ✓ Deleted: {f} ({size:.2f} MB)")
        except Exception as e:
            print(f"  ✗ Failed to delete {f}: {e}")
    else:
        print(f"  ⊘ Skipped (current session): {f}")

print("\n=== After Deletion ===")
files = os.listdir(sessions_dir)
for f in sorted(files):
    filepath = os.path.join(sessions_dir, f)
    size_mb = os.path.getsize(filepath) / (1024 * 1024)
    print(f"  {f}: {size_mb:.2f} MB")
