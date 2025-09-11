# 🎲 Lottery Generator

Um gerador de apostas de loteria em **Python**, flexível e modular.  
Suporta **estratégias diferentes** (`QuickPick`, `Weighted`) e permite configuração via **config.yaml**.

---

## 🚀 Instalação

Crie e ative um ambiente virtual:

```bash
python -m venv venv
source venv/bin/activate
venv\Scripts\activate      
```


Instale as dependências em modo desenvolvimento:
```bash
pip install -e .
```

▶️ Uso via CLI

Um jogo padrão (QuickPick)
```bash
python cli.py generate
```
📌 Saída de exemplo:
```bash
Jogo 1: [3, 8, 15, 22, 41, 56]
```


Cinco jogos
```bash
python cli.py generate --tickets 5
```
📌 Saída de exemplo:
```bash
Jogo 1: [4, 12, 27, 33, 41, 55]
Jogo 2: [2, 9, 15, 28, 37, 44]
Jogo 3: [1, 7, 18, 23, 36, 60]
Jogo 4: [5, 14, 22, 31, 42, 59]
Jogo 5: [6, 11, 20, 29, 34, 48]
```

Usando estratégia ponderada (definida no config.yaml)
```bash
python cli.py generate --tickets 3 --strategy weighted
```
📌 Saída de exemplo:
```bash
Jogo 1: [7, 10, 22, 33, 42, 51]
Jogo 2: [3, 7, 13, 27, 38, 49]
Jogo 3: [7, 14, 19, 28, 35, 42]
```

Com seed fixa (resultados reprodutíveis)
```bash
python cli.py generate --tickets 2 --seed demo
```
```bash
Jogo 1: [3, 9, 21, 28, 34, 57]
Jogo 2: [2, 8, 17, 26, 39, 44]
```

Usando gerador seguro (secrets)
```bash
python cli.py generate --tickets 2 --secure
```
📌 Saída de exemplo:
```bash
Jogo 1: [1, 7, 13, 25, 36, 48]
Jogo 2: [5, 12, 20, 29, 37, 59]
```

▶️ Uso no Python (importando como biblioteca)
```bash
from generator.core import LotteryGenerator
from generator.strategies import QuickPickStrategy


s = QuickPickStrategy(pool_min=1, pool_max=60, numbers_per_ticket=6, seed="demo")
gen = LotteryGenerator(s)

print("Um jogo:", gen.generate_ticket())
print("Cinco jogos:", gen.generate_multiple(5))
```
📌 Saída de exemplo:
```bash
Um jogo: [5, 14, 23, 31, 42, 56]
Cinco jogos: [
  [2, 9, 15, 28, 37, 44],
  [1, 7, 18, 23, 36, 60],
  [4, 12, 27, 33, 41, 55],
  [6, 11, 20, 29, 34, 48],
  [3, 8, 16, 24, 39, 53]
]
```


🧪 Testes

Rodar todos os testes com:
```bash
pytest
```
Se tudo estiver certo, você verá:
```bash
========================== 4 passed in 0.05s ==========================
```
📂 Estrutura do Projeto
```bash
Projeto-Pessoal-Gerador-de-Loteria-Python/
│── generator/
│   ├── __init__.py
│   ├── core.py
│   ├── strategies.py
│── tests/
│   └── test_generator.py
│── docs/
│   ├── explicacao_codigo.md
│   └── linha_a_linha.md
│── cli.py
│── config.yaml
│── pyproject.toml
│── README.md
```

📜 Licença

Este projeto é pessoal e foi desenvolvido apenas para estudo e prática de programação em Python.
Não possui vínculo com nenhuma loteria oficial.
Você é livre para usar e modificar o código como quiser.

## ✍️ Autor

Desenvolvido por **Matheus Beiruth Miranda dos Santos**  
💼 [www.linkedin.com/in/matheusbeiruth]  
📧 [matheusbeiruth10@gmail.com]