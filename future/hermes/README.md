
# Hermes - Experimentos Futuros



Esta pasta é reservada para testes futuros com Hermes/LLM.



## Objetivo futuro



Testar Hermes como camada experimental para interpretação avançada e possíveis tarefas em sites.



## Limites



Hermes não deve:



- executar terminal livremente;

- confirmar ações sensíveis sozinho;

- alterar dados importantes sem confirmação;

- baixar ou executar arquivos;

- substituir o router seguro do Michael.



## Ideia de uso



Hermes pode interpretar intenção e retornar JSON estruturado.



Exemplo:



```json

{

  "action": "setup",

  "confidence": 0.87,

  "reply": "Bora trabalhar."

}

