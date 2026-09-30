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
