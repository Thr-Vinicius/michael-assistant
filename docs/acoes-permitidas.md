
# Ações Permitidas do Michael 2.0



Esta lista define as ações que poderão ser reconhecidas pelo Michael 2.0.



A LLM não executa comandos diretamente. Ela apenas sugere uma ação desta lista.



## Ações principais



| Ação | Função |

|---|---|

| setup | Abrir o ambiente de trabalho |

| mudar | Reorganizar janelas/setup |

| status | Mostrar estado do Michael |

| check | Rodar diagnóstico rápido |

| logs | Mostrar logs recentes |

| pausar | Pausar escuta do Michael |

| voltar | Reativar escuta do Michael |

| fone | Conectar/sincronizar fones |

| resolver | Ressincronizar fones |

| ajuda | Mostrar ajuda |



## Ações de interação leve



| Ação | Função |

|---|---|

| piada | Contar uma piada curta |

| motivar | Dar uma frase curta de incentivo |

| conversa | Responder conversa curta |

| none | Não executar nada |



## Ações removidas ou fora do escopo



| Ação | Motivo |

|---|---|

| musica | Não está sendo usada |

| agenda | Fora do foco inicial |

| previsao_tempo | Baixo ganho prático |

| noticias | Pode desperdiçar requisições |

| tarefas | Integração ainda indefinida |

| standard_notes | Complexidade alta para a fase inicial |

| obsidian | Não faz parte do fluxo atual |

| navegador_livre | Risco alto |

| terminal_livre | Proibido |



## Exemplo de JSON esperado



```json

{

  "action": "resolver",

  "confidence": 0.91,

  "reply": "Vou tentar resolver os fones."

}



---



## 4. README do legado Michael 1.1



```bash

cat > legacy/michael-1.1/README.md <<'EOF'

# Michael 1.0/1.1 - Legado



Esta pasta preserva arquivos antigos do Michael apenas para referência histórica.



Estes arquivos não fazem parte do Michael 1.2 atual nem do Michael 2.0.



## Atenção



A versão 1.0/1.1 possuía comportamentos que foram removidos ou abandonados:



- detecção por palmas;

- wakeword antigo;

- confirmação "correto";

- scripts antigos de setup;

- comportamentos menos seguros.



Não usar estes arquivos em produção sem revisar.

