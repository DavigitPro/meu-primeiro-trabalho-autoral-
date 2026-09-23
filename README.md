Darcy Organizado

Trabalho autoral desenvolvido para a disciplina do professor Moisés.

Sobre o projeto

O Darcy Organizado é um sistema de gerenciamento escolar feito em Python, que reúne em um só lugar duas necessidades comuns dos alunos: consultar e reservar livros da biblioteca, e consultar e solicitar uniformes escolares.

A ideia surgiu porque, na minha escola, essas duas coisas (biblioteca e uniforme) são bem desorganizadas e feitas de forma manual. Então pensei em criar um sistema simples, com interface visual, que facilitasse esse processo tanto para o aluno quanto para a administração.

 Funcionalidades

- Login de usuários, com dois níveis de acesso: Aluno e Administrador
- Biblioteca
  - Consulta de livros por título, autor ou categoria
  - Reserva de livros com controle automático de exemplares disponíveis
  - Histórico de reservas do aluno
- Uniformes
  - Consulta de peças por tipo e tamanho
  - Solicitação de uniforme com seleção de quantidade
  - Histórico de solicitações do aluno
- Painel administrativo
  - Visão geral do sistema (quantidade de alunos, livros e reservas)
  - Acesso rápido à biblioteca e ao estoque de uniformes

 Tecnologias utilizadas

- Python 3.14
- Tkinter e CustomTkinter — para a interface gráfica
- SQLite3 — para o banco de dados local

 Como executar

1. Clone o repositório:
   ```bash
   git clone https://github.com/DavigitPro/meu-primeiro-trabalho-autoral-.git
   ```
2. Instale a dependência do CustomTkinter:
   ```bash
   pip install customtkinter
   ```
3. Execute o arquivo principal:
   ```bash
   python "Darci organizado.py"
   ```

O banco de dados (`darcy_organizado.db`) é criado automaticamente na primeira execução, já com alguns livros e uniformes de exemplo cadastrados.

## Usuários de teste

| Perfil | Usuário | Senha |
|--------|---------|-------|
| Aluno | `aluno` | `1234` |
| Administrador | `admin` | `admin123` |

## O que aprendi fazendo esse trabalho

Foi meu primeiro projeto usando banco de dados junto com interface gráfica. Aprendi a estruturar tabelas relacionadas no SQLite (usuários, livros, reservas, uniformes e solicitações), a manipular o CustomTkinter para deixar a tela mais bonita e organizada, e também a pensar na experiência do usuário — por exemplo, avisando quando um livro não tem exemplar disponível ou quando o aluno já reservou aquele mesmo item.

## Autor

Feito por DavigitPro 
