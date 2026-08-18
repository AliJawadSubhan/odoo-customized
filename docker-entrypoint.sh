#!/bin/bash
set -e

# Generate odoo.conf dynamically with the master password
cat > /tmp/odoo.conf <<EOF
[options]
admin_passwd = ${ADMIN_PASSWD}
db_host = ${PGHOST}
db_port = ${PGPORT:-5432}
db_user = ${PGUSER}
db_password = ${PGPASSWORD}
addons_path = addons
list_db = True
EOF

# Initialize base module on first boot (idempotent — safe to run every start)
python odoo-bin -c /tmp/odoo.conf \
    -d odoo -i base \
    --stop-after-init \
    --without-demo all

exec python odoo-bin -c /tmp/odoo.conf \
    -d odoo \
    --http-port "${PORT:-8069}" \
    --proxy-mode \
    --without-demo all