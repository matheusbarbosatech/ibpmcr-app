-- ==============================================================================
-- SCHEMA OFICIAL DO BANCO DE DADOS SUPABASE - SUPER-APP IBPM CR (VERSÃO 2.0)
-- Totalmente compatível com Supabase Free Tier (PostgreSQL 15+)
-- Execute este script completo no SQL Editor do seu Dashboard Supabase.
-- ==============================================================================

-- Habilitar extensões úteis
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 1. TABELA DE MEMBROS / USUÁRIOS
CREATE TABLE IF NOT EXISTS public.usuarios_membros (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    telefone TEXT UNIQUE,
    nome_completo TEXT NOT NULL,
    email TEXT UNIQUE,
    tipo_usuario TEXT DEFAULT 'membro' CHECK (tipo_usuario IN ('membro', 'visitante', 'lider', 'pastor', 'admin')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL,
    ultimo_acesso TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now())
);

-- 2. TABELA DE DEVOCIONAIS DIÁRIOS (365 DIAS NO ALTAR)
CREATE TABLE IF NOT EXISTS public.devocionais_diarios (
    id SERIAL PRIMARY KEY,
    dia_ano INT UNIQUE NOT NULL, -- 1 a 365
    titulo TEXT NOT NULL,
    livro_biblia TEXT NOT NULL,
    versiculo_chave TEXT NOT NULL,
    texto_versiculo TEXT NOT NULL,
    reflexao_pastoral TEXT NOT NULL,
    oracao_do_dia TEXT NOT NULL,
    desafio_pratico TEXT,
    audio_url TEXT, -- Link do Cloudflare R2
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- 3. TABELA DO ACERVO DE CULTOS & VÍDEOS (16:9 E SHORTS 9:16)
CREATE TABLE IF NOT EXISTS public.acervo_cultos (
    id SERIAL PRIMARY KEY,
    numero_culto INT NOT NULL,
    data_culto DATE NOT NULL,
    tipo_culto TEXT NOT NULL, -- Domingo Família, Quinta Profética, Quarta Doutrina, Santa Ceia
    titulo_pregacao TEXT NOT NULL,
    pastor_ministrante TEXT DEFAULT 'Pastor Presidente',
    video_16_9_url TEXT, -- Link Cloudflare R2 / YouTube
    audio_mp3_url TEXT,  -- Link Cloudflare R2
    duracao_minutos INT,
    resumo_pregacao TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- 4. TABELA DE CORTES VERTICAIS (SHORTS 9:16)
CREATE TABLE IF NOT EXISTS public.cortes_verticais (
    id SERIAL PRIMARY KEY,
    culto_id INT REFERENCES public.acervo_cultos(id) ON DELETE CASCADE,
    titulo_impacto TEXT NOT NULL,
    tema_categoria TEXT, -- Família, Milagres, Oração, Guerra Espiritual
    video_9_16_url TEXT NOT NULL, -- Link Cloudflare R2
    duracao_segundos INT,
    total_compartilhamentos INT DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- 5. TABELA DA SUPER GALERIA DE FOTOS DOS CULTOS
CREATE TABLE IF NOT EXISTS public.galeria_fotos (
    id SERIAL PRIMARY KEY,
    album_nome TEXT NOT NULL, -- Ex: Domingo de Celebração - 06/09/2026
    data_evento DATE NOT NULL,
    categoria TEXT DEFAULT 'Culto', -- Culto, Batismo, Conferência, Vigília
    foto_hd_url TEXT NOT NULL,     -- Foto em alta resolução (Cloudflare R2)
    foto_thumb_url TEXT NOT NULL,  -- Miniatura ultraleve para carregamento instantâneo
    total_downloads INT DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- 6. TABELA DO MURAL SOCIAL DE ORAÇÃO & INTERCESSÃO
CREATE TABLE IF NOT EXISTS public.pedidos_oracao (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    usuario_id UUID REFERENCES public.usuarios_membros(id) ON DELETE SET NULL,
    nome_solicitante TEXT NOT NULL,
    motivo_oracao TEXT NOT NULL, -- Saúde, Família, Causas na Justiça, Libertação
    detalhes_pedido TEXT NOT NULL,
    is_anonimo BOOLEAN DEFAULT false,
    status TEXT DEFAULT 'aprovado' CHECK (status IN ('pendente', 'aprovado', 'atendido', 'arquivado')),
    contador_orando INT DEFAULT 1, -- Quantas pessoas clicaram em "Estou Orando por Você"
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- 7. TABELA DE FRASES PROFÉTICAS & WIDGET DE SENTIMENTOS
CREATE TABLE IF NOT EXISTS public.frases_profeticas (
    id SERIAL PRIMARY KEY,
    frase TEXT NOT NULL,
    sentimento_tag TEXT NOT NULL, -- ansiedade, medo, desanimo, gratidao, fe, vitoria
    referencia_biblica TEXT,
    culto_origem_id INT REFERENCES public.acervo_cultos(id) ON DELETE SET NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- 8. TABELA DE E-BOOKS & LIVROS OFICIAIS DO PASTOR
CREATE TABLE IF NOT EXISTS public.livros_ebooks (
    id SERIAL PRIMARY KEY,
    titulo_livro TEXT NOT NULL,
    subtitulo TEXT,
    capa_url TEXT NOT NULL,
    pdf_url TEXT NOT NULL,
    epub_url TEXT,
    total_capitulos INT DEFAULT 12,
    sinopse TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- 9. TABELA DA ESCOLA DE LÍDERES (52 MÓDULOS)
CREATE TABLE IF NOT EXISTS public.escola_lideres_modulos (
    id SERIAL PRIMARY KEY,
    numero_modulo INT UNIQUE NOT NULL, -- 1 a 52
    titulo_modulo TEXT NOT NULL,
    tema_central TEXT NOT NULL,
    conteudo_apostila TEXT NOT NULL,
    pdf_apostila_url TEXT,
    questoes_quiz JSONB, -- 5 questões de múltipla escolha com gabarito
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- ==============================================================================
-- ÍNDICES PARA VELOCIDADE MÁXIMA (CARREGAMENTO EM < 50ms)
-- ==============================================================================
CREATE INDEX IF NOT EXISTS idx_devocionais_dia ON public.devocionais_diarios(dia_ano);
CREATE INDEX IF NOT EXISTS idx_galeria_data ON public.galeria_fotos(data_evento DESC);
CREATE INDEX IF NOT EXISTS idx_cortes_categoria ON public.cortes_verticais(tema_categoria);
CREATE INDEX IF NOT EXISTS idx_oracao_status ON public.pedidos_oracao(status, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_frases_sentimento ON public.frases_profeticas(sentimento_tag);

-- Habilitar Row Level Security (RLS) para Segurança Pastoral
ALTER TABLE public.usuarios_membros ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.pedidos_oracao ENABLE ROW LEVEL SECURITY;

-- Políticas de Leitura Pública
CREATE POLICY "Leitura pública de devocionais" ON public.devocionais_diarios FOR SELECT USING (true);
CREATE POLICY "Leitura pública de fotos" ON public.galeria_fotos FOR SELECT USING (true);
CREATE POLICY "Leitura pública de vídeos" ON public.acervo_cultos FOR SELECT USING (true);
CREATE POLICY "Leitura pública de cortes" ON public.cortes_verticais FOR SELECT USING (true);
CREATE POLICY "Leitura pública de pedidos aprovados" ON public.pedidos_oracao FOR SELECT USING (status = 'aprovado');
CREATE POLICY "Inserção livre de pedidos de oração" ON public.pedidos_oracao FOR INSERT WITH CHECK (true);
