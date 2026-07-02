# Estado do Michael 1.2

## Sistema

- Arch Linux
- Hyprland
- Assistente local por voz

## Serviço principal

- `michael-voice.service`
- Executa: `/home/arthur/michael_voice.py`

## Serviços antigos

- `jarvis-wakeword.service`: inativo/desabilitado
- `michael-clap.service`: inativo/desabilitado

## Comportamento atual

- Palmas removidas.
- Confirmação "correto" removida.
- "Michael começar" abre o setup direto.
- Michael não fala ao chamar setup.
- Michael fala apenas ao iniciar o PC via `michael-welcome`.
- `Ctrl+Ç` ativa escuta por alguns segundos via `michael-ativar`.
- Comandos sem wake/origem confiável são bloqueados.
- Perguntas como "Michael como mudar" são ignoradas para evitar ação acidental.
- Uso de `flock` para evitar processos duplicados.
- `Michael estado` também chama status, pois o Vosk costuma entender "status" como "estado".

## Comandos existentes

- `Michael começar` / `Michael setup`
- `Michael música`
- `Michael mudar`
- `Michael status` / `Michael estado`
- `Michael check`
- `Michael logs`
- `Michael pausar`
- `Michael voltar`
- `Michael fone`
- `Michael resolver`
- `Ctrl+Ç`

## Preferências

- Scripts chamados por voz devem ser silenciosos.
- Usar notificações e logs.
- Sempre fazer backup antes de alterar scripts importantes.
- Não criar processos duplicados.
- LLM/Hermes não pode executar terminal livremente.
