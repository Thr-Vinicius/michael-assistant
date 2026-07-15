# Integração com o Hyprland

O Michael 2.0 usa duas integrações diretas no `hyprland.conf`.

## Preparar a sessão gráfica

Executar uma vez durante o login:

```ini
exec-once = /home/arthur/.local/bin/michael-session-ready
```

O script espera a sessão gráfica estabilizar, importa as variáveis do Wayland e
reinicia `michael-voice.service`.

## Modo game

Atalho para desligar ou reativar temporariamente a escuta:

```ini
bind = SUPER CTRL, M, exec, /home/arthur/.local/bin/michael-zero-toggle
```

O estado é informado por notificação e registrado em
`~/.local/state/michael/zero.log`.

## Comportamentos removidos

O Michael 2.0 não executa automaticamente `michael-welcome` nem
`auto-split-fones.sh`. O gerenciamento atual é automático pelo projeto `linux-bluetooth-split-stereo` e seu watchdog.
