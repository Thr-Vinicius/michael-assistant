# Michael Assistant

Michael é um assistente local para Arch Linux com Hyprland, focado em produtividade, automação simples e redução de atrito.

## Estado atual

Versão atual preservada: Michael 1.2.

## Objetivo

Evoluir para o Michael 2.0 com uma camada segura de interpretação por IA/Hermes, mantendo comandos reais atrás de um roteador validado.

## Princípios

- Estabilidade antes de inteligência.
- Nada de terminal livre para LLM.
- Comandos por voz passam por whitelist.
- Scripts silenciosos em stdout/stderr.
- Notificações e logs em vez de prints no terminal.
- Backup antes de alterações importantes.
- Sem processos duplicados.

## Componentes

- `voice/michael_voice.py`: captura e interpretação inicial de voz.
- `bin/`: comandos locais do Michael.
- `systemd/user/`: serviços systemd de usuário.
- `hypr/scripts/`: scripts integrados ao Hyprland.
- `config/`: configurações de exemplo.
- `docs/`: documentação do estado atual e planos.
