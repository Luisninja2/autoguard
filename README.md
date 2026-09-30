🛡️ AutoGuard — Watchdog de Serviços com Auto-Recuperação
AutoGuard é um watchdog leve em Python que monitora serviços críticos (via systemd ou Docker), detecta falhas e reinicia automaticamente, enviando notificações em tempo real para o Discord.

🎯 Problema que resolve
Em ambientes de infraestrutura, um serviço parado às 3h da manhã pode gerar horas de indisponibilidade até alguém notar. O AutoGuard elimina esse tempo de reação: ele detecta a queda em segundos e já tenta reiniciar o serviço, te avisando imediatamente.

⚙️ Arquitetura
+------------------+         +-------------------+
|  AutoGuard Loop  | ------> |  Serviço systemd  |
+------------------+         +-------------------+
         |                             | (caiu)
         |                             v
         |                   [ Restart systemctl ]
         |                             |
         v                             v
+------------------+         +-------------------+
| Container Docker | ------> |  Alerta Discord   |
+------------------+         +-------------------+
✨ Funcionalidades
Monitoramento de múltiplos serviços (systemd e Docker) em um só processo.
Auto-restart em caso de falha.
Log rotativo em arquivo (autoguard.log).
Notificação via webhook do Discord.
Configuração via YAML, sem hardcode de credenciais.
Pronto para rodar como serviço systemd (24/7).
🧰 Requisitos
Python 3.9+
pip install -r requirements.txt
Permissão para executar systemctl e/ou docker
🚀 Como usar
git clone https://github.com/Luisninja2/ll.git
cd ll
pip install -r requirements.txt
cp config.example.yaml config.yaml
export AUTOGUARD_WEBHOOK_URL="https://discord.com/api/webhooks/..."
python3 autoguard.py -c config.yaml

🔒 Segurança
O webhook do Discord nunca deve ser commitado no repositório. Use a variável de ambiente AUTOGUARD_WEBHOOK_URL.

🖥️ Rodando como serviço permanente (systemd)
sudo cp systemd/autoguard.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now autoguard
