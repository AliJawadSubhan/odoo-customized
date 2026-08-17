#!/bin/bash
set -e

exec python odoo-bin \
    --db_host "${PGHOST}" \
    --db_port "${PGPORT:-5432}" \
    --db_user "${PGUSER}" \
    --db_password "${PGPASSWORD}" \
    --db_name "${PGDATABASE:-odoo}" \
    --http-port "${PORT:-8069}" \
    --proxy-mode \
    --addons-path "addons" \
    --without-demo all \
    --logfile ""
