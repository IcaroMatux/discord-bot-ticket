# Soraka Calminha 🍌🦄

Bot de Discord desenvolvido em Python utilizando a biblioteca `discord.py`. O foco principal deste projeto é o gerenciamento automatizado de tickets para serviços como EloBoost, DuoBoost e Coach.

## 📋 Funcionalidades

O bot atua como um facilitador de contato entre clientes e a equipe (Staff/Boosters), manipulando canais e permissões automaticamente.

- **Painel de Tickets Interativo**:
  - Comando `/painel` (Slash Command) para enviar um menu fixo ao canal configurado.
  - **Categorias**: EloBoost 🎮, DuoBoost 👥, Coach 💪.
  
- **Criação e Manipulação de Canais**:
  - Ao abrir um ticket, o bot cria automaticamente um **canal de texto privado**.
  - **Permissões de Acesso**: O canal é configurado para ser visível *apenas* para o criador do ticket, a Staff e os Boosters. Isso garante privacidade e organização.
  - **Nomenclatura**: Os canais seguem o padrão `ticket-nomeuser-categoria` para fácil identificação.

- **Ciclo de Vida do Ticket**:
  - Botão de **Fechar Ticket** disponível dentro do canal de atendimento.
  - Validação de permissão (apenas Staff/Boosters podem encerrar).
  - Exclusão automática do canal após 5 segundos da confirmação.

- **Logs e Monitoramento**:
  - Sistema de logs integrado (`logging`) para monitorar a inicialização, erros de carregamento e ações dos usuários no terminal.

## 📂 Estrutura do Projeto

```text
soraka-calminha/
├── cogs/
│   └── ticket_system.py   # Lógica do sistema (Views, Botões, Criação de Canais)
├── config.py              # Configurações centrais (IDs, Prefixos)
├── main.py                # Arquivo principal (Inicialização e carregamento de Cogs)
├── .env                   # (Não incluído) Variáveis de ambiente sensíveis
└── README.md              # Documentação do projeto
```

## 🚀 Como Rodar Localmente

### Pré-requisitos
- Python 3.8 ou superior.
- Git instalado.

### Instalação

1. **Clone o repositório:**
   ```bash
   git clone <URL_DO_SEU_REPOSITORIO>
   cd soraka-calminha
   ```

2. **Instale as dependências:**
   ```bash
   pip install discord.py python-dotenv
   ```

3. **Configuração:**
   - Crie um arquivo `.env` na raiz e adicione seu token: `DISCORD_TOKEN=seu_token_aqui`.
   - Edite o arquivo `config.py` e insira os IDs corretos do seu servidor (Guild ID, IDs de Cargos, Categoria de Tickets, etc).

4. **Execução:**
   ```bash
   python main.py
```