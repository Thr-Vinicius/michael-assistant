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

O áudio de boas-vindas ao ligar o PC foi desativado.

Arquivo antigo de áudio removido do uso:

/home/arthur/audios-michael/boas_vindas_senhor_pronto_para_mais_um_dia.mp3

## LLM/Hermes

LLM e Hermes ficam fora desta versão.

Motivo: evitar complexidade, consumo, manutenção e distração antes dos cursos.

## Próxima fase futura

Depois dos cursos, avaliar uma camada opcional de LLM como fallback de intenção.

A LLM nunca deve executar terminal livremente.
