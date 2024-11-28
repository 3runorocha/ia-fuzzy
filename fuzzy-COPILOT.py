import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

# 1. Definir as variáveis fuzzy
# Definindo o universo de discurso
experiencia = ctrl.Antecedent(np.arange(0, 11, 1), 'experiencia')
entrosamento = ctrl.Antecedent(np.arange(0, 11, 1), 'entrosamento')
rotatividade = ctrl.Antecedent(np.arange(0, 11, 1), 'rotatividade')
qualidade_requisitos = ctrl.Antecedent(np.arange(0, 11, 1), 'qualidade_requisitos')
mudanca_requisitos = ctrl.Antecedent(np.arange(0, 11, 1), 'mudanca_requisitos')
complexidade = ctrl.Antecedent(np.arange(0, 11, 1), 'complexidade')
tamanho = ctrl.Antecedent(np.arange(0, 11, 1), 'tamanho')
recursos = ctrl.Antecedent(np.arange(0, 11, 1), 'recursos')
orcamento = ctrl.Antecedent(np.arange(0, 11, 1), 'orcamento')
prazo = ctrl.Antecedent(np.arange(0, 11, 1), 'prazo')
dependencias = ctrl.Antecedent(np.arange(0, 11, 1), 'dependencias')
ambiguidade = ctrl.Antecedent(np.arange(0, 11, 1), 'ambiguidade')
risco = ctrl.Consequent(np.arange(0, 11, 1), 'risco')

# 2. Definir as funções de pertinência para cada variável
# Funções de pertinência para todas as variáveis de entrada e saída
for var in [experiencia, entrosamento, rotatividade, qualidade_requisitos, mudanca_requisitos, 
            complexidade, tamanho, recursos, orcamento, prazo, dependencias, ambiguidade]:
    var['baixa'] = fuzz.trimf(var.universe, [0, 0, 3])
    var['media'] = fuzz.trimf(var.universe, [3, 5, 7])
    var['alta'] = fuzz.trimf(var.universe, [7, 10, 10])

risco['baixo'] = fuzz.trimf(risco.universe, [0, 0, 3])
risco['medio'] = fuzz.trimf(risco.universe, [3, 5, 7])
risco['alto'] = fuzz.trimf(risco.universe, [7, 10, 10])

# 3. Definir as regras fuzzy abrangentes
rules = [
    ctrl.Rule(experiencia['baixa'] & complexidade['alta'], risco['alto']),
    ctrl.Rule(qualidade_requisitos['alta'] & recursos['alta'], risco['baixo']),
    ctrl.Rule(rotatividade['alta'] & mudanca_requisitos['alta'], risco['alto']),
    ctrl.Rule(entrosamento['alta'] & experiencia['alta'], risco['baixo']),
    ctrl.Rule(dependencias['alta'] & prazo['baixa'], risco['alto']),
    ctrl.Rule(orcamento['baixa'] & tamanho['alta'], risco['alto']),
    ctrl.Rule(ambiguidade['alta'] & qualidade_requisitos['baixa'], risco['alto']),
    ctrl.Rule(recursos['alta'] & complexidade['baixa'], risco['baixo']),
    ctrl.Rule(prazo['baixa'] & mudanca_requisitos['alta'], risco['alto']),
    ctrl.Rule(tamanho['baixa'] & entrosamento['alta'], risco['baixo']),
    ctrl.Rule(qualidade_requisitos['baixa'] & dependencias['alta'], risco['alto']),
    ctrl.Rule(experiencia['alta'] & complexidade['baixa'], risco['baixo']),
]

# 4. Criar o sistema de controle fuzzy
sistema_risco_ctrl = ctrl.ControlSystem(rules)
sistema_risco = ctrl.ControlSystemSimulation(sistema_risco_ctrl)

# 5. Definir entradas pré-definidas adequadas às regras
entradas = {
    'experiencia': 7,
    'entrosamento': 6,
    'rotatividade': 9,
    'qualidade_requisitos': 1,
    'mudanca_requisitos': 9,
    'complexidade': 5,
    'tamanho': 2,
    'recursos': 7,
    'orcamento': 1,
    'prazo': 10,
    'dependencias': 4,
    'ambiguidade': 3
}

# Passando entradas para o sistema fuzzy
sistema_risco.input['experiencia'] = entradas['experiencia']
sistema_risco.input['entrosamento'] = entradas['entrosamento']
sistema_risco.input['rotatividade'] = entradas['rotatividade']
sistema_risco.input['qualidade_requisitos'] = entradas['qualidade_requisitos']
sistema_risco.input['mudanca_requisitos'] = entradas['mudanca_requisitos']
sistema_risco.input['complexidade'] = entradas['complexidade']
sistema_risco.input['tamanho'] = entradas['tamanho']
sistema_risco.input['recursos'] = entradas['recursos']
sistema_risco.input['orcamento'] = entradas['orcamento']
sistema_risco.input['prazo'] = entradas['prazo']
sistema_risco.input['dependencias'] = entradas['dependencias']
sistema_risco.input['ambiguidade'] = entradas['ambiguidade']

# Verificação das entradas
for key, value in entradas.items():
    print(f"Entrada usada - {key}: {value}")

# 6. Computando o sistema fuzzy
try:
    sistema_risco.compute()
    # Exibindo o nível de risco calculado com duas casas decimais
    if 'risco' in sistema_risco.output:
        print(f"Nível de Risco: {sistema_risco.output['risco']:.2f}")
    else:
        print("Erro: A variável de saída 'risco' não foi computada corretamente.")
except Exception as e:
    print(f"Erro ao computar o sistema fuzzy: {e}")

# Função de pertinência de exemplo (substitua isso com suas funções reais)
def funcao_pertinencia(x):
    return np.exp(-x**2)

# 7. Plotagem das funções de pertinência
# Criar uma figura com subplots
fig, axes = plt.subplots(nrows=4, ncols=3, figsize=(15, 10))
plt.subplots_adjust(hspace=0.5)

# Plotar as funções de pertinência
for var, ax in zip([experiencia, entrosamento, rotatividade, qualidade_requisitos, mudanca_requisitos, 
                    complexidade, tamanho, recursos, orcamento, prazo, dependencias, ambiguidade], axes.flatten()):
    for label in var.terms:
        ax.plot(var.universe, var[label].mf, label=label)
        ax.axvline(entradas[var.label], color='r', linestyle='--')
    ax.set_title(f"Função de Pertinência - {var.label.capitalize()}")
    ax.legend()

# Exibir o gráfico de funções de pertinência para a saída calculada
risco.view(sim=sistema_risco)
plt.title("Função de Pertinência - Risco (Simulação)")
plt.xlabel("Nível de Risco")
plt.ylabel("Grau de Pertinência")

plt.show()
