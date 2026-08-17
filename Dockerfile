FROM python:3.12-slim

# System dependencies
RUN apt-get update && apt-get install -y \
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
