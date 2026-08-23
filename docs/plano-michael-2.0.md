\# Plano do Michael 2.0

\#\# Objetivo

Evoluir o Michael 1.2 para uma versão minimalista com interpretação mais natural, personalidade curta e uso controlado de LLM, sem perder estabilidade, segurança e baixo consumo.

\#\# Princípios

- Preservar o Michael 1.2 funcionando.

- Não transformar o projeto em uma Alexa gigante.

- Priorizar produtividade real.

- Evitar comandos inúteis.

- Usar LLM apenas quando fizer sentido.

- Não desperdiçar requisições.

- Não permitir que LLM execute terminal livremente.

- Toda ação real deve passar por um roteador seguro.

- Scripts chamados por voz devem ser silenciosos em stdout/stderr.

- Usar notificações e logs.

- Evitar processos duplicados.

\#\# Arquitetura desejada

Fluxo básico:

\`\`\`text  
voz ou Ctrl+Ç  
↓  
michael\_voice.py  
↓  
michael-voice-command  
↓  
michael-router  
↓  
parser local  
↓  
LLM, somente se necessário  
↓  
JSON validado  
↓  
ação permitida  
↓  
script local

---  
  
\#\# 2. Decisões do Michael 2.0  
  
\`\`\`bash  
cat \> docs/decisoes-michael-2.0.md \<\<'EOF'  
\# Decisões do Michael 2.0  
  
\#\# Decisões aprovadas  
  
\#\#\# Michael minimalista  
  
O Michael 2.0 deve ser pequeno, rápido e útil.  
  
O foco é produtividade, não quantidade de comandos.  
  
\#\#\# LLM com uso controlado  
  
A LLM não será chamada para comandos óbvios.  
  
Exemplos que não precisam de LLM:  
  
- Michael status  
- Michael estado  
- Michael check  
- Michael logs  
- Michael pausar  
- Michael voltar  
- Michael fone  
- Michael resolver  
  
\#\#\# LLM como fallback  
  
A LLM poderá interpretar frases naturais quando o parser local não entender com segurança.  
  
Exemplos:  
  
- organiza minha bagunça  
- meus fones estão bugados  
- como você está?  
- me motiva  
- conte uma piada  
  
\#\#\# Remover música do Michael 2.0  
  
O comando "Michael música" não será mantido como ação ativa no Michael 2.0, pois não está sendo usado.  
  
O script antigo pode permanecer no repositório como histórico, mas não deve entrar na whitelist inicial do router.  
  
\#\#\# Sem previsão do tempo  
  
Comando de previsão do tempo foi descartado por não trazer ganho real de produtividade.  
  
\#\#\# Sem agenda  
  
Comando de agenda foi descartado por não trazer ganho real no momento.  
  
\#\#\# Sem Standard Notes agora  
  
Integração com Standard Notes foi descartada da fase inicial porque exigiria sincronização, gerenciamento e manutenção demais.  
  
\#\#\# Hermes depois  
  
Hermes poderá ser testado no futuro, principalmente para tarefas dentro de sites.  
  
Por enquanto, não deve ser parte do núcleo do Michael 2.0.  
  
\#\# Limites de segurança  
  
A LLM nunca deve retornar comandos de terminal.  
  
A LLM deve retornar intenção estruturada, preferencialmente JSON.  
  
O router seguro decide se a ação é permitida.  
  
Se houver dúvida, o Michael não executa nada.
