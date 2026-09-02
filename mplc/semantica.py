"""
Entrega 3 — Análise Semântica, Tabela de Símbolos e Checagem de Tipos.

Valida regras contextuais da linguagem MPL: resolução de identificadores,
escopos estáticos aninhados, compatibilidade de tipos e fluxos de retorno.
"""
from typing import List, Any
from mplc.erros import NaoImplementado


def analisar(arvore_ast: Any) -> Any:
    """
    Percorre a AST, constrói a tabela de símbolos e realiza a checagem de tipos.
    Retorna o ambiente de símbolos resolvido.
    """
    raise NaoImplementado('a analise semantica (Entrega 3)')


def despejar(tabela_simbolos: Any) -> List[str]:
    """
    Formata o mapa de escopos e declarações de símbolos conforme especificado em CONTRATOS.md.
    """
    raise NaoImplementado('o despejo da tabela de simbolos (Entrega 3)')
