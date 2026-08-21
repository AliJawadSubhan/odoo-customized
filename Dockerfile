FROM python:3.12-slim

# System dependencies + wkhtmltopdf (patched Qt build required by Odoo for PDF headers/footers)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    libxml2-dev \
    libxslt1-dev \
    libldap2-dev \
    libsasl2-dev \
    libssl-dev \
    libjpeg-dev \
    libfreetype6-dev \
    zlib1g-dev \
    npm \
    ca-certificates \
    curl \
    && curl -fsSL https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6.1-3/wkhtmltox_0.12.6.1-3.bookworm_amd64.deb \
         -o /tmp/wkhtmltox.deb \
    && apt-get install -y --no-install-recommends /tmp/wkhtmltox.deb \
    && rm /tmp/wkhtmltox.deb \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /odoo

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir psycopg2-binary && \
    grep -v 'rl-renderPM\|psycopg2==' requirements.txt > /tmp/req_filtered.txt && \
    pip install --no-cache-dir -r /tmp/req_filtered.txt

# Copy source
COPY . .

RUN chmod +x docker-entrypoint.sh && \
    useradd -m odoo && \
    chown -R odoo:odoo /odoo

USER odoo

EXPOSE 8069

CMD ["./docker-entrypoint.sh"]
