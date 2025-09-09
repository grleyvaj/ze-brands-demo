#!/usr/bin/env python3
import os
import re
import sys
import time

import psycopg2

dsn = os.environ.get("DATABASE_URL")
if not dsn:
    sys.exit(1)

# Normalize DSN for psycopg2 (remove driver prefix if present)
conn_str = dsn.replace("postgresql+psycopg2://", "postgresql://")

m = re.match(
    r"postgresql://(?P<user>[^:]+):(?P<pw>[^@]+)"
    r"@(?P<host>[^:/]+)(:(?P<port>\d+))?/(?P<db>.+)",
    conn_str,
)

if m:
    params = m.groupdict()
    host = params.get("host")
    port = params.get("port") or "5432"
    user = params.get("user")
    pw = params.get("pw")
    db = params.get("db")
else:
    # fallback: try to connect using the whole connection string
    host = None

attempt = 0
while True:
    try:
        if host:
            conn = psycopg2.connect(
                host=host,
                port=port,
                user=user,
                password=pw,
                dbname=db,
            )
        else:
            conn = psycopg2.connect(conn_str)
        conn.close()
        break
    except Exception:
        attempt += 1
        time.sleep(1)
