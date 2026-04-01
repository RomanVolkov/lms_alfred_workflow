#!/bin/bash
set -e

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUTPUT="$REPO_ROOT/release/lms_alfred.alfredworkflow"

cd "$REPO_ROOT"

sips -s format png "/Applications/LM Studio.app/Contents/Resources/icon.icns" \
    --out icon.png -z 256 256 2>/dev/null
echo "icon OK"

plutil -lint info.plist && echo "plist OK"
python3 -c "import ast; ast.parse(open('src/filter.py').read())" && echo "src/filter.py OK"
python3 -c "import ast; ast.parse(open('src/action.py').read())" && echo "src/action.py OK"

mkdir -p release
rm -f "$OUTPUT"
zip -r "$OUTPUT" info.plist icon.png src/
echo "built: $OUTPUT"
