from abc import ABC, abstractmethod
from typing import Optional
from collections import defaultdict

# ════════════════════════════════════════════════════════════════════
#  INTERFACES (ISP - Segregação de Interfaces)
# ════════════════════════════════════════════════════════════════════

class Exibivel(ABC):
    @abstractmethod
    def exibir(self) -> str:
        """Retorna a representação formatada em texto para CLI ou UI."""
        ...

class Avaliavel(ABC):
    @abstractmethod
    def avaliar(self, avaliacao: "Avaliacao") -> None:
        ...

class Pesquisavel(ABC):
    @abstractmethod
    def buscar_por_genero(self, genero: str) -> list:
        ...


# ════════════════════════════════════════════════════════════════════
#  PLATAFORMA E AVALIAÇÃO [source: 1]
# ════════════════════════════════════════════════════════════════════

class Plataforma(Exibivel):
    _total_plataformas: int = 0

    def __init__(self, nome: str, fabricante: str) -> None:
        self._nome: str = nome
        self._fabricante: str = fabricante
        self._online: bool = True
        Plataforma._total_plataformas += 1

    @property
    def nome(self) -> str: return self._nome
    @property
    def fabricante(self) -> str: return self._fabricante
    @property
    def online(self) -> bool: return self._online

    def exibir(self) -> str:
        status = "🟢 Online" if self._online else "🔴 Offline"
        return f"🖥️ {self._nome} ({self._fabricante}) — {status}"


class Avaliacao(Exibivel):
    NOTA_MIN: int = 0
    NOTA_MAX: int = 10

    def __init__(self, nota: float, comentario: str) -> None:
        self.nota = nota
        self._comentario: str = comentario

    @property
    def nota(self) -> float: return self._nota

    @nota.setter
    def nota(self, valor: float) -> None:
        if not (self.NOTA_MIN <= valor <= self.NOTA_MAX):
            raise ValueError(f"Nota deve estar entre {self.NOTA_MIN} e {self.NOTA_MAX}.")
        self._nota = valor
        self._recomenda = valor >= 7.0

    @property
    def comentario(self) -> str: return self._comentario
    @property
    def recomenda(self) -> bool: return self._recomenda

    def exibir(self) -> str:
        rec = "👍 Recomendado" if self._recomenda else "👎 Não recomendado"
        return f"⭐ Nota: {self._nota:.1f}/10 — {self._comentario} ({rec})"


# ════════════════════════════════════════════════════════════════════
#  JOGO (LSP & OCP) [source: 1]
# ════════════════════════════════════════════════════════════════════

class Jogo(Exibivel, Avaliavel, ABC):
    _total_jogos: int = 0

    def __init__(self, titulo: str, genero: str, plataforma: Plataforma,
                 horas_jogadas: float = 0.0) -> None:
        self._titulo: str = titulo
        self._genero: str = genero
        self._plataforma: Plataforma = plataforma
        self._horas_jogadas: float = horas_jogadas
        self._zerado: bool = False
        self._avaliacao: Optional[Avaliacao] = None
        self._favorito: bool = False
        Jogo._total_jogos += 1

    @property
    def titulo(self) -> str: return self._titulo
    @property
    def genero(self) -> str: return self._genero
    @property
    def horas_jogadas(self) -> float: return self._horas_jogadas
    @property
    def zerado(self) -> bool: return self._zerado
    @property
    def favorito(self) -> bool: return self._favorito
    @property
    def avaliacao(self) -> Optional[Avaliacao]: return self._avaliacao
    @property
    def plataforma(self) -> Plataforma: return self._plataforma

    @zerado.setter
    def zerado(self, valor: bool) -> None: self._zerado = valor

    @favorito.setter
    def favorito(self, valor: bool) -> None: self._favorito = valor

    def avaliar(self, avaliacao: Avaliacao) -> None:
        self._avaliacao = avaliacao

    @abstractmethod
    def tipo(self) -> str: ...

    def exibir(self) -> str:
        status = "✅ Zerado" if self._zerado else "⚠️ Em andamento"
        fav = " [❤️]" if self._favorito else ""
        base = (f"● {self._titulo}{fav} | {self._genero} | {self.tipo()} | "
                f"{self._plataforma.nome} | {self._horas_jogadas:.0f}h | {status}")
        if self._avaliacao:
            base += f"\n   {self._avaliacao.exibir()}"
        return base


class JogoSingle(Jogo):
    def __init__(self, titulo: str, genero: str, plataforma: Plataforma,
                 horas_jogadas: float = 0.0, duracao_campanha: float = 0.0, runs: int = 0) -> None:
        super().__init__(titulo, genero, plataforma, horas_jogadas)
        self._duracao_campanha: float = max(0.0, duracao_campanha)
        self._runs: int = max(0, runs)

    def progresso(self) -> float:
        # Se o jogo foi zerado, garante 100% automaticamente
        if self._zerado:
            return 100.0
        # Se não foi zerado e não tem campanha cadastrada, fica em 0%
        if self._duracao_campanha == 0:
            return 0.0
        # Caso contrário, calcula a porcentagem (limitada a 100%)
        return min(100.0, (self._horas_jogadas / self._duracao_campanha) * 100)
    
    def tipo(self) -> str:
        return "Single-player"

    def exibir(self) -> str:
        res = [super().exibir()]
        if self._duracao_campanha:
            res.append(f"   📊 Progresso da campanha: {self.progresso():.1f}%")
        if self._runs:
            res.append(f"   🔁 Runs totais: {self._runs}")
        return "\n".join(res)


