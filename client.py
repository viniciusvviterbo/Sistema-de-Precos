import socket
import argparse

# Configuracao dos argumentos
parser = argparse.ArgumentParser(description = 'Simples implementação do jogo Batalha Naval.')
parser.add_argument('-i', action = 'store', dest = 'host', default = '127.0.1.1', required = False, help = 'Endereço IP do servidor.')
parser.add_argument('-p', action = 'store', dest = 'porta', default = 9999, required = False, help = 'Porta a ser usada pelo servidor.')

def main():
    # Recebe os argumentos. Se as variaveis nao forem passadas, retorna -h
    arguments = parser.parse_args()
    # Instancia o socket UDP
    soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Armazena o nome do host, seu endereço IP e a porta
    host = arguments.host
    porta = int(arguments.porta)
    buffer_size = 1024
    
    print('Inicializando o programa...')
    print('Programa inicializado\n')

    while True:
        tipo_mensagem = input('\nInforme o tipo de mensagem a ser enviada\n' + \
        'D - Dados\n' + \
        'P - Pesquisa\n' + \
        '[D/P]: ')

        if tipo_mensagem == 'D':
            id_mensagem = input('\nInforme o número identificador da mensagem a ser enviada: ')
            tipo_combustvel = input('\nTipos de combustível\n' + \
            '0 - diesel\n' + \
            '1 - álcool\n' + \
            '2 - gasolina\n' + \
            '[0/1/2]: ')
            preco_combustivel = str(int(input('\nInforme o preço do combustível: ')) * 1000)
            latitude = input('\nInforme a latitude do posto de combustível: ')
            longitude = input('\nInforme a longitude do posto de combustível: ')

            mensagem_envio = \
                tipo_mensagem + '&' + \
                id_mensagem + '&' + \
                tipo_combustvel + '&' + \
                preco_combustivel + '&' + \
                latitude + '&' + \
                longitude

        elif tipo_mensagem == 'P':
            id_mensagem = input('\nInforme o número identificador da mensagem a ser enviada: ')
            tipo_combustvel = input('\nTipos de combustível\n' + \
            '0 - diesel\n' + \
            '1 - álcool\n' + \
            '2 - gasolina\n' + \
            '[0/1/2]: ')
            raio_busca = input('Informe o raio de busca: ')
            latitude = input('\nInforme a latitude do centro de busca: ')
            longitude = input('\nInforme a longitude do centro de busca: ')

            mensagem_envio = \
                tipo_mensagem + '&' + \
                id_mensagem + '&' + \
                tipo_combustvel + '&' + \
                raio_busca + '&' + \
                latitude + '&' + \
                longitude 

        elif tipo_mensagem == '[sair]':
            print('Encerrando execução')
            break

        else:
            print('Opção não suportada')
            continue

        # Envia a mensagem construída com as opções selecionados pelo usuário
        soc.sendto(str.encode(mensagem_envio), (host, porta))
        # Recebe a confirmação de que a mensagem foi recebida pelo destinatário
        mensagem_recebida = soc.recvfrom(buffer_size)

        # Recebe e exibe o resultado da requisição enviada
        resultado = soc.recvfrom(buffer_size)
        print(resultado.decode())

# Chama a função main
if __name__ == '__main__':
    main()