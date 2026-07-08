# Michael Assistant

Michael é um assistente local para Arch Linux com Hyprland, focado em produtividade, automação simples e redução de atrito.

## Versão atual

Michael 2.0 Minimal Stable.

## Objetivo

Manter um assistente local pequeno, seguro, útil e sem LLM por enquanto.

## Princípios

- Estabilidade antes de inteligência.
- Sem LLM/Hermes nesta versão.
- Nada de terminal livre para IA.
- Comandos passam por router seguro.
- Scripts chamados por voz devem ser silenciosos.
- Notificações e logs em vez de prints quando chamado por voz.
- Sem processos duplicados.
- Baixo consumo e baixa manutenção.

## Componentes

- voice/michael_voice.py: escuta de voz.
- bin/michael-voice-command: ponte entre voz e router.
- bin/michael-router: roteador seguro.
- bin/michael: modo terminal.
- bin/michael-check: diagnóstico.
- bin/michael-ouviu: histórico do que foi reconhecido.
- hypr/scripts/: integração com Hyprland.
- systemd/user/: serviço systemd de usuário.
- docs/: documentação.
