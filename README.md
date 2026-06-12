# Sistema de Biblioteca de Jogos 🎮
Projeto da disciplina de Princípios de Programação II, utilizando Programação Orientada a Objetos com a linguagem Python.
__________________________________________________________________________________________________________________________________________

## Contexto / Persona
Lucas, 22 anos, gamer casual que tem mais de 80 jogos espalhados em Steam, PS5 e Xbox. Ele nunca sabe o que jogar, esquece quais jogos já zerou e não consegue recomendar nada para os amigos. Quer um sistema para catalogar, avaliar e organizar sua coleção.
__________________________________________________________________________________________________________________________________________

# Classes
```
Jogo                → dados de cada jogo
Plataforma          → Steam, PS5, Xbox...
Avaliacao           → nota e comentário do usuário
Biblioteca          → coleção completa do usuário
Usuario             → dono da biblioteca
````
________________________________________________________________________________________________________________

# Diagrama de classes

'''
Usuario
├── total_usuarios (classe)
├── __nome, __username
├── __biblioteca → Biblioteca
└── exibir_perfil()

Biblioteca
├── __jogos → [Jogo]
├── adicionar/remover_jogo()
├── listar_todos/zerados()
├── buscar_por_genero()
└── media_horas()

Jogo
├── total_jogos (classe)
├── __titulo, __genero, __horas_jogadas, __zerado
├── __plataforma → Plataforma
├── __avaliacao  → Avaliacao
└── exibir()

Plataforma              Avaliacao
├── __nome              ├── __nota
├── __fabricante        ├── __comentario
└── get/set...          └── exibir()
''''''
Usuario
├── total_usuarios (classe)
├── __nome, __username
├── __biblioteca → Biblioteca
└── exibir_perfil()

Biblioteca
├── __jogos → [Jogo]
├── adicionar/remover_jogo()
├── listar_todos/zerados()
├── buscar_por_genero()
└── media_horas()

Jogo
├── total_jogos (classe)
├── __titulo, __genero, __horas_jogadas, __zerado
├── __plataforma → Plataforma
├── __avaliacao  → Avaliacao
└── exibir()

Plataforma              Avaliacao
├── __nome              ├── __nota
├── __fabricante        ├── __comentario
└── get/set...          └── exibir()
'''

