# 🛡️ AutoGuard — Watchdog de Serviços com Auto-Recuperação

AutoGuard é um watchdog leve em Python que monitora serviços críticos (via **systemd** ou **Docker**), detecta falhas e **reinicia automaticamente**, enviando notificações em tempo real para o Discord.

## 🎯 Problema que resolve

Em ambientes de infraestrutura, um serviço parado às 3h da manhã pode gerar horas de indisponibilidade até alguém notar. O AutoGuard elimina esse tempo de reação: ele detecta a queda em segundos e já tenta reiniciar o serviço, te avisando imediatamente.

## ⚙️ Arquitetura

```mermaid
flowchart LR
    A[AutoGuard Loop] -->|verifica| B(Serviço systemd)
    A -->|verifica| C(Container Docker)
    B -- caiu --> D[Restart systemctl]
    C -- caiu --> E[Restart docker]
    D --> F[Notificação Discord]
    E --> F
    A --> G[Log rotativo em arquivo] 
    git clone https://github.com/Luisninja2/ll.git
cd ll
pip install -r requirements.txt
cp config.example.yaml config.yaml
# edite config.yaml com seus serviços

export AUTOGUARD_WEBHOOK_URL="https://discord.com/api/webhooks/..."
python3 autoguard.py -c config.yaml
sudo cp systemd/autoguard.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now autoguard

---

#### 2️⃣ Nome do arquivo: `autoguard.py`

```python
#!/usr/bin/env python3
"""
AutoGuard - Watchdog de Serviços com Auto-Recuperação
Monitora serviços (systemd ou Docker), reinicia se caírem
e envia notificações via webhook (Discord).
"""

import subprocess
import time
import logging
import argparse
import os
import sys
from logging.handlers import RotatingFileHandler

try:
    import yaml
    import requests
except ImportError:
    print("Dependências faltando. Rode: pip install -r requirements.txt")
    sys.exit(1)


def setup_logging(log_file="autoguard.log"):
    logger = logging.getLogger("autoguard")
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(message)s", "%Y-%m-%d %H:%M:%S"
    )

    file_handler = RotatingFileHandler(log_file, maxBytes=1_000_000, backupCount=3)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    return logger


def load_config(path):
    with open(path, "r") as f:
        return yaml.safe_load(f)


def check_systemd(unit):
    result = subprocess.run(
        ["systemctl", "is-active", unit], capture_output=True, text=True
    )
    return result.stdout.strip() == "active"


def restart_systemd(unit):
    subprocess.run(["systemctl", "restart", unit], check=False)


def check_docker(container_name):
    result = subprocess.run(
        ["docker", "inspect", "-f", "{{.State.Running}}", container_name],
        capture_output=True,
        text=True,
    )
    return result.stdout.strip() == "true"


def restart_docker(container_name):
    subprocess.run(["docker", "start", container_name], check=False)


def send_discord_notification(webhook_url, message):
    if not webhook_url:
        return
    try:
        requests.post(webhook_url, json={"content": message}, timeout=5)
    except requests.RequestException as e:
        logging.getLogger("autoguard").warning(f"Falha ao notificar Discord: {e}")


def monitor(config):
    logger = setup_logging(config.get("log_file", "autoguard.log"))
    interval = config.get("check_interval", 30)

    webhook_url = os.environ.get(
        "AUTOGUARD_WEBHOOK_URL", config.get("notifications", {}).get("discord_webhook_url")
    )

    services = config.get("services", [])
    logger.info(f"AutoGuard iniciado. Monitorando {len(services)} serviço(s).")

    while True:
        for service in services:
            name = service.get("name")
            svc_type = service.get("type")

            try:
                if svc_type == "systemd":
                    unit = service.get("unit")
                    is_up = check_systemd(unit)
                elif svc_type == "docker":
                    container = service.get("container_name")
                    is_up = check_docker(container)
                else:
                    logger.warning(f"Tipo desconhecido para '{name}': {svc_type}")
                    continue

                if is_up:
                    logger.info(f"[OK] {name} está saudável.")
                else:
                    logger.error(f"[DOWN] {name} está fora do ar. Tentando reiniciar...")
                    if svc_type == "systemd":
                        restart_systemd(service.get("unit"))
                    else:
                        restart_docker(service.get("container_name"))

                    send_discord_notification(
                        webhook_url,
                        f"🚨 **AutoGuard**: `{name}` caiu e foi reiniciado automaticamente.",
                    )

            except Exception as e:
                logger.exception(f"Erro ao verificar '{name}': {e}")

        time.sleep(interval)


def main():
    parser = argparse.ArgumentParser(description="AutoGuard - Watchdog de Serviços")
    parser.add_argument(
        "-c", "--config", default="config.yaml", help="Caminho do arquivo de configuração"
    )
    args = parser.parse_args()

    if not os.path.exists(args.config):
        print(f"Arquivo de configuração não encontrado: {args.config}")
        print("Copie config.example.yaml para config.yaml e ajuste.")
        sys.exit(1)

    config = load_config(args.config)
    monitor(config)


if __name__ == "__main__":
    main()
    check_interval: 30
log_file: autoguard.log

notifications:
  discord_webhook_url: ""

services:
  - name: nginx
    type: systemd
    unit: nginx.service

  - name: meu-container
    type: docker
    container_name: meu-container
check_interval: 30
log_file: autoguard.log

notifications:
  discord_webhook_url: ""

services:
  - name: nginx
    type: systemd
    unit: nginx.service

  - name: meu-container
    type: docker
    container_name: meu-container
pyyaml==6.0.2
requests==2.32.3
__pycache__/
*.pyc
venv/
.env
config.yaml
*.log
MIT License

Copyright (c) 2026 Luisninja2

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
[Unit]
Description=AutoGuard - Watchdog de Serviços
After=network.target

[Service]
Type=simple
WorkingDirectory=/opt/autoguard
ExecStart=/usr/bin/python3 /opt/autoguard/autoguard.py -c /opt/autoguard/config.yaml
Environment=AUTOGUARD_WEBHOOK_URL=coloque_sua_url_aqui
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
