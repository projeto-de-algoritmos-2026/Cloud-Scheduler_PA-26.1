# Cloud Scheduler - Simulador de Escalonamento Guloso

> Ferramenta para simular, visualizar e comparar algoritmos de escalonamento de tarefas em um ambiente inspirado em servidores cloud.

**Disciplina:** Projeto de Algoritmos
**Periodo:** 2026.1  
**Modulo:** 2 - Algoritmos Gulosos  
**Alunos:** Renato Gameiro e Vinicius Araruna

---

## Descricao do Projeto

Este projeto implementa uma simulacao de escalonamento de tarefas usando uma estrategia gulosa baseada em **EDF (Earliest Deadline First)**. O cenario representa um servidor que recebe tarefas com tempo de execucao, deadline e multa por atraso. O objetivo e ordenar a execucao para reduzir atrasos e minimizar a multa total acumulada.

A aplicacao compara o desempenho de tres estrategias:

- **EDF (Earliest Deadline First)** - executa primeiro as tarefas com menor deadline
- **FIFO (First In, First Out)** - executa as tarefas na ordem de chegada
- **Random** - executa as tarefas em ordem aleatoria para servir como baseline

O projeto possui duas formas de uso:

- **CLI em Python**, para executar simulacoes e comparar metricas no terminal
- **Interface web**, para visualizar graficos, indicadores e diagrama de Gantt de forma interativa

---

## Funcionalidades

### Geracao de Tarefas

- Cria tarefas com duracao, deadline e penalidade
- Permite configurar quantidade de tarefas e seed da simulacao
- Mantem os dados reprodutiveis para facilitar comparacoes

### Escalonamento Guloso com EDF

- Ordena as tarefas pelo deadline mais proximo
- Calcula inicio, fim, atraso e multa de cada tarefa
- Compara a solucao gulosa com FIFO e Random

### Metricas de Desempenho

- Quantidade de tarefas atrasadas
- Percentual de atraso
- Atraso maximo
- Multa total
- Makespan da execucao

### Interface Web

- Controles para alterar numero de tarefas, duracao maxima, folga de deadline e multa maxima
- KPIs com economia do EDF, atraso maximo, tarefas atrasadas e multa total
- Graficos comparativos usando Chart.js
- Tabela com resultados dos algoritmos
- Diagrama de Gantt para visualizar a ordem de execucao das tarefas

### Visualizacoes Estaticas

O modulo `src/visualizer.py` gera graficos em PNG na pasta `reports/`, incluindo:

- Multa total por algoritmo
- Tarefas atrasadas vs. tarefas no prazo
- Multa acumulada ao longo do tempo
- Diagrama de Gantt do EDF
- Analise de escalabilidade

---

## Requisitos

- **Python:** 3.8 ou superior
- **Matplotlib:** 3.7.0 ou superior
- **NumPy:** 1.24.0 ou superior
- **Navegador Web:** Chrome, Edge, Firefox ou equivalente

---

## Instalacao

### 1. Clonar Repositorio

```bash
git clone https://github.com/projeto-de-algoritmos-2026/G43_Greedy_PA-26.1.git
cd G43_Greedy_PA-26.1
```

### 2. Criar Ambiente Virtual

```bash
# Windows
python -m venv venv
.\venv\Scripts\Activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar Dependencias

```bash
pip install -r requirements.txt
```

---

## Como Executar

### Executar a Simulacao no Terminal

```bash
python main.py
```

Tambem e possivel definir a quantidade de tarefas e a seed:

```bash
python main.py --tasks 100 --seed 42
```

Exemplo de saida:

```text
Escalonamento de Tarefas - EDF
  100 tarefas | seed=42

  tempo de execucao: 1.2 ms

  Algoritmo    Atrasadas  % Atras.  Atraso Max      Multa Total
  EDF                 84      84.0%       820.4s  R$  9,123,456.78
  FIFO                90      90.0%       910.2s  R$ 10,234,567.89
  Random              92      92.0%       950.7s  R$ 11,345,678.90
```

### Abrir a Interface Web

Abra o arquivo abaixo diretamente no navegador:

```text
frontend/index.html
```

A interface roda localmente no navegador e nao precisa de servidor para funcionar.

---

## Estrutura do Projeto

```text
G43_Greedy_PA-26.1/
├── README.md
├── requirements.txt
├── main.py
├── src/
│   ├── __init__.py
│   ├── task.py
│   ├── generator.py
│   ├── schedulers.py
│   └── visualizer.py
└── frontend/
    ├── index.html
    ├── css/
    │   └── style.css
    └── js/
        ├── simulation.js
        ├── charts.js
        ├── gantt.js
        ├── table.js
        └── main.js
```

---

## Detalhes dos Algoritmos

### EDF (Earliest Deadline First)

- **Ideia:** ordenar as tarefas pelo menor deadline
- **Estrategia:** gulosa
- **Complexidade:** O(n log n), devido a ordenacao
- **Caracteristica:** prioriza tarefas mais urgentes e tende a reduzir atrasos em cenarios com deadlines apertados

### FIFO (First In, First Out)

- **Ideia:** executar as tarefas na ordem de chegada
- **Complexidade:** O(n log n) na implementacao atual, por ordenar pelo identificador
- **Caracteristica:** simples e previsivel, mas ignora deadline e penalidade

### Random

- **Ideia:** embaralhar as tarefas antes da execucao
- **Complexidade:** O(n)
- **Caracteristica:** usado como baseline para comparar o ganho do EDF contra uma ordem sem criterio

---

## Modelo de Tarefa

Cada tarefa possui:

| Campo | Descricao |
|-------|-----------|
| `task_id` | Identificador numerico da tarefa |
| `name` | Nome exibido nos resultados |
| `duration` | Tempo necessario para executar a tarefa |
| `deadline` | Tempo limite desejado para conclusao |
| `penalty` | Multa aplicada por segundo de atraso |
| `start_time` | Momento em que a tarefa comeca |
| `finish_time` | Momento em que a tarefa termina |

A multa total de uma tarefa e calculada como:

```text
max(0, finish_time - deadline) * penalty
```

---

## Analise de Desempenho

A simulacao calcula as principais metricas de cada algoritmo:

```text
late_count    -> quantidade de tarefas atrasadas
late_pct      -> percentual de tarefas atrasadas
max_lateness  -> maior atraso encontrado
avg_lateness  -> atraso medio entre tarefas atrasadas
total_penalty -> soma das multas por atraso
makespan      -> tempo total para concluir todas as tarefas
```

Na pratica, o EDF costuma apresentar melhores resultados quando deadlines sao relevantes, pois sua decisao local sempre favorece a tarefa mais urgente.

---

## Interface Web

A interface web foi criada para facilitar a exploracao visual do problema. O usuario pode ajustar os parametros da simulacao e observar imediatamente:

- Economia do EDF em relacao ao Random
- Atraso maximo do EDF
- Quantidade e percentual de tarefas atrasadas
- Multa total por algoritmo
- Evolucao da multa acumulada
- Ordem de execucao no diagrama de Gantt

As cores usadas na interface seguem a comparacao entre algoritmos:

| Cor | Algoritmo |
|-----|-----------|
| Verde | EDF |
| Vermelho | FIFO |
| Amarelo | Random |

---

## Relacao com Algoritmos Gulosos

O EDF e um exemplo direto de estrategia gulosa: a cada passo, ele escolhe a tarefa com deadline mais proximo, sem recalcular todas as combinacoes futuras possiveis. Essa decisao local e simples, eficiente e produz bons resultados para cenarios de escalonamento em que cumprir prazos e minimizar atraso sao prioridades.

---

