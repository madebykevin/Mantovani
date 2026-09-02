"""
Ponto de entrada e despachante da linha de comando do compilador MPL.
Gerencia os modos de compilação por fases e a execução na máquina virtual.
"""
import sys
from typing import List

from mplc.erros import ErroMPL, NaoImplementado
from mplc import lexico, sintatico, semantica, intermediario, gerador, vm

OPCOES_MODO = {
    '--tokens': 'tokens',
    '--ast': 'ast',
    '--tabela': 'tabela',
    '--ir': 'ir',
}


def compilar_ate(fonte: str, etapa: str) -> List[str]:
    """
    Executa o pipeline de compilação até a etapa especificada,
    retornando a lista de linhas geradas para impressão/gravação.
    """
    # 1. Análise Léxica
    lista_tokens = lexico.analisar(fonte)
    if etapa == 'tokens':
        return [str(tok) for tok in lista_tokens]

    # 2. Análise Sintática
    arvore_sintatica = sintatico.analisar(lista_tokens)
    if etapa == 'ast':
        return sintatico.despejar(arvore_sintatica)

    # 3. Análise Semântica
    tabela_simbolos = semantica.analisar(arvore_sintatica)
    if etapa == 'tabela':
        return semantica.despejar(tabela_simbolos)

    # 4. Código Intermediário
    codigo_ir = intermediario.gerar(arvore_sintatica, tabela_simbolos)
    if etapa == 'ir':
        return intermediario.despejar(codigo_ir)

    # 5. Geração de Bytecode
    return gerador.gerar(codigo_ir)


def main(argumentos: List[str]) -> int:
    """Função principal de processamento de comandos."""
    modo_selecionado = 'bytecode'
    modo_execucao = False
    arquivos_alvo: List[str] = []

    for arg in argumentos:
        if arg in OPCOES_MODO:
            modo_selecionado = OPCOES_MODO[arg]
        elif arg == '--rodar':
            modo_execucao = True
        else:
            arquivos_alvo.append(arg)

    if len(arquivos_alvo) != 1:
        print('uso: ./compilar [--tokens|--ast|--tabela|--ir] programa.mpl', file=sys.stderr)
        print('     ./executar programa.mplb', file=sys.stderr)
        return 1

    caminho_arquivo = arquivos_alvo[0]

    try:
        if modo_execucao:
            with open(caminho_arquivo, encoding='utf-8') as f:
                codigo_vm = f.read()
            vm.executar(codigo_vm, sys.stdout)
            return 0

        with open(caminho_arquivo, encoding='utf-8') as f:
            conteudo_fonte = f.read()

        resultado_linhas = compilar_ate(conteudo_fonte, modo_selecionado)

        if modo_selecionado == 'bytecode':
            if caminho_arquivo.endswith('.mpl'):
                arquivo_destino = caminho_arquivo[:-4] + '.mplb'
            else:
                arquivo_destino = caminho_arquivo + '.mplb'

            with open(arquivo_destino, 'w', encoding='utf-8') as f:
                f.write('\n'.join(resultado_linhas) + '\n')
        else:
            print('\n'.join(resultado_linhas))

        return 0

    except ErroMPL as erro:
        print(erro, file=sys.stderr)
        return 2 if erro.fase == 'execucao' else 1
    except NaoImplementado as pendente:
        print(f"ainda falta escrever: {pendente}", file=sys.stderr)
        return 3
    except FileNotFoundError:
        print(f"nao achei o arquivo {caminho_arquivo}", file=sys.stderr)
        return 1
    except RecursionError:
        print("erro execucao: linha 1, coluna 1: estouro de pilha", file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
