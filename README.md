# IBPM CR - Aplicativo Oficial da Igreja ⛪📱

Aplicativo oficial da Igreja Batista do Povo em Monte Castelo / Região (IBPMCR), desenvolvido 100% em Python com Flet (motor Flutter).

## 🎯 Visão do Projeto
O aplicativo conecta a congregação às atividades da igreja, servindo como hub para:
1. **Feed de Mensagens e Cortes Virais**: Integrado diretamente ao `ibpmcr-automation-system`.
2. **Devocionais Inteligentes**: Resumos semanais das pregações gerados por IA.
3. **Agenda & Eventos**: Cultos, eventos, encontros de jovens, retiros e conferências.
4. **Mural de Oração & Células**: Comunidade conectada e suporte aos membros.
5. **Contribuições**: Dízimos e ofertas facilitados via chave PIX copia e cola.

## 🛠️ Stack Tecnológica
- **Linguagem**: Python 3.11+
- **Framework Mobile/UI**: [Flet](https://flet.dev/) (Material Design 3 / Flutter Engine)
- **Backend / Database**: FastAPI / Supabase (PostgreSQL + Auth + Storage)
- **Integração**: Consome os dados e cortes do ecossistema `ibpmcr-automation-system`

## 📂 Estrutura Inicial
```text
ibpmcr-app/
├── assets/          # Ícones, logo e imagens
├── src/
│   ├── components/  # Cards, botões e widgets reutilizáveis
│   ├── views/       # Telas do app (Home, Vídeos, Eventos, Oração, Perfil)
│   ├── services/    # Conexão com banco e API
│   └── main.py      # Ponto de entrada da aplicação Flet
├── .gitignore
├── requirements.txt
└── README.md
```
