# Michael Assistant

Michael é um assistente local para Arch Linux com Hyprland, focado em produtividade, automação simples e redução de atrito.

## Versão atual

Michael 2.0 Minimal Stable.

As versões anteriores permanecem preservadas em `legacy/`. Recursos que podem
ser avaliados no futuro ficam separados em `future/`.

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
- bin/michael-desligar: rotina controlada de desligamento.
- bin/michael-session-ready: prepara a sessão gráfica para o serviço de voz.
- bin/michael-welcome: reproduz o som curto de inicialização.
- bin/michael-zero-toggle: liga ou desliga temporariamente a escuta.
- bin/michael-ultimos: mostra um resumo curto dos logs.
- hypr/scripts/: integração com Hyprland.
- systemd/user/: serviço systemd de usuário.
- docs/: documentação.

A integração necessária com o Hyprland está descrita em
`docs/integracao-hyprland.md`.

## Organização das versões

- `bin/`, `voice/`, `hypr/`, `systemd/` e `config/`: Michael 2.0 atual.
- `legacy/michael-1.1/`: arquivos preservados do Michael 1.1.
- `legacy/michael-1.2/`: fotografia preservada do Michael 1.2.
- `future/`: ideias fora da versão atual, sem execução automática.

## Integração com os fones Bluetooth

O gerenciamento dos dois fones foi transferido para o projeto
[linux-bluetooth-split-stereo](https://github.com/Thr-Vinicius/linux-bluetooth-split-stereo).

O watchdog configura as saídas automaticamente. O comando `Michael fone` foi
desativado, enquanto `Michael resolver` permanece disponível para solicitar uma
ressincronização. Consulte [docs/integracao-fones.md](docs/integracao-fones.md).
