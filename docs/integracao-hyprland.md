# Integração com o Hyprland

O Michael 2.0 usa integrações diretas com o Hyprland por meio do provider Lua.

## Som de inicialização

Executar uma vez durante o login:

    hl.exec_cmd("/home/arthur/.local/bin/michael-welcome")

O script reproduz somente o áudio curto de inicialização. A antiga mensagem
longa de boas-vindas permanece desativada.

## Preparar a sessão gráfica

Executar uma vez durante o login:

    hl.exec_cmd("/home/arthur/.local/bin/michael-session-ready")

O script espera a sessão gráfica estabilizar, importa as variáveis do Wayland e
reinicia `michael-voice.service`.

## Modo game

O atalho atual chama:

    /home/arthur/.local/bin/michael-zero-toggle

Quando o modo game é ativado:

- `michael-voice.service` é interrompido;
- o Caelestia Shell é encerrado;
- o Overview do Quickshell é encerrado.

Quando o modo game é desativado, os três componentes são reativados.

O estado é informado por notificação e registrado nos logs do Michael.

## Gerenciamento dos fones

O gerenciamento dos dois fones Bluetooth pertence ao projeto
`linux-bluetooth-split-stereo` e funciona independentemente do Michael.

O Hyprland não executa mais scripts antigos de roteamento dos fones.

## Atalho para ressincronizar os fones

A ressincronização manual chama diretamente:

    ~/.local/bin/resync-fones.sh

O atalho atual no Hyprland é:

    SUPER + SHIFT + R

Assim, a ressincronização dos fones não depende do Michael e continua
disponível mesmo quando o modo game está ativo.
