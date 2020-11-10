#import socketserver
import socket
import argparse
import sys
import haversine as hs

# Configuracao dos argumentos
parser = argparse.ArgumentParser(description = 'Simples implementação do jogo Batalha Naval.')
parser.add_argument('-p', action = 'store', dest = 'porta', default = 9999, required = False, help = 'Porta a ser usada pelo servidor.')

def calc_geodistancia(origem, destino):
    return hs.haversine(origem,destino)

def filtra_combustivel(matrix_registros, tipo_combustivel):
    nova_matrix = []
    for linha in matrix_registros:
        if linha[0] == tipo_combustivel:
            nova_matrix.append(linha)
    return nova_matrix

def filtra_localizacao(matrix_registros, raio, latitude, longitude):
    nova_matrix = []
    origem = (latitude, longitude)
    for linha in matrix_registros:
        destino = (linha[2], linha[3])
        distancia = calc_geodistancia(origem, destino)
        if distancia <= raio:
            nova_matrix.append(linha)
    return nova_matrix

def get_melhor_preco(matrix_registros):
    menor_preco = sys.maxsize
    melhor_posto = None
    for linha in matrix_registros:
        if linha[1] < menor_preco:
            melhor_posto = linha
    return melhor_posto

def main():
    # Recebe os argumentos. Se as variaveis nao forem passadas, retorna -h
    arguments = parser.parse_args()
    print('Inicializando servidor...')
    # Instancia o socket
    soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Abre o arquivo de registro
    try:
        arquivo_registro = open('sistema_precos_registro.txt', 'x')
        arquivo_registro = open('sistema_precos_registro.txt', 'r+')
        arquivo_registro.write('tipo_combustivel & preco_combustivel & latitude & longitude')
    except IOError:
        arquivo_registro = open('sistema_precos_registro.txt', 'r+')
    # Armazena o nome do host, seu endereço IP e a porta
    host = socket.gethostname()
    ip = socket.gethostbyname(host)
    porta = int(arguments.porta)
    buffer_size = 1024
    mensagem_conclusao = ''
    # Configura o socket à porta e o nome do host
    soc.bind((host, porta))
    print(host, '({})'.format(ip))
    # Espera por uma mensagem de um client
    print('Esperando mensagens do client...')

    while True:
        # Recebe mensagem do client
        mensagem_recebida = soc.recvfrom(buffer_size)
        mensagem_conteudo = mensagem_recebida[0].decode() 
        endereco_client = mensagem_recebida[1]
        print('Mensagem do cliente: {}\nEndereço do cliente: {}\n'.format(mensagem_conteudo, endereco_client))
        # Confirma recebimento da mensagem
        mensagem_confirmacao = str.encode('Mensagem recebida')
        soc.sendto(mensagem_confirmacao, endereco_client)
        # Separa o conteúdo da mensagem em um array
        dados_arr = mensagem_conteudo.split('&')

        if dados_arr[0] == 'D':
            # Registra os dados recebidos
            arquivo_registro.write('&'.join(dados_arr[2:] + '\n')
            # Envia uma mensagem que confirma a conclusão do registro dos dados recebidos
            mensagem_conclusao = str.encode('Dados cadastrados com sucesso')
        
        else:
            # Instancia a matrix_registros para ler os dados mais facilmente
            matrix_registros = []
            for linha in arquivo_registro.read().split('\n'):
                matrix_registros.append(linha.split('&'))

            # Filtra as opções disponíveis pelo tipo de combustível
            matrix_registros = filtra_combustivel(matrix_registros, dados_arr[2])
            # Filtra as opções  disponíveis pela distância máxima da origem
            matrix_registros = filtra_localizacao(matrix_registros, dados_arr[3], dados_arr[4], dados_arr[5])
            # Busca o posto de combustível com o menor preço dentre os restantes
            posto_barato = get_melhor_preco(matrix_registros)
            localizacao_posto_barato = (posto_barato[2], posto_barato[3])

            # Envia a localização do posto de combustível mais indicado para compra
            mensagem_conclusao = str.encode('Posto mais indicado para compra: {}'.format(localizacao_posto_barato))
        
        soc.sendto(mensagem_conclusao, endereco_client)
        arquivo_registro.close()

# Chama a função main
if __name__ == '__main__':
    main()