# Database connection information

This file documents how to connect to the PostgreSQL database used by the project and includes example CLI commands and Navicat settings (direct TCP and SSH tunnel).

> Note: The project currently stores DB credentials in `course_registration/settings.py`. For production you should move credentials to environment variables and secure them.

## Credentials (from `course_registration/settings.py`)

- Database name: `courseruniversty`
- Host: `localhost`
- Port: `5432`
- Username: `abdalla`
- Password: `mysecretpassword`

## Direct PostgreSQL connection (Navicat)

If the database is accessible directly from your workstation (Postgres listening on the host interface and firewall allows it):

- Connection Type: PostgreSQL
- Host: `localhost` (or the DB server IP)
- Port: `5432`
- Database: `courseruniversty`
- Username: `abdalla`
- Password: `mysecretpassword`

Test connection using `psql`:

```bash
# requires psql client
PGPASSWORD="mysecretpassword" psql -h localhost -U abdalla -d courseruniversty -p 5432 -c '\l'
```

Check if Postgres is listening locally:

```bash
ss -ltnp | grep :5432
# or
sudo lsof -iTCP:5432 -sTCP:LISTEN -P -n
```

## SSH tunnel (Navicat SSH tunnel configuration)

If the DB server only listens on `localhost` of the remote machine (common for security), you can use an SSH tunnel.

In Navicat enable the SSH tunnel section and fill:

- SSH Host: <your remote host or IP>
- SSH Port: <usually 22>
- SSH User: <your ssh username>
- Authentication: Password or Private Key
- SSH Password / Key: <your ssh password or key path>

Then set the DB connection fields (from the remote server perspective):

- Host: `127.0.0.1`
- Port: `5432`
- Database: `courseruniversty`
- Username: `abdalla`
- Password: `mysecretpassword`

Manual SSH tunnel (CLI) example:

```bash
# Forward local port 5433 to remote's localhost:5432
ssh -L 5433:localhost:5432 -p <ssh_port> <ssh_user>@<ssh_host>
# then in a new terminal:
PGPASSWORD="mysecretpassword" psql -h localhost -U abdalla -d courseruniversty -p 5433 -c '\dt'
```

Replace `<ssh_host>`, `<ssh_port>`, and `<ssh_user>` with your remote server values.

## Use postgres user or different database

The project does NOT use the `postgres` superuser by default. If you need to use `postgres` database or user, create/set its password on the DB server.

Examples to run on the DB server (requires sudo or postgres user privileges):

```bash
# create DB (if missing)
sudo -u postgres createdb courseruniversty

# create user and set password
sudo -u postgres psql -c "CREATE USER abdalla WITH PASSWORD 'mysecretpassword';"

# grant access
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE courseruniversty TO abdalla;"

# or change postgres user's password
sudo -u postgres psql -c "ALTER USER postgres WITH PASSWORD 'new_postgres_password';"
```

## Security notes

- Do not expose Postgres directly to the internet without firewall and proper authentication.
- Prefer SSH key auth over password for SSH tunnels.
- Move credentials out of plaintext `settings.py` for production, use environment variables or a secrets manager.

## Troubleshooting

- "Connection refused" — check Postgres is running and listening on the expected address.
- "Peer authentication failed" — check pg_hba.conf for allowed auth types and addresses.
- If using SSH tunnel and connection times out, ensure SSH is reachable and the tunnel is established.

If you want, I can:

- Add a `requirements.txt` or quick `Makefile` to help test connections.
- Create a systemd service example for running the app on Linux bound to a chosen address/port.
- Generate step-by-step screenshots or a Navicat-specific guide if you tell me your Navicat version.

