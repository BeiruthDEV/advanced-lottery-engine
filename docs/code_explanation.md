# Explicação do Código


Este documento descreve a função de cada módulo do projeto.


## pyproject.toml
Define as dependências, metadados e configurações de build do projeto.


## config.yaml
Arquivo de configuração opcional para definir parâmetros padrão (tamanho do pool, seed, etc.).


## generator/utils.py
from typing import Optional
Importa a anotação de tipo Optional[T], usada para declarar que um argumento pode ser do tipo indicado ou None.
s
import secrets
Biblioteca do Python para geração de números aleatórios seguros (acesso ao Entropy do sistema). Útil para RNG criptográfico.

import random
Módulo de RNG padrão do Python com Random (reproduzível via seed) e utilitários como sample, choices.

import hashlib
Biblioteca para hashs (SHA-256 etc.). Aqui é usada para transformar uma seed textual em um inteiro bem distribuído.

def make_rng(seed: Optional[str] = None, secure: bool = True) -> random.Random:
Assinatura da função: cria e devolve um "gerador de números" (objeto com API semelhante a random.Random ou secrets.SystemRandom). seed permite reprodutibilidade; secure indica uso de RNG do sistema.

Docstring da função
Explica o comportamento: se seed dado -> RNG reproduzível; se secure True -> usa RNG seguro.

if seed is not None:
Ramificação para modo reproduzível: se o usuário passou uma string seed, o código gera um inteiro a partir do hash e instancia random.Random(seed_int).

h = hashlib.sha256(seed.encode("utf-8")).digest()
Gera bytes SHA-256 da seed. Permite transformar qualquer string em um espaço grande e uniforme de bits.

seed_int = int.from_bytes(h[:8], "big")
Pega os primeiros 8 bytes do hash e converte para inteiro. (8 bytes = 64 bits — suficiente para semear random.Random de forma determinística.)

rng = random.Random(seed_int)
Cria instância de random.Random com seed numérica — produz sequência reproduzível.

return rng
Retorna esse gerador reproduzível.

if secure:
Se não havia seed e secure é True, entramos no modo RNG seguro.

return secrets.SystemRandom()
Retorna SystemRandom que usa fontes seguras do sistema (não aceita .seed(); não é reproduzível, é o objetivo quando quer-se maior entropia).

return random.Random()
Se chegou aqui, não havia seed e secure é False: devolve um random.Random() sem seed (usa tempo/estado interno, não reproduzível por padrão).



## generator/strategies.py
from typing import List
Importa tipo List[...] para anotação de retorno.

from .utils import make_rng
Usa a fábrica de RNG criada em utils.py, centralizando política de RNG.

QuickPickStrategy
3. class QuickPickStrategy:
Declara a estratégia simples de "Quick Pick" — escolher n números únicos do pool.

Docstring da classe
Explica o objetivo da estratégia.

def __init__(..., pool_min=1, pool_max=60, numbers_per_ticket=6, seed=None, secure=True):
Parâmetros:

pool_min, pool_max: intervalo inclusivo de números disponíveis;

numbers_per_ticket: quantos números por bilhete;

seed e secure: repassados para make_rng.

self.pool_min = pool_min / self.pool_max = pool_max / self.n = numbers_per_ticket
Armazena as configurações da instância.

self.rng = make_rng(seed, secure)
Cria o gerador (reproduzível ou seguro) e guarda em self.rng para uso em generate().

def generate(self) -> List[int]:
Método que gera um bilhete.

pool = list(range(self.pool_min, self.pool_max + 1))
Monta a lista de números disponíveis (inclusive pool_max).

ticket = self.rng.sample(pool, k=self.n)
Seleciona n números únicos do pool usando o RNG criado — sample faz amostragem sem reposição.

return ticket
Devolve a lista de números gerada (ordem aleatória — a ordenação é responsabilidade de quem chamar, se desejar).

Observações sobre QuickPickStrategy:

Reprodutibilidade: se self.rng for random.Random(seed_int) então a mesma seed dá os mesmos tickets.

Segurança: se self.rng for SystemRandom, não é reproduzível, mas é mais entropicamente forte.

WeightedStrategy
12. class WeightedStrategy(QuickPickStrategy):
Herda QuickPick e adiciona suporte a pesos por número (para dar preferência a alguns números).

def __init__(self, weights: dict[int, float] | None = None, **kwargs):
Recebe um dicionário weights mapeando número→peso; **kwargs repassam para QuickPickStrategy.__init__.

self.weights = weights or {}
Normaliza para um dicionário vazio se None.

def generate(self) -> List[int]:
Método que gera utilizando os pesos.

Montagem de pool e verificação de weights
Se self.weights está vazio, faz fallback para o super().generate() — comportamento seguro.

probs = [self.weights.get(num, 1.0) for num in pool]
Para cada número do pool, pega o peso (default 1.0) e monta a lista de probabilidades não normalizadas.

Normalização (total = sum(probs) / probs = [p/total for p in probs])
Torna a lista em probabilidades somando 1. Se total <= 0 faz fallback.

