"""
Entrega 4 (Parte 3) — Máquina Virtual da Linguagem MPL.

Interpretador baseado em pilha para execução das instruções .mplb,
gerenciamento de chamadas recursivas (frames de ativação) e tratamento de exceções em runtime.
"""
from typing import TextIO
from mplc.erros import NaoImplementado


def executar(conteudo_mplb: str, saida: TextIO) -> None:
    """
    Executa o programa compilado em formato .mplb, direcionando impressões
    dos comandos 'escreva' para o stream fornecido em `saida`.
    """
    raise NaoImplementado('a maquina virtual (Entrega 4)')
