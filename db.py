import os

file_path = os.path.join("data", "output", "topics.txt")

print("Looking for file at:", file_path)

if not os.path.exists(file_path):
    print(f"⚠️ Warning: {file_path} does not exist!")
    open(file_path, "w").close()  # Create an empty file
    print(f"✅ Created missing file: {file_path}")

with open(file_path, "r") as file:
    topics = file.read()
    print("File content:", topics)
