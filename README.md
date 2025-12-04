# Advanced Lottery Engine 🎲

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Architecture](https://img.shields.io/badge/Design%20Pattern-Strategy-orange)
![Security](https://img.shields.io/badge/RNG-Secure-green)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

## 📋 Project Overview
O **Advanced Lottery Engine** é uma solução de software projetada para a geração flexível e segura de combinações numéricas para sistemas de loteria. 

Diferente de scripts simples de aleatoriedade, este projeto implementa uma arquitetura robusta baseada no **Strategy Design Pattern**, permitindo a injeção de diferentes algoritmos de seleção (como *QuickPick* padrão ou *Weighted Selection*) sem alterar o núcleo da aplicação. O sistema também suporta geração criptograficamente segura (CSPRNG) para garantir a imprevisibilidade dos resultados.

## 🏗️ Architecture & Design Patterns

O projeto foi construído sobre princípios de **SOLID** e **Clean Code**:

* **Strategy Pattern:** A lógica de geração de números é encapsulada em classes de estratégia (`QuickPickStrategy`, `WeightedStrategy`). O `LotteryGenerator` (Contexto) desconhece os detalhes da implementação, apenas solicita a geração.
* **Dependency Injection:** A estratégia desejada é injetada no gerador em tempo de execução, baseada nos argumentos da CLI ou configuração YAML.
* **Secure RNG:** Utilização do módulo `secrets` do Python para geração de entropia segura, essencial para aplicações que exigem auditoria e justiça.
* **Configuration Management:** Separação entre código e configuração através de arquivos YAML, permitindo ajustes de pesos e regras sem *redeployment*.

## 🛠️ Tech Stack
* **Language:** Python 3.10+
* **CLI Framework:** `argparse` (Standard Library)
* **Configuration:** `PyYAML`
* **Security:** `secrets` (Cryptographically secure random numbers)

## 🚀 Installation

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/BeiruthDEV/advanced-lottery-engine.git](https://github.com/BeiruthDEV/advanced-lottery-engine.git)
    cd advanced-lottery-engine
    ```

2.  **Configure o ambiente virtual:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # Windows: venv\Scripts\activate
    pip install -r requirements.txt  # Ou: pip install -e .
    ```

## 💻 CLI Usage

A ferramenta oferece uma interface de linha de comando robusta para integração com outros sistemas ou uso direto.

### 1. Geração Padrão (QuickPick)
Gera um jogo simples utilizando distribuição uniforme.
```bash
python cli.py generate --tickets 1
# Output: Jogo 1: [5, 12, 23, 34, 45, 56]
```

### 2. Geração Ponderada (Weighted Strategy)
Utiliza pesos definidos no config.yaml para alterar a probabilidade de certos números (ex: baseada em estatísticas históricas).

```bash
python cli.py generate --tickets 3 --strategy weighted
```


### 3. Modo Seguro (Secure RNG)
Força o uso de fontes de entropia do sistema operacional para garantir aleatoriedade criptográfica.

```bash
python cli.py generate --tickets 5 --secure
```

### 4. Reproducibilidade (Seeding)
Permite replicar resultados para fins de teste e depuração.

```bash
python cli.py generate --seed "audit-test-2025"
```


## ⚙️ Configuration (YAML)
O comportamento do sistema é controlado via config.yaml:
```bash

YAML

quickpick:
  pool_min: 1
  pool_max: 60
  numbers_per_ticket: 6

weighted:
  pool_min: 1
  pool_max: 60
  weights:
    10: 2.5  # O número 10 tem 2.5x mais chance de aparecer
    23: 0.5  # O número 23 tem metade da chance
```

## 🧪 Extensibility
Para adicionar uma nova lógica (ex: baseada em Sequência de Fibonacci), basta estender a classe base e injetá-la no core.py, sem necessidade de refatorar o código existente.

Desenvolvido por Matheus Beiruth.