class JogoMultiplayer(Jogo):
    def __init__(self, titulo: str, genero: str, plataforma: Plataforma,
                 horas_jogadas: float = 0.0, partidas: int = 0) -> None:
        super().__init__(titulo, genero, plataforma, horas_jogadas)
        self._partidas: int = max(0, partidas)

    def registrar_partida(self, horas: float = 0.5) -> None:
        self._partidas += 1
        self._horas_jogadas += horas

    def tipo(self) -> str:
        return "Multiplayer"

    def exibir(self) -> str:
        return f"{super().exibir()}\n   🎯 Partidas jogadas: {self._partidas}"


# ════════════════════════════════════════════════════════════════════
#  BIBLIOTECA (Tabelas Hash + Recursão + SRP)
# ════════════════════════════dict════════════════════════════════════

class Biblioteca(Pesquisavel):
    def __init__(self) -> None:
        # TABELA HASH 1: Mapeamento de Título -> Objeto Jogo O(1)
        self._tabela_jogos: dict[str, Jogo] = {}
        # TABELA HASH 2: Índice de Gênero -> Conjunto de Jogos O(1)
        self._indice_genero: dict[str, set[Jogo]] = defaultdict(set)

    @property
    def jogos(self) -> list[Jogo]:
        return list(self._tabela_jogos.values())

    def adicionar_jogo(self, jogo: Jogo) -> bool:
        """Adiciona um jogo à tabela hash em O(1)."""
        chave = jogo.titulo.lower()
        if chave in self._tabela_jogos:
            return False
        self._tabela_jogos[chave] = jogo
        self._indice_genero[jogo.genero.lower()].add(jogo)
        return True

    def remover_jogo(self, titulo: str) -> bool:
        """Remove um jogo pelas tabelas hash em O(1)."""
        chave = titulo.lower()
        jogo = self._tabela_jogos.pop(chave, None)
        if not jogo:
            return False
        self._indice_genero[jogo.genero.lower()].discard(jogo)
        return True

    def buscar_por_genero(self, genero: str) -> list[Jogo]:
        """Consulta na tabela hash do índice de gêneros em O(1)."""
        return list(self._indice_genero.get(genero.lower(), set()))

    def buscar_por_genero_parcial(self, termo: str) -> list[Jogo]:
        termo_lower = termo.lower()
        resultado = set()
        for genero, conjunto_jogos in self._indice_genero.items():
            if termo_lower in genero:
                resultado.update(conjunto_jogos)
        return list(resultado)

    def generos_disponiveis(self) -> list[str]:
        return sorted({j.genero for j in self.jogos})

    # ── RECURSÃO ─────────────────────────────────────────────────────
    def _somar_horas_recursivo(self, lista_jogos: list[Jogo], indice: int = 0) -> float:
        """Algoritmo recursivo para soma total das horas jogadas na coleção."""
        # Caso base: chegamos ao fim da lista
        if indice >= len(lista_jogos):
            return 0.0
        # Passo recursivo: hora do jogo atual + soma recursiva do restante
        return lista_jogos[indice].horas_jogadas + self._somar_horas_recursivo(lista_jogos, indice + 1)

    def total_horas(self) -> float:
        return self._somar_horas_recursivo(self.jogos)
    # ─────────────────────────────────────────────────────────────────

    def media_horas(self) -> float:
        total = len(self._tabela_jogos)
        return self.total_horas() / total if total > 0 else 0.0

    def jogo_mais_jogado(self) -> Optional[Jogo]:
        if not self._tabela_jogos:
            return None
        return max(self._tabela_jogos.values(), key=lambda j: j.horas_jogadas)

    def listar_zerados(self) -> list[Jogo]:
        return [j for j in self.jogos if j.zerado]

    def listar_em_andamento(self) -> list[Jogo]:
        return [j for j in self.jogos if not j.zerado]

    def listar_favoritos(self) -> list[Jogo]:
        return [j for j in self.jogos if j.favorito]

    def __len__(self) -> int:
        return len(self._tabela_jogos)


# ════════════════════════════════════════════════════════════════════
#  USUÁRIO [source: 1]
# ════════════════════════════════════════════════════════════════════

class Usuario(Exibivel):
    _total_usuarios: int = 0

    def __init__(self, nome: str, username: str, email: str = "") -> None:
        self._nome: str = nome
        self._username: str = username
        self._email: str = email
        self._biblioteca: Biblioteca = Biblioteca()
        self._nivel: int = 1
        Usuario._total_usuarios += 1

    @property
    def nome(self) -> str: return self._nome
    @property
    def username(self) -> str: return self._username
    @property
    def email(self) -> str: return self._email
    @property
    def biblioteca(self) -> Biblioteca: return self._biblioteca
    @property
    def nivel(self) -> int:
        self._calcular_nivel()
        return self._nivel

    def _calcular_nivel(self) -> None:
        horas = self._biblioteca.total_horas()
        if horas < 10:   self._nivel = 1
        elif horas < 50: self._nivel = 2
        elif horas < 150: self._nivel = 3
        elif horas < 300: self._nivel = 4
        else:            self._nivel = 5

    def exibir(self) -> str:
        self._calcular_nivel()
        lib = self._biblioteca
        top = lib.jogo_mais_jogado()
        top_str = f"{top.titulo} ({top.horas_jogadas:.0f}h)" if top else "Nenhum"
        
        return (
            f"👤 {self._nome} (@{self._username}) | 🏆 Nível: {self._nivel}\n"
            f"🎮 Jogos: {len(lib)} | ⏱️ Total: {lib.total_horas():.0f}h | "
            f"Média: {lib.media_horas():.1f}h/jogo\n"
            f"🥇 Mais jogado: {top_str}"
        )