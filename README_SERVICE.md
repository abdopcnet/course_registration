Service install notes (macOS launchd)

Files added
- launchd/com.course_registration.student.plist — the launchd property list that runs the venv python and manage.py runserver bound to 127.0.0.1:8000
- scripts/install_service.sh — copies the plist to ~/Library/LaunchAgents and loads it
- scripts/restart_service.sh — unloads and loads the plist to restart the service

Install and start the service (macOS, per-user)

1. Make the helper scripts executable:

```bash
chmod +x ./scripts/install_service.sh ./scripts/restart_service.sh
```

2. Install the service (this copies the plist to ~/Library/LaunchAgents and loads it):

```bash
./scripts/install_service.sh
```

3. Restart service later with:

```bash
./scripts/restart_service.sh
```

4. View logs:

```bash
tail -f ./logs/student.stdout.log
tail -f ./logs/student.stderr.log
```

Notes & caveats
- The plist references an absolute path to the venv python inside this repo: `/Users/abdallaswayeb/Desktop/course_registration/.venv/bin/python`. If your environment or path differs, update `launchd/com.course_registration.student.plist` accordingly.
- The plist runs `manage.py runserver 127.0.0.1:8000`. This is fine for development but not recommended for production. For production, run the app under Gunicorn or similar and use a reverse proxy.
- The service runs as the current user (per-user LaunchAgents). To run system-wide use `/Library/LaunchDaemons` (requires root) and adapt plist ownership/paths.

If you want me to install and start the service for you, say "please install service" and I'll run the install script. If you'd rather I only produce the files and let you run installation locally, say "I'll install myself".