Amostragem sem reposição ponderada (algoritmo ruleta com remoção)
Implementa repetidamente:

gerar um número aleatório r ∈ [0,1)

varrer probabilidades cumulativas até achar o índice correspondente

remover o elemento escolhido do pool e re-normalizar as probabilidades restantes

repetir n vezes

IMPORTANTE — bug/nota de reprodutibilidade
O código atual faz import random e r = random.random() dentro do loop: isso usa o RNG global do módulo random, não self.rng. Consequência:

Se você queria reprodutibilidade via seed, este trecho quebrará a reprodutibilidade porque usa o RNG global e não o self.rng semeado.

Solução recomendada: trocar por r = self.rng.random() ou usar self.rng.choices(population=..., weights=..., k=1) / self.rng.choice ou implementação que dependa consistentemente de self.rng.

return chosen
Retorna a lista de números escolhidos.




## generator/filters.py
from typing import List, Iterable
Tipos para anotações.

class ExcludeRecentFilter:
Filtro que impede números que apareceram em sorteios recentes.

Docstring com exemplo de uso
Mostra como passar recent_draws (lista de listas) e aplicar o filtro.

def __init__(self, recent_draws: Iterable[Iterable[int]] | None = None):
Recebe coleções de sorteios recentes.

self.recent_draws = list(recent_draws or [])
Garante lista; previne None.

self.excluded = set()
Conjunto para rápida verificação/remoção.

for draw in self.recent_draws: self.excluded.update(draw)
Junta todos os números que devem ser excluídos.

def apply(self, ticket: List[int]) -> List[int]:
Método que recebe um bilhete e devolve versão filtrada.

allowed = [n for n in ticket if n not in self.excluded]
Remove números indesejados mantendo a ordem original do ticket (exceto exclusões).

if not allowed: return ticket
Estratégia defensiva: se tudo foi excluído, devolve o ticket original em vez de retornar lista vazia.

return allowed
Caso normal: devolve os números permitidos.


## generator/core.py
from typing import List / from .strategies import QuickPickStrategy
Tipos e import da estratégia base.

class LotteryGenerator:
Orquestrador principal: usa estratégias e aplica filtros/ordenacão.

def __init__(self, strategy: QuickPickStrategy): self.strategy = strategy
Recebe e guarda a estratégia a ser usada (injeção de dependência → facilita testes e extensibilidade).

def generate_ticket(self, filters: list | None = None, sort: bool = True) -> List[int]:
API principal: gera um bilhete, aplica filtros (em cadeia), e opcionalmente ordena.

ticket = self.strategy.generate()
Gera um ticket bruto via estratégia.

if filters: for f in filters: ticket = f.apply(ticket)
Aplica cada filtro na ordem recebida, substituindo ticket a cada iteração (encadeamento).

if sort: try: ticket = sorted(ticket) except Exception: pass
Ordena o ticket se solicitado; try/except protege contra objetos não ordenáveis (defensivo).

return ticket
Entrega o ticket final.

def generate_multiple(self, count: int = 1, **kwargs) -> List[List[int]]:
Componente utilitário: gera count bilhetes chamando generate_ticket repetidamente.

return [self.generate_ticket(**kwargs) for _ in range(count)]
Simples compreensão para gerar múltiplos tickets.


## cli.py
import argparse
Biblioteca para parse de argumentos de linha de comando.

Import das classes do pacote (QuickPickStrategy, LotteryGenerator, ExcludeRecentFilter)
Conecta CLI com o core do gerador.

def build_args():
Função que monta o ArgumentParser com opções como --count, --pool-min, --pool-max, --n, --seed, --secure, --no-sort.

Uso dos add_argument
Define tipos, defaults e help para cada opção; --secure usa action="store_true" (flag).

if __name__ == "__main__":
Bloco executável quando o script é chamado diretamente.

args = build_args().parse_args()
Faz parser dos argumentos passados pelo usuário.

strat = QuickPickStrategy(..., seed=args.seed, secure=args.secure)
Instancia a estratégia com os parâmetros do CLI.

gen = LotteryGenerator(strat)
Cria o gerador principal com a estratégia.

Exemplo de leitura/uso de recent e filtro ExcludeRecentFilter
No exemplo simples o recent é codificado; em produção você leria de arquivo/API.

Geração e impressão dos tickets
Usa generate_multiple e imprime cada bilhete numerado.



## tests/test_generator.py
QuickPickStrategy e LotteryGenerator.

def test_quickpick_length():
Teste que:

Instancia QuickPickStrategy em modo não seguro (secure=False) com seed fixa ("testseed").

Gera um ticket e verifica len(t) == 5 e que todos os números estão no intervalo 1..10.

Objetivo: validar tamanho e limites do pool.

def test_multiple_tickets_unique_within():
Teste que:

Instancia QuickPickStrategy com pool_max=20, numbers_per_ticket=6, seed="abc".

Gera 10 tickets e valida que cada ticket não tem números repetidos (len(set(t)) == len(t)).

Objetivo: garantir amostragem sem reposição dentro do ticket.