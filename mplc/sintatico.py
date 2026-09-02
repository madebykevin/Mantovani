"""
Entrega 2 — Analisador Sintático e Construção da AST (Árvore Sintática Abstrata).

Módulo responsável por validar a estrutura gramatical do programa a partir
dos tokens gerados na fase léxica e construir a árvore hierárquica correspondente.
"""
from typing import List, Optional, Any
from mplc.erros import NaoImplementado


class No:
    """
    Nó estrutural da Árvore Sintática Abstrata (AST).
    Armazena o rótulo da operação/regra, lista de nós filhos e posições de origem.
    """

    def __init__(self, rotulo: str, filhos: Optional[List['No']] = None, linha: int = 0, coluna: int = 0, **atributos: Any):
        self.rotulo = rotulo
        self.filhos = filhos if filhos is not None else []
        self.linha = linha
        self.coluna = coluna
        self.extra = atributos

    def __repr__(self) -> str:
        return f"No({self.rotulo!r}, filhos={len(self.filhos)})"


def analisar(tokens: List[Any]) -> No:
    """
    Recebe a lista de tokens e produz a raiz da AST (nó 'programa').
    A ser implementado na Entrega 2 utilizando método descendente recursivo.
    """
    raise NaoImplementado('a analise sintatica (Entrega 2)')


def despejar(raiz: No, nivel: int = 0, buffer_saida: Optional[List[str]] = None) -> List[str]:
    """
    Formata e exporta a AST com indentação de 2 espaços por nível conforme CONTRATOS.md.
    """
    buffer_saida = buffer_saida if buffer_saida is not None else []
    buffer_saida.append('  ' * nivel + raiz.rotulo)
    for filho in raiz.filhos:
        despejar(filho, nivel + 1, buffer_saida)
    return buffer_saida
