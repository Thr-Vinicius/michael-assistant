# Integração histórica dos fones

Estes arquivos pertencem à antiga implementação em que o Michael controlava
diretamente os dois fones Bluetooth.

Arquivos preservados:

- `michael-fone`: interface antiga do comando `Michael fone`;
- `split-fones.sh`: criação manual da saída estéreo dividida;
- `resync-fones.sh`: ressincronização executada diretamente pelo Michael.

Essa implementação foi substituída pelo projeto independente
[linux-bluetooth-split-stereo](https://github.com/Thr-Vinicius/linux-bluetooth-split-stereo),
que utiliza o serviço persistente `fones-watchdog.service`.

Os arquivos deste diretório são históricos e não devem ser instalados como a
implementação atual.
