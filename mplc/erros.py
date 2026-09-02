"""
Definição de exceções e tratamento de erros do compilador MPL.
Formato e fases padronizados de acordo com a especificação em CONTRATOS.md.
"""


class ErroMPL(Exception):
    """
    Representa uma falha detectada durante as fases de compilação ou execução.
    Armazena a fase de ocorrência, localização (linha e coluna) e descrição textual.
    """

    def __init__(self, fase: str, linha: int, coluna: int, mensagem: str):
        super().__init__(mensagem)
        self.fase = fase          # 'lexico', 'sintatico', 'semantico' ou 'execucao'
        self.linha = linha        # Indexação 1-based (primeira linha = 1)
        self.coluna = coluna      # Indexação 1-based (primeira coluna = 1)
        self.mensagem = mensagem

    def __str__(self) -> str:
        return f"erro {self.fase}: linha {self.linha}, coluna {self.coluna}: {self.mensagem}"


class NaoImplementado(Exception):
    """
    Sinaliza que determinada etapa do pipeline ainda não foi implementada no compilador.
    """

    def __init__(self, etapa: str):
        super().__init__(etapa)
        self.etapa = etapa

    def __str__(self) -> str:
        return str(self.etapa)
