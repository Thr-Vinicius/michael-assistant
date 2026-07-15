# Michael 2.0 Minimal Stable

## Estado

Michael 2.0 Minimal Stable é a versão congelada do Michael sem LLM/Hermes.

Objetivo: manter um assistente local simples, útil, seguro e de baixo atrito no Arch Linux com Hyprland.

## Arquitetura

Fluxo por voz:

voz / Ctrl+Ç
↓
michael_voice.py
↓
michael-voice-command
↓
michael-router
↓
ação permitida
↓
script local

Fluxo por terminal:

michael
↓
michael-router

## Comandos ativos

- Michael começar / Michael setup
- Michael mudar
- Michael status / Michael estado
- Michael check
- Michael logs
- Michael ouviu
- Michael ajuda
- Michael fone
- Michael resolver
- Michael desligar
- Michael conte uma piada
- Michael me motiva

## Comandos removidos

- Michael música
- Michael pausar
- Michael voltar
- Michael previsão do tempo
- Michael agenda
- Michael notícias
- Michael tarefas

## Fones

- Michael fone roda split-fones.sh
- Michael resolver roda resync-fones.sh
- Sink virtual usado: split_lr

## Welcome

O áudio e o script de boas-vindas na inicialização foram removidos da versão
atual. O Hyprland não executa mais `michael-welcome` durante o login.

O comportamento antigo permanece preservado em `legacy/michael-1.2/`.

## Sessão e modo game

- `michael-session-ready` prepara o ambiente gráfico e reinicia o serviço de voz
  depois que a sessão do Hyprland está pronta.
- `michael-zero-toggle` permite desligar e reativar temporariamente a escuta.
- `michael-desligar` executa a rotina personalizada usada pelo comando de
  desligamento.

## LLM/Hermes

LLM e Hermes ficam fora desta versão.

Motivo: evitar complexidade, consumo, manutenção e distração antes dos cursos.

## Próxima fase futura

Depois dos cursos, avaliar uma camada opcional de LLM como fallback de intenção.

A LLM nunca deve executar terminal livremente.
