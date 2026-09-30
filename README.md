## 🛡️ AutoGuard — Watchdog de Serviços com Auto-Recuperação

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

3. Clique no botão verde **"Commit changes..."** lá no canto superior direito (no seu print dá pra ver ele verdinho ali).

Depois disso, o seu repositório já vai ficar com a documentação bonitona na página principal! Me avisa quando clicar em commit!
