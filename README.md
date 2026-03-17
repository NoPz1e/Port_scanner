# Port_scanner

## Descrição

Este script python utiliza socket, para tentar portas requisitadas de um host para saber se elas estão abertas, fechadas ou filtradas. 

## Requisitos

- Python 3.x instalado

## Como usar!

Depois de instalar o scrit no seu computador, no terminal navegar até ao diretorio do script.

### Argumentos

#### Target '-t' '--target'
Passar o ip ou dominio alvo para o script, é obrigatorio para funcionar.

#### Port '-p' '--port'
Passar as porta alvo para o script.
- 443
- 22,80,443
- 1-1024
##### Default ports
'443, 80, 53, 22, 25, 8080, 445, 143, 3389, 21'

#### Thread '-th' '--thread'
Passar o número de thread, que vai influnciar a velocidade do script

##### Default thread
30

### Exemplos de comandos:

`python3 scanner.py -t 0.0.0.0 -p 34`

`python3 scanner.py -t 0.0.0.0 --port 22,44 -th 100`

`python3 scanner.py -t google.com -p 1-500` 

`python3 scanner.py --target 0.0.0.0 --thread 50`


### Output esperado

```
Scannig google.com ..........
-> 22 FILTERED
-> 80 OPEN
-> 443 OPEN
```