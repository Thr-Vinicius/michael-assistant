# Integração com o Hyprland

O Michael 2.0 usa três integrações diretas no `hyprland.conf`.

## Som de inicialização

Executar uma vez durante o login:

    exec-once = /home/arthur/.local/bin/michael-welcome

O script reproduz somente o áudio curto `inic.mp3` em 70%. A antiga mensagem
longa de boas-vindas permanece desativada.

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

## Gerenciamento dos fones

O Hyprland não executa mais `auto-split-fones.sh`. O gerenciamento atual é
automático pelo projeto `linux-bluetooth-split-stereo` e seu watchdog.

## Atalho para ressincronizar os fones

Quando o sistema de áudio dividido estiver instalado, o comando
`michael-resolver` pode ser associado a um atalho do Hyprland.

Exemplo com `Ctrl + Super + F`:

```ini
bind = CTRL SUPER, F, exec, ~/.local/bin/michael-resolver
```

Recarregue a configuração:

```bash
hyprctl reload
```

O atalho funciona sem reconhecimento de voz e também pode ser usado quando
o modo jogo estiver ativo.

O comando verifica se os dois fones estão conectados antes de solicitar a
ressincronização. Quando eles não estão disponíveis, nenhum pedido fica
pendente no watchdog.
