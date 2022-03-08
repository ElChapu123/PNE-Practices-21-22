from pathlib import Path

FILENAME = "RNU6_269P"

file_contents = Path(FILENAME).read_text()

print(file_contents)