#!/usr/bin/env bash
set -euo pipefail

SERVICE_NAME="course_service"
PROJECT_DIR="/var/www/course_registration"
VENV_DIR="$PROJECT_DIR/.venv"
GUNICORN_BIN="$VENV_DIR/bin/gunicorn"
SERVICE_FILE="/etc/systemd/system/${SERVICE_NAME}.service"
LOG_DIR="$PROJECT_DIR/logs"
WORKERS=4

usage(){
  cat <<EOF
Usage: $0 {install|uninstall|start|stop|restart|status}

install   - write systemd unit and enable the service (requires sudo)
uninstall - stop, disable and remove the unit file (requires sudo)
start     - start service (systemctl start)
stop      - stop service
restart   - restart service
status    - show service status
EOF
}

if [ "$#" -ne 1 ]; then
  usage; exit 1
fi

cmd="$1"

owner_user=$(stat -c '%U' "$PROJECT_DIR" 2>/dev/null || echo root)
owner_group=$(stat -c '%G' "$PROJECT_DIR" 2>/dev/null || echo root)

unit_content(){
  cat <<UNIT
[Unit]
Description=Course Registration Django application
After=network.target

[Service]
Type=simple
User=${owner_user}
Group=${owner_group}
WorkingDirectory=${PROJECT_DIR}
Environment=PATH=${VENV_DIR}/bin
ExecStart=${GUNICORN_BIN} course_registration.wsgi:application --bind 0.0.0.0:8000 --workers ${WORKERS}
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
UNIT
}

case "$cmd" in
  install)
    if [ "$(id -u)" -ne 0 ]; then
      echo "install must be run as root or with sudo"; exit 1
    fi
    mkdir -p "$LOG_DIR"
    chown -R ${owner_user}:${owner_group} "$LOG_DIR" || true
    echo "Writing systemd unit to $SERVICE_FILE"
    unit_content > "$SERVICE_FILE"
    chmod 644 "$SERVICE_FILE"
    systemctl daemon-reload
    systemctl enable --now "$SERVICE_NAME"
    echo "Service installed and started. Use: service ${SERVICE_NAME} start|stop|restart|status"
    ;;

  uninstall)
    if [ "$(id -u)" -ne 0 ]; then
      echo "uninstall must be run as root or with sudo"; exit 1
    fi
    systemctl stop "$SERVICE_NAME" 2>/dev/null || true
    systemctl disable "$SERVICE_NAME" 2>/dev/null || true
    if [ -f "$SERVICE_FILE" ]; then
      rm -f "$SERVICE_FILE"
      systemctl daemon-reload
      echo "Service unit removed"
    else
      echo "Service unit not found: $SERVICE_FILE"
    fi
    ;;

  start)
    systemctl start "$SERVICE_NAME"
    ;;

  stop)
    systemctl stop "$SERVICE_NAME"
    ;;

  restart)
    systemctl restart "$SERVICE_NAME"
    ;;

  status)
    systemctl status "$SERVICE_NAME" --no-pager
    ;;

  *)
    usage; exit 1
    ;;
esac

exit 0
