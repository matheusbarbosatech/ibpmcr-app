# 🏛️ Architecture & Product Decision Log (ADR)
**Registro Histórico de Decisões Estratégicas - IBPM CR App**

---

### ADR-001: Unificação em Flet e Descarte do Streamlit
* **Data:** Setembro de 2026
* **Status:** Aprovado
* **Contexto:** Inicialmente cogitou-se usar Flet para o app mobile e Streamlit para o painel do pastor no desktop.
* **Decisão:** Abandonar o Streamlit e utilizar **100% Flet** para todo o ecossistema.
* **Racional Técnico & de Produto:**
  1. O Flet já é nativamente multiplataforma (roda em Android, iOS e Web responsivo).
  2. O pastor precisa receber alertas e orar na palma da mão no celular, não apenas sentado na frente do computador.
  3. Reduz a manutenção de dois frameworks para um único código limpo com controle de acesso (Roles).

---

### ADR-002: Integração Direta com Supabase (Eliminação da Camada FastAPI no MVP)
* **Data:** Setembro de 2026
* **Status:** Aprovado
* **Contexto:** A proposta inicial incluía uma API intermediária em FastAPI entre o Flet e o banco de dados.
* **Decisão:** Na Fase 1, o Flet se comunicará diretamente com o Supabase via biblioteca oficial `supabase-py`.
* **Racional:** Reduz a complexidade de infraestrutura, custos de hospedagem de servidores e acelera a entrega do MVP sem comprometer a segurança, aproveitando o Row Level Security (RLS) do Supabase.

---

### ADR-003: Corte Radical de Escopo para a Fase 1 (Foco no Refúgio Silencioso)
* **Data:** Setembro de 2026
* **Status:** Aprovado
* **Contexto:** Havia mais de 15 funcionalidades mapeadas nas pesquisas (Kids com QR Code, cifras para banda, LMS, caronas, banco de talentos).
* **Decisão:** Congelar todas as funções secundárias e aprovar apenas o tripé: **Refúgio Silencioso + Cortes de Mensagens + Avisos com Modo Pastoral**.
* **Racional:** Princípio do MVP (Minimum Viable Product). Entregar valor emocional rápido, testar com 10 a 20 membros e validar a retenção real antes de construir módulos complexos.
