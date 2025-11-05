#!/usr/bin/env bash
# Install the launchd plist into the current user's LaunchAgents and load it.
# Usage: ./scripts/install_service.sh

set -euo pipefail

PLIST_SRC="$(pwd)/launchd/com.course_registration.student.plist"
PLIST_DEST="$HOME/Library/LaunchAgents/com.course_registration.student.plist"

mkdir -p "$HOME/Library/LaunchAgents"
cp "$PLIST_SRC" "$PLIST_DEST"
chmod 644 "$PLIST_DEST"

echo "Copied plist to $PLIST_DEST"

# Create logs dir
mkdir -p "$(pwd)/logs"

echo "Loading service..."
# Try unload then load to restart if present
launchctl unload "$PLIST_DEST" 2>/dev/null || true
launchctl load "$PLIST_DEST"

echo "Service installed and loaded. To see logs: tail -f $(pwd)/logs/student.stdout.log"
