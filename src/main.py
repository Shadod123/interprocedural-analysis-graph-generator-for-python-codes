#---------------------------------------------------------------------------------------------------------------
# Autor:      Caio Eduardo Ramos Arães
# Matrícula:  738811
# Disciplina: Compiladores (2024/1)
# Professor:  Pedro Henrique Ramos Costa
# Data:       01/07/2024
# Descrição:  Programa para gerar o grafo da árvore sintática abstrata (AST) e realizar a análise interprocedural 
#             de um código em Python.
#
# OBS: O programa foi testado em um ambiente com Windows 11 e Python 3.11.2 instalado
#
# Instruções: Basta executar o arquivo main.py passando como argumento o arquivo .py que se deseja gerar a AST.
#
# Exemplo:    python main.py code.py
#---------------------------------------------------------------------------------------------------------------

import ast
import sys
from printer.printer import ExprPrinter
from graphviz import Digraph

# Função para armazenar as definições de funções no dicionário func_dict
def store_function_defs(node, func_dict):
    if isinstance(node, ast.FunctionDef):
        func_dict[node.name] = node

    # Itera sobre os filhos do nó
    for child in ast.iter_child_nodes(node):
        store_function_defs(child, func_dict)

# Função para desenhar o grafo da árvore sintática abstrata
def draw_graph(node, parent=None):
    node_name = str(node.__class__.__name__)
    
    # Adiciona o nome do nó ao grafo
    dot.node(str(id(node)), node_name)
    
    # Adiciona as arestas entre os nós
    if parent:
        dot.edge(str(id(parent)), str(id(node)))
        
    # Itera sobre os filhos do nó    
    for child in ast.iter_child_nodes(node):
        draw_graph(child, node)

# Função para desenhar o grafo da AST com análise interprocedural inclusa
def draw_interprocedural_graph(node, parent=None, func_dict=None):
    # Variável global para armazenar o grafo
    global dot
    
    # Cria um novo nó no grafo com o nome do nó atual
    node_name = str(node.__class__.__name__)
    dot.node(str(id(node)), node_name)
    
    # Adiciona as arestas entre os nós
    if parent:
        dot.edge(str(id(parent)), str(id(node)))
    
    # Conecta as chamadas de função (Call) às suas definições (FunctionDef)
    if isinstance(node, ast.Call):
        # Verifica se a chamada é de uma função ou de um método de instância
        if isinstance(node.func, ast.Name):
            func_name = node.func.id
        elif isinstance(node.func, ast.Attribute):
            func_name = node.func.attr
        else:
            func_name = None
        
        # Verifica se a função chamada está no dicionário de funções
        if func_name in func_dict:
            dot.edge(str(id(node)), str(id(func_dict[func_name])), color='green')
    
            # Conecta as constantes (Constant) aos argumentos (arg) dos FunctionDef
            func_def = func_dict[func_name]
            for i, arg in enumerate(node.args):
                if isinstance(arg, ast.Constant) or isinstance(arg, ast.Name):
                    if i < len(func_def.args.args):
                        dot.edge(str(id(arg)), str(id(func_def.args.args[i])), color='red')
    
    # Itera sobre os filhos do nó
    for child in ast.iter_child_nodes(node):
        draw_interprocedural_graph(child, node, func_dict)

# Função para gerar o arquivo .dot e renderizar o grafo em um arquivo .png
def generate_dot_and_png(dot, filename, directory='./results'):
    # Configurações de geração da representação em grafo
    dot.graph_attr['rankdir'] = 'TD'
    dot.node_attr['shape'] = 'square'
    
    # Renderiza a imagem do grafo e salva a representação textual dele em um arquivo .dot
    dot.render(filename=filename, format='png', engine='dot', directory=directory, cleanup=True)
    dot.save(f'{filename}.dot')

if __name__ == '__main__':
    # Verifica se o arquivo foi passado como argumento
    if len(sys.argv) != 2:
        print("Usage: python main.py <path_to_python_file>")
        sys.exit(1)
    
    file_path = sys.argv[1]
        
    # Lê o arquivo e gera a árvore sintática abstrata (AST)
    with open(file_path, 'r') as source:
        tree = ast.parse(source.read())
        
    #printer = ExprPrinter()
    #printer.visit(tree)
    
    # Gera um arquivo de dump da árvore sintática abstrata
    with open('dump.txt', 'w') as dump:
        dump.write(ast.dump(tree, indent=4))
    
    # Grafo representativo da árvore sintática abstrata
    dot = Digraph()
    
    # Desenha o grafo da árvore sintática abstrata
    draw_graph(tree)
    generate_dot_and_png(dot, 'ast')
    
    # Limpa o grafo para o posterior desenho do com análise interprocedural
    dot.clear()
    
    # Dicionário que armazena as funções do código
    func_dict = {}
    
    # Armazena as definições de funções antes de desenhar o grafo
    store_function_defs(tree, func_dict)
    
    # Desenha o grafo da AST com análise interprocedural
    draw_interprocedural_graph(tree, func_dict=func_dict)
    generate_dot_and_png(dot, 'inter')