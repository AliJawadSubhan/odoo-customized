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
proxy_mode = True
EOF

exec python odoo-bin -c /tmp/odoo.conf \
    -u markition_branding \
    --http-port "${PORT:-8069}" \
    --proxy-mode \
    --without-demo all