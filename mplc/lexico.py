"""
Entrega 1 — Analisador Léxico da linguagem MPL (Minha Pequena Linguagem).

Responsável pela leitura do fluxo de caracteres do código-fonte e conversão
em uma sequência ordenada de objetos Token, finalizando obrigatoriamente com
o marcador FIM_ARQUIVO.
"""
from typing import List, Optional
from mplc.erros import ErroMPL


class Token:
    """
    Representação de uma unidade léxica identificada no código-fonte.
    Armazena tipo, lexema original e posição (linha e coluna 1-based).
    """
    __slots__ = ('tipo', 'lexema', 'linha', 'coluna')

    def __init__(self, tipo: str, lexema: str, linha: int, coluna: int):
        self.tipo = tipo
        self.lexema = lexema
        self.linha = linha
        self.coluna = coluna

    def __str__(self) -> str:
        # Formato canônico especificado em CONTRATOS.md: linha,coluna,TIPO,lexema
        return f"{self.linha},{self.coluna},{self.tipo},{self.lexema}"

    def __repr__(self) -> str:
        return f"Token({self.tipo!r}, {self.lexema!r}, l={self.linha}, c={self.coluna})"


# Mapeamento de palavras-chave reservadas da linguagem MPL
PALAVRAS_CHAVE = {
    'funcao': 'FUNCAO',
    'retorne': 'RETORNE',
    'se': 'SE',
    'senao': 'SENAO',
    'enquanto': 'ENQUANTO',
    'escreva': 'ESCREVA',
    'inteiro': 'TIPO_INTEIRO',
    'real': 'TIPO_REAL',
    'logico': 'TIPO_LOGICO',
    'texto': 'TIPO_TEXTO',
    'vazio': 'TIPO_VAZIO',
    'verdadeiro': 'LOGICO',
    'falso': 'LOGICO',
    'e': 'E',
    'ou': 'OU',
    'nao': 'NAO',
}

# Operadores relacionais compostos (avaliados prioritariamente para evitar conflito com prefixos simples)
OPERADORES_COMPOSTOS = {
    '==': 'IGUAL',
    '!=': 'DIFERENTE',
    '<=': 'MENOR_IGUAL',
    '>=': 'MAIOR_IGUAL',
}

# Operadores aritméticos, lógicos e símbolos delimitadores de caractere único
SIMBOLOS_SIMPLES = {
    '+': 'MAIS',
    '-': 'MENOS',
    '*': 'VEZES',
    '/': 'DIVIDE',
    '%': 'RESTO',
    '<': 'MENOR',
    '>': 'MAIOR',
    '=': 'ATRIBUI',
    '(': 'ABRE_PAR',
    ')': 'FECHA_PAR',
    '{': 'ABRE_CHAVE',
    '}': 'FECHA_CHAVE',
    ',': 'VIRGULA',
    ';': 'PONTO_VIRGULA',
}

# Caracteres de escape válidos dentro de literais de texto
ESCAPES_PERMITIDOS = {'n', 't', '"', '\\'}


class AnalisadorLexico:
    """
    Scanner léxico estruturado que itera sobre o código-fonte gerando tokens.
    Controla posições de linha, coluna e índice absoluto.
    """

    def __init__(self, fonte: str):
        self._fonte = fonte
        self._total = len(fonte)
        self._cursor = 0
        self._linha = 1
        self._coluna = 1

    @property
    def _fim(self) -> bool:
        return self._cursor >= self._total

    def _espiar(self, deslocamento: int = 0) -> str:
        alvo = self._cursor + deslocamento
        return self._fonte[alvo] if alvo < self._total else ''

    def _avancar(self) -> str:
        ch = self._fonte[self._cursor]
        self._cursor += 1
        if ch == '\n':
            self._linha += 1
            self._coluna = 1
        else:
            self._coluna += 1
        return ch

    def _pular_espacos_e_comentarios(self) -> None:
        """Consome espaços em branco, quebras de linha e comentários de linha/bloco."""
        while not self._fim:
            ch = self._espiar()

            # Espaços em branco e quebras de linha
            if ch in ' \t\r\n':
                self._avancar()
                continue

            # Comentário de linha (// até o final da linha)
            if ch == '/' and self._espiar(1) == '/':
                self._avancar()
                self._avancar()
                while not self._fim and self._espiar() != '\n':
                    self._avancar()
                continue

            # Comentário de bloco (/* até */)
            if ch == '/' and self._espiar(1) == '*':
                lin_inicio, col_inicio = self._linha, self._coluna
                self._avancar()
                self._avancar()
                fechado = False
                while not self._fim:
                    if self._espiar() == '*' and self._espiar(1) == '/':
                        self._avancar()
                        self._avancar()
                        fechado = True
                        break
                    self._avancar()
                if not fechado:
                    raise ErroMPL('lexico', lin_inicio, col_inicio, 'comentario de bloco nao fechado')
                continue

            # Não há mais espaços ou comentários a consumir
            break

    def _processar_identificador_ou_palavra(self) -> Token:
        """Lê identificadores e palavras reservadas seguindo a regra do máximo munch."""
        lin_token, col_token = self._linha, self._coluna
        inicio_idx = self._cursor

        while not self._fim:
            ch = self._espiar()
            if ('a' <= ch <= 'z') or ('A' <= ch <= 'Z') or ('0' <= ch <= '9') or ch == '_':
                self._avancar()
            else:
                break

        lexema = self._fonte[inicio_idx:self._cursor]
        tipo = PALAVRAS_CHAVE.get(lexema, 'ID')
        return Token(tipo, lexema, lin_token, col_token)

    def _processar_numero(self) -> Token:
        """Lê literais inteiros e reais, validando a obrigatoriedade de dígitos antes e após o ponto."""
        lin_token, col_token = self._linha, self._coluna
        inicio_idx = self._cursor

        while not self._fim and '0' <= self._espiar() <= '9':
            self._avancar()

        # Verifica se há ponto indicando número real
        if not self._fim and self._espiar() == '.':
            col_ponto = self._coluna
            self._avancar()

            # O ponto exige ao menos um dígito na sequência imediata
            if self._fim or not ('0' <= self._espiar() <= '9'):
                raise ErroMPL('lexico', lin_token, col_ponto, 'o ponto do numero real exige digito antes e depois')

            while not self._fim and '0' <= self._espiar() <= '9':
                self._avancar()

            lexema = self._fonte[inicio_idx:self._cursor]
            return Token('REAL', lexema, lin_token, col_token)

        lexema = self._fonte[inicio_idx:self._cursor]
        return Token('INTEIRO', lexema, lin_token, col_token)

    def _processar_texto(self) -> Token:
        """Lê cadeias literais entre aspas duplas, validando escapes e fechamento de linha."""
        lin_token, col_token = self._linha, self._coluna
        inicio_idx = self._cursor

        # Consome aspas de abertura
        self._avancar()

        while not self._fim:
            ch = self._espiar()

            # Fechamento com aspas
            if ch == '"':
                self._avancar()
                lexema = self._fonte[inicio_idx:self._cursor]
                return Token('TEXTO', lexema, lin_token, col_token)

            # Quebra de linha não permitida sem fechar texto
            if ch == '\n':
                break

            # Tratamento de escape
            if ch == '\\':
                col_barra = self._coluna
                self._avancar()
                prox = self._espiar()
                if not self._fim and prox in ESCAPES_PERMITIDOS:
                    self._avancar()
                    continue
                raise ErroMPL('lexico', self._linha, col_barra, 'escape desconhecido dentro de texto')

            self._avancar()

        raise ErroMPL('lexico', lin_token, col_token, 'texto sem fechar na mesma linha')

    def escanear(self) -> List[Token]:
        """Varre todo o texto de entrada gerando a lista de tokens finalizada por FIM_ARQUIVO."""
        tokens: List[Token] = []

        while True:
            self._pular_espacos_e_comentarios()

            if self._fim:
                break

            ch = self._espiar()
            lin_atual, col_atual = self._linha, self._coluna

            # 1. Identificadores ou Palavras-Chave
            if ('a' <= ch <= 'z') or ('A' <= ch <= 'Z') or ch == '_':
                tokens.append(self._processar_identificador_ou_palavra())
                continue

            # 2. Literais Numéricos (Inteiro ou Real)
            if '0' <= ch <= '9':
                tokens.append(self._processar_numero())
                continue

            # 3. Literais de Texto
            if ch == '"':
                tokens.append(self._processar_texto())
                continue

            # 4. Operadores Relacionais Compostos (==, !=, <=, >=)
            par = self._fonte[self._cursor:self._cursor + 2]
            if par in OPERADORES_COMPOSTOS:
                self._avancar()
                self._avancar()
                tokens.append(Token(OPERADORES_COMPOSTOS[par], par, lin_atual, col_atual))
                continue

            # 5. Operadores Simples e Delimitadores
            if ch in SIMBOLOS_SIMPLES:
                self._avancar()
                tokens.append(Token(SIMBOLOS_SIMPLES[ch], ch, lin_atual, col_atual))
                continue

            # Caractere inválido encontrado
            raise ErroMPL('lexico', lin_atual, col_atual, f"caractere invalido {ch!r}")

        # Marcação mandatória de término de arquivo
        tokens.append(Token('FIM_ARQUIVO', '', self._linha, self._coluna))
        return tokens


def analisar(fonte: str) -> List[Token]:
    """
    Função principal da etapa léxica.
    Recebe o código-fonte em formato string e retorna a lista de tokens correspondente.
    """
    scanner = AnalisadorLexico(fonte)
    return scanner.escanear()
