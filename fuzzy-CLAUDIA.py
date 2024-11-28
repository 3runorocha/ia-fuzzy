import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

class ProjetoRiscoFuzzy:
    def __init__(self):
        self.experiencia = ctrl.Antecedent(np.arange(0, 11, 1), 'experiencia')
        self.complexidade = ctrl.Antecedent(np.arange(0, 11, 1), 'complexidade')
        self.estabilidade_requisitos = ctrl.Antecedent(np.arange(0, 11, 1), 'estabilidade_requisitos')
        self.maturidade_tecnologica = ctrl.Antecedent(np.arange(0, 11, 1), 'maturidade_tecnologica')
        self.tamanho_equipe = ctrl.Antecedent(np.arange(0, 11, 1), 'tamanho_equipe')
        self.rotatividade = ctrl.Antecedent(np.arange(0, 11, 1), 'rotatividade')
        self.qualidade_documentacao = ctrl.Antecedent(np.arange(0, 11, 1), 'qualidade_documentacao')
        self.interdependencia_modulos = ctrl.Antecedent(np.arange(0, 11, 1), 'interdependencia_modulos')
        self.recursos_orcamentarios = ctrl.Antecedent(np.arange(0, 11, 1), 'recursos_orcamentarios')
        self.suporte_gerencia = ctrl.Antecedent(np.arange(0, 11, 1), 'suporte_gerencia')
        self.complexidade_requisitos = ctrl.Antecedent(np.arange(0, 11, 1), 'complexidade_requisitos')
        self.integracao_sistemas = ctrl.Antecedent(np.arange(0, 11, 1), 'integracao_sistemas')
        
        self.risco_projeto = ctrl.Consequent(np.arange(0, 11, 1), 'risco_projeto')
        
        # Funções de pertinência para variáveis de entrada
        variaveis_entrada = [
            self.experiencia, self.complexidade, self.estabilidade_requisitos,
            self.maturidade_tecnologica, self.tamanho_equipe, self.rotatividade,
            self.qualidade_documentacao, self.interdependencia_modulos,
            self.recursos_orcamentarios, self.suporte_gerencia,
            self.complexidade_requisitos, self.integracao_sistemas
        ]
        
        for variavel in variaveis_entrada:
            variavel['baixo'] = fuzz.trimf(variavel.universe, [0, 0, 5])
            variavel['medio'] = fuzz.trimf(variavel.universe, [2, 5, 8])
            variavel['alto'] = fuzz.trimf(variavel.universe, [5, 10, 10])
        
        # Funções de pertinência para risco do projeto
        self.risco_projeto['muito_baixo'] = fuzz.trimf(self.risco_projeto.universe, [0, 0, 2])
        self.risco_projeto['baixo'] = fuzz.trimf(self.risco_projeto.universe, [1, 3, 5])
        self.risco_projeto['medio'] = fuzz.trimf(self.risco_projeto.universe, [4, 5, 6])
        self.risco_projeto['alto'] = fuzz.trimf(self.risco_projeto.universe, [5, 7, 9])
        self.risco_projeto['muito_alto'] = fuzz.trimf(self.risco_projeto.universe, [8, 10, 10])
        
        # Definição das regras fuzzy
        self.regras = [
            ctrl.Rule(
                self.experiencia['baixo'] & self.complexidade['baixo'] & 
                self.estabilidade_requisitos['baixo'] & self.maturidade_tecnologica['baixo'],
                self.risco_projeto['muito_baixo']
            ),
            ctrl.Rule(
                self.experiencia['medio'] | self.complexidade['medio'] | 
                self.estabilidade_requisitos['medio'],
                self.risco_projeto['baixo']
            ),
            ctrl.Rule(
                self.experiencia['alto'] | self.complexidade['alto'] | 
                self.estabilidade_requisitos['alto'] | 
                self.rotatividade['alto'] | self.interdependencia_modulos['alto'],
                self.risco_projeto['medio']
            ),
            ctrl.Rule(
                (self.complexidade['alto'] & self.experiencia['baixo']) |
                (self.rotatividade['alto'] & self.suporte_gerencia['baixo']) |
                (self.integracao_sistemas['alto'] & self.maturidade_tecnologica['alto']),
                self.risco_projeto['alto']
            ),
            ctrl.Rule(
                self.complexidade['alto'] & self.rotatividade['alto'] & 
                self.estabilidade_requisitos['alto'] & 
                self.maturidade_tecnologica['alto'],
                self.risco_projeto['muito_alto']
            ),
            ctrl.Rule(
                self.tamanho_equipe['alto'] & self.complexidade['alto'], self.risco_projeto['alto']
            ),
            ctrl.Rule(
                self.qualidade_documentacao['baixo'] & self.complexidade['alto'], self.risco_projeto['muito_alto']
            ),
            ctrl.Rule(
                self.recursos_orcamentarios['baixo'] & self.suporte_gerencia['baixo'], self.risco_projeto['alto']
            ),
            ctrl.Rule(
                self.complexidade_requisitos['alto'] & self.estabilidade_requisitos['baixo'], self.risco_projeto['muito_alto']
            )
        ]
        
        self.sistema_controle = ctrl.ControlSystem(self.regras)
        self.simulador = ctrl.ControlSystemSimulation(self.sistema_controle)
    
    def avaliar_risco(self, parametros_projeto):
        for chave, valor in parametros_projeto.items():
            try:
                self.simulador.input[chave] = valor
            except KeyError:
                print(f"entrada não reconhecida: {chave}")
    
    # Após definir todas as entradas, compute o sistema fuzzy
        try:
            self.simulador.compute()
        except ValueError as e:
            print(f"Erro ao calcular o sistema fuzzy: {e}")
            return None  # Ou um valor padrão
    
    # Retorne o resultado, por exemplo, o risco calculado
        return self.simulador.output['risco_projeto']

    
    def classificar_risco(self, valor_risco):
        if valor_risco <= 2:
            return "Muito Baixo"
        elif valor_risco <= 4:
            return "Baixo"
        elif valor_risco <= 6:
            return "Médio"
        elif valor_risco <= 8:
            return "Alto"
        else:
            return "Muito Alto"
    
    def plotar_funcoes_pertinencia(self):
        variaveis_entrada = [
            (self.experiencia, 'experiencia'),
            (self.complexidade, 'complexidade'),
            (self.estabilidade_requisitos, 'estabilidade_requisitos'),
            (self.maturidade_tecnologica, 'maturidade_tecnologica'),
            (self.tamanho_equipe, 'tamanho_equipe'),
            (self.rotatividade, 'rotatividade'),
            (self.qualidade_documentacao, 'qualidade_documentacao'),
            (self.interdependencia_modulos, 'interdependencia_modulos'),
            (self.recursos_orcamentarios, 'recursos_orcamentarios'),
            (self.suporte_gerencia, 'suporte_gerencia'),
            (self.complexidade_requisitos, 'complexidade_requisitos'),
            (self.integracao_sistemas, 'integracao_sistemas')
        ]
        
        fig, axes = plt.subplots(4, 3, figsize=(10, 12))
        axes = axes.ravel()
        
        for i, (variavel, titulo) in enumerate(variaveis_entrada):
            axes[i].plot(variavel.universe, variavel['baixo'].mf, 'b', label='Baixo')
            axes[i].plot(variavel.universe, variavel['medio'].mf, 'g', label='Médio')
            axes[i].plot(variavel.universe, variavel['alto'].mf, 'r', label='Alto')
            
            axes[i].set_title(titulo)
            axes[i].set_xlabel('Valor')
            axes[i].set_ylabel('Grau de Pertinência')
            axes[i].legend()
            axes[i].grid(True)
        
        plt.tight_layout()
        plt.show()
    
    def plotar_saida_risco(self):
        plt.figure(figsize=(10, 6))
        
        plt.plot(self.risco_projeto.universe, self.risco_projeto['muito_baixo'].mf, label='Muito Baixo')
        plt.plot(self.risco_projeto.universe, self.risco_projeto['baixo'].mf, label='Baixo')
        plt.plot(self.risco_projeto.universe, self.risco_projeto['medio'].mf, label='Médio')
        plt.plot(self.risco_projeto.universe, self.risco_projeto['alto'].mf, label='Alto')
        plt.plot(self.risco_projeto.universe, self.risco_projeto['muito_alto'].mf, label='Muito Alto')
        
        plt.title('Funções de Pertinência - Risco do Projeto')
        plt.xlabel('Risco')
        plt.ylabel('Grau de Pertinência')
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()

def main():
    avaliador = ProjetoRiscoFuzzy()
    
    # Plotar funções de pertinência
    avaliador.plotar_funcoes_pertinencia()
    avaliador.plotar_saida_risco()
    
    # Exemplo de avaliação de risco de um projeto
    parametros_projeto = {
        'experiencia': 5,
        'complexidade': 7,
        'estabilidade_requisitos': 6,
        'maturidade_tecnologica': 8,
        'tamanho_equipe': 10,
        'rotatividade': 3,
        'qualidade_documentacao': 4,
        'interdependencia_modulos': 5,
        'recursos_orcamentarios': 9,
        'suporte_gerencia': 7,
        'complexidade_requisitos': 6,
        'integracao_sistemas': 8
}
    
    # Calcular risco
    risco = avaliador.avaliar_risco(parametros_projeto)
    classificacao = avaliador.classificar_risco(risco)
    
    print(f"Risco calculado: {risco:.2f}")
    print(f"Classificação do Risco: {classificacao}")

if __name__ == "__main__":
    main()