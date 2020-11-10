# Sistema de Preços

Implementação de um sistema de análise de preço que aponta qual o melhor local de compra dada uma certa região.

### Instalando Dependências

Clone esse repositório e execute:
```
pip3 install argparse haversine
```

### Uso

#### Servidor
```
python3 server.py [-h] [-p PORTA]
```
Informe a porta pela qual pretende-se comunicar com o cliente.

Exemplo:
```
python3 server.py -p 9999
```

#### Cliente
```
python3 client.py [-h] [-i HOST] [-p PORTA]
```

Informe o endereço IP e a porta do servidor que registrará e fará as buscas dos melhores locais para compra de combustível.

Exemplo:
```
python3 client.py -i 127.0.1.1 -p 9999
```

Todos os parâmetros, tanto do servidor quanto do cliente são opcionais.

**[GNU GPL v3.0](https://www.gnu.org/licenses/gpl-3.0.html)**
