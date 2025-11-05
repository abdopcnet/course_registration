#!/usr/bin/env bash
# Restart the launchd service for the student app
# Usage: ./scripts/restart_service.sh

set -euo pipefail

PLIST_DEST="$HOME/Library/LaunchAgents/com.course_registration.student.plist"

if [ ! -f "$PLIST_DEST" ]; then
  echo "Service plist not found at $PLIST_DEST"
  echo "Install first with: ./scripts/install_service.sh"
  exit 1
fi

echo "Unloading service (if loaded)"
launchctl unload "$PLIST_DEST" 2>/dev/null || true

echo "Loading service"
launchctl load "$PLIST_DEST"

echo "Service restarted. Check logs at ./logs/student.stdout.log"
