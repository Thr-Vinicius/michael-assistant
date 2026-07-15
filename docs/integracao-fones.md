# Integração com os fones Bluetooth

O gerenciamento dos dois fones Bluetooth não pertence mais diretamente ao
Michael. A implementação atual é mantida no projeto independente
[linux-bluetooth-split-stereo](https://github.com/Thr-Vinicius/linux-bluetooth-split-stereo).

## Funcionamento atual

O serviço `fones-watchdog.service` roda em segundo plano e monitora a conexão
dos fones. Quando os dois dispositivos estão disponíveis, ele cria
automaticamente a saída estéreo dividida `split_lr`.

Também seleciona uma saída adequada quando apenas um fone está conectado e
restaura a saída normal do computador quando nenhum deles está disponível.

Por isso, o antigo comando `Michael fone` foi desativado: seu trabalho passou
a ser executado automaticamente pelo watchdog.

## Ressincronização pelo Michael

O comando `Michael resolver` continua disponível.

Ele não controla diretamente o Bluetooth nem executa uma segunda instância dos
scripts. Em vez disso, cria uma solicitação para o watchdog, que realiza a
ressincronização de forma coordenada.

Essa integração requer:

- `~/.local/bin/split-fones.sh`
- `~/.local/bin/resync-fones.sh`
- `~/.local/bin/fones-watchdog.sh`
- `~/.config/linux-bluetooth-split-stereo/config`
- `fones-watchdog.service`

A ausência dessa integração não impede o funcionamento das demais funções do
Michael.

## Variações de sincronização

Pequenas diferenças de atraso podem ocorrer porque são usados dois dispositivos
Bluetooth independentes, cada um com seu próprio buffer e relógio de áudio.

Quando a diferença se torna perceptível, o comando `Michael resolver` pode ser
usado para solicitar uma nova sincronização. Nem toda execução produzirá
exatamente o mesmo alinhamento, embora o áudio normalmente permaneça utilizável.

## Histórico

As antigas implementações mantidas diretamente pelo Michael estão preservadas
em `legacy/integracao-fones/`. Elas existem apenas como registro histórico e não
representam a instalação atual.
