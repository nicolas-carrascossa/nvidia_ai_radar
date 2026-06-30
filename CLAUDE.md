# NVIDIA Startup AI Radar

Sistema multi-agente que descobre startups brasileiras de IA, coleta dados públicos sobre elas, diagnostica maturidade técnica e recomenda tecnologias NVIDIA. Projeto da Liga de IA do Inteli, case com a NVIDIA.

Arquitetura final prevista: LangGraph multiagente + RAG com reranking. Este documento descreve o que já está implementado (Fase 1 — Scraping) e o que vem a seguir (Fase 2 — RAG).

---

## Regra de trabalho (importante para qualquer sessão futura)

Antes de escrever qualquer código, leia os arquivos relevantes e confirme o que encontrou. Não assuma comportamento de um arquivo sem ler — várias correções nesse projeto só foram necessárias porque uma sessão anterior assumiu algo sem checar (ex: breaking change do Firecrawl v4, formato de resposta do LLM com code fences). Um passo de cada vez: implemente, rode, mostre o resultado, só então avance.

---

## O que está implementado (Fase 1 — Scraping) — FECHADA

### Arquitetura: Discovery → Filtro → save_discovery → Enrichment guiado por status

```
Discovery (barato, sem LLM pesado)
    ↓
Filtro de sinal de IA (zero custo, string matching)
    ↓
save_discovery() — insere com status='descoberta', ON CONFLICT DO NOTHING
    ↓
get_pending_enrichment() — busca TODAS as startups com status='descoberta'
    (não só as do batch atual — qualquer pendente de qualquer rodada anterior)
    ↓
Enrichment (caro — Firecrawl + LLM, só roda em quem está 'descoberta')
    ↓
update_enrichment_status() — grava resultado + status final
    ('enriquecida' | 'parcial' | 'falhou')
```

A separação existe para controlar custo: descoberta é rápida e barata, enrichment usa LLM e Firecrawl pesado, então só roda em quem já provou ter sinal de IA. A versão final (com `status` explícito) substituiu uma versão anterior que inferia "completo/incompleto" pelo campo `descricao` ser nulo ou não — frágil e sem distinção entre "nunca processado" e "processado mas incompleto". A migração para tabela única com status resolve isso e garante idempotência real: rodar o pipeline duas vezes seguidas não reprocessa quem já tem status terminal (`enriquecida`/`parcial`/`falhou`), validado na prática.

**Resultado final da Fase 1: 64 startups no banco — 27 `enriquecida`, 24 `parcial`, 0 `falhou`** (acumulado em 2 execuções consecutivas do pipeline completo, confirmando idempotência: a segunda rodada só processou startups genuinamente novas, zero reprocessamento das já enriquecidas).

### Infraestrutura

- `config/settings.py` — carrega `.env`, expõe `settings.openai_api_key`, `settings.firecrawl_api_key`, `settings.supabase_url`, `settings.supabase_anon_key`, `settings.supabase_service_role_key`
- `scrapers/base.py` — ABC `BaseScraper` com contrato `scrape(url) -> dict`
- `scrapers/firecrawl_scraper.py` — wrapper do Firecrawl v4.30.4 (breaking change da v1 já corrigido: `search(query, limit=N)` retorna `SearchData.web`; `scrape(url, *, wait_for=None, actions=None)` aceita parâmetros extras para sites com JS/SPA)
- `scrapers/filter.py` — `has_ai_signal(snippet) -> bool`, string matching contra 10 termos (inteligência artificial, machine learning, llm, gpt, etc.), case-insensitive, sem LLM
- `db/supabase_client.py` — `save_discovery()` (insere com status='descoberta', ON CONFLICT DO NOTHING), `get_pending_enrichment()` (busca tudo com status='descoberta'), `update_enrichment_status()` (grava resultado final + status terminal), `normalize_name()`, `update_source_sync()`, `seed_sources()`. Funções antigas removidas: `save_startup()` (upsert genérico) e `check_startup_exists()` (inferia completo/incompleto pelo campo `descricao`) — substituídas pelo modelo de status explícito, ver seção "Deduplicação e idempotência" abaixo.

### Fontes de Discovery implementadas

| Fonte | Arquivo | Tipo | Estratégia |
|---|---|---|---|
| startups.com.br | `scrapers/sources/startups_com_br.py` | notícias | `search()` por query, cada resultado é um artigo individual com `url_origem` específico |
| WOW Aceleradora | `scrapers/sources/wow_aceleradora.py` | portfólio | `scrape()` direto da página de portfólio, LLM extrai lista de empresas do markdown |
| Darwin Startups | `scrapers/sources/darwin_startups.py` | portfólio | mesmo padrão do WOW |
| ACE Ventures | `scrapers/sources/ace_ventures.py` | portfólio | mesmo padrão, com `wait_for=3000` (WordPress com JS) |

**Cubo Itaú foi descartado.** O domínio retorna erro S3 (`NoSuchKey 404`) em `/startups`, `/portfolio` e `/empresas` — problema de infraestrutura do terceiro (site possivelmente migrado/quebrado), não do nosso scraper.

Padrão comum dos scrapers de portfólio: todos têm uma função `_strip_fences()` que remove ` ```json ... ``` ` da resposta do LLM antes do `json.loads()` — o LLM frequentemente envolve o JSON em code fences mesmo quando instruído a não fazer isso.

**Importante:** fontes de portfólio compartilham o mesmo `url_origem` genérico (a página de portfólio inteira) para todas as startups que descobrem — isso teve implicações no enrichment, ver abaixo.

Resultado atual combinado: **103 startups descobertas, 40 passaram no filtro de sinal de IA.**

### Enrichment

`scrapers/enricher.py` — função `enrich(startup) -> dict`, pipeline em 5 etapas:

1. Obter conteúdo de "artigo" sobre a startup (url_origem direto, ou busca em cascata para fontes de portfólio — ver abaixo)
2. LLM extrai `site_oficial` do conteúdo do artigo
3. Validação HTTP (`requests.get`, timeout 8s) — se 404/timeout, `site` vira `None` mas o enrichment continua
4. Scrape do site oficial (se passou na validação)
5. LLM extrai perfil completo combinando artigo + site

`enrich()` não decide mais sozinho se deve pular uma startup — isso é responsabilidade de quem orquestra (só chama `enrich()` em quem está com `status='descoberta'`, via `get_pending_enrichment()`). O retorno sempre inclui um `status` calculado:
- `'falhou'` — sem conteúdo algum para processar (artigo + cascata vazios), ou o LLM do passo 5 lança exceção
- `'parcial'` — passo 5 completou mas faltou pelo menos um de `site`/`descricao`/`setor`
- `'enriquecida'` — os três campos-chave (`site`, `descricao`, `setor`) saíram preenchidos

Erros em cada etapa intermediária (2, 3, 4) são isolados com `logger.error` e não geram `'falhou'` — só resultam em campos `None`, que por sua vez podem levar a `'parcial'`.

**Duas validações críticas dentro do enrichment:**

- **Filtro de domínio cruzado**: depois do LLM extrair um "site oficial", o código checa via `urlparse` se o domínio é o mesmo da fonte de origem. Se for, descarta — evita que o LLM confunda um link interno do artigo/portfólio com o site real da startup (aconteceu com Tako e repetidamente com Darwin, que alucinava `/cart`).
- **Validação HTTP antes do scrape do site**: evita gastar uma chamada de Firecrawl em uma URL que não resolve.

**Busca em cascata (`_search_article_cascade`)** — a peça mais importante do enrichment. Startups vindas de fontes de portfólio (`_PORTFOLIO_SOURCES = {wow_aceleradora, darwin_startups, ace_ventures}`) não têm um artigo individual — o `url_origem` é a página de portfólio genérica, que mistura 70+ empresas no mesmo texto. Usar esse texto direto na etapa 1 fazia o LLM retornar `None` ou alucinar links genéricos.

A cascata resolve isso: para essas fontes, em vez de usar `url_origem`, o sistema faz `search(f"{nome} startup Brasil")`, filtra domínios bloqueados (LinkedIn, YouTube, Instagram, Facebook, X/Twitter), e tenta `scrape()` nos resultados em ordem até achar um com conteúdo útil (> 200 chars). O resultado dessa busca substitui o "conteúdo de artigo" usado na etapa 2.

Isso elevou o enrichment de 0 sites oficiais encontrados (antes da cascata) para 6 em 15 startups testadas (depois). `startups_com_br` não usa a cascata — já tem artigo individual desde o discovery.

### Deduplicação e idempotência (modelo final, com status)

A deduplicação não vive mais dentro de `enrich()` — foi movida para a camada de orquestração (`test_enrichment_batch.py`), o que é mais correto: `enrich()` agora só processa o que recebe, sem decidir se deveria rodar ou não.

- `save_discovery(startup)` — insere com `status='descoberta'`. Usa `ON CONFLICT DO NOTHING` por `(nome, fonte_origem)`: se a startup já existe (em qualquer status), a inserção é ignorada silenciosamente — nunca sobrescreve progresso de enrichment anterior.
- `get_pending_enrichment()` — retorna todas as startups com `status='descoberta'` no banco inteiro, não só as descobertas na rodada atual. Isso é o que dá resiliência a quedas: se o script morrer no meio do batch, rodar de novo retoma exatamente de onde parou, porque só processa quem ainda está pendente.
- `update_enrichment_status(nome, fonte_origem, status, dados)` — grava o resultado final do enrichment, incluindo o status terminal.

A função antiga `check_startup_exists()` (que inferia completo/incompleto pelo campo `descricao`) foi removida e substituída por essa lógica baseada em status explícito.

Validado com duas execuções consecutivas do pipeline completo: a segunda rodada processou apenas startups genuinamente novas (descobertas pela primeira vez nessa execução), zero reprocessamento das que já tinham status terminal.

### Schema da tabela `startups` (Supabase) — atualizado com status

```sql
id                      uuid PK
nome                    text NOT NULL
site                    text nullable
descricao               text nullable
setor                   text nullable
modelo_negocio          text nullable
tecnologias_ia          text[] nullable
tipo_ia                 text nullable
founders                text[] nullable
funding                 text nullable
clientes_mencionados    text[] nullable
fonte_origem            text NOT NULL
url_origem              text NOT NULL
snippet                 text nullable      -- snippet original do discovery, útil pra debug
status                  text NOT NULL DEFAULT 'descoberta'
                        CHECK (status IN ('descoberta','enriquecida','parcial','falhou'))
data_descoberta         timestamptz default now()
data_enrichment         timestamptz nullable
data_coleta             timestamptz default now()
created_at              timestamptz default now()

UNIQUE (nome, fonte_origem)  -- viabiliza upsert/ON CONFLICT DO NOTHING
```

**Regra de status:**
- `'descoberta'` — passou no filtro de IA, ainda não foi processada pelo enrichment
- `'enriquecida'` — `site AND descricao AND setor` todos preenchidos
- `'parcial'` — o enrichment rodou até o fim (LLM retornou perfil), mas faltou pelo menos um dos três campos-chave (geralmente `site`, quando a cascata/validação HTTP/filtro de domínio cruzado não encontrou um site confiável)
- `'falhou'` — não havia conteúdo para processar (artigo + cascata vazios) OU a chamada de LLM do passo final lançou exceção

RLS está desabilitado (advisory do Supabase) — decisão consciente, sem risco enquanto só `service_role_key` for usada server-side. Reavaliar se o frontend algum dia usar `anon_key` direto.

### Tabela `sources` (controle de sincronização)

```sql
id              uuid PK
nome            text NOT NULL UNIQUE
url             text NOT NULL
tipo            text NOT NULL       -- 'noticias' | 'portfolio'
frequencia      text NOT NULL       -- 'continua' | 'mensal'
ultima_sync     timestamptz
ativa           boolean default true
created_at      timestamptz default now()
```

Pensada para diferenciar fontes de carga inicial (portfólios estáticos, não mudam toda semana — sincronizar mensalmente é suficiente) de fontes contínuas (notícias, sempre vale rodar de novo). **A lógica de "só rodar discovery se passou tempo suficiente desde `ultima_sync`" ainda não foi implementada no pipeline** — hoje a tabela só registra a data, mas nada checa essa data antes de decidir se roda. Isso é backlog.

### Scripts de teste existentes

- `test_discovery.py` — testa só `startups_com_br`, não usar como referência de padrão atual (anterior à arquitetura multi-fonte)
- `test_discovery_sources.py` — roda as 4 fontes ativas, aplica filtro, imprime totais por fonte
- `test_enrichment.py` — versão anterior ao modelo de status, mantido por histórico; não reflete mais o fluxo atual
- `test_enrichment_batch.py` — script principal, ponta a ponta: discover nas 4 fontes → filtro de IA → `save_discovery()` de tudo que passou → `get_pending_enrichment()` (pega todas as pendentes do banco, não só do batch atual) → `enrich()` em cada uma → `update_enrichment_status()`. Idempotente: rodar de novo só processa quem ainda está `'descoberta'`. É o script a usar para rodar o pipeline completo de novo no futuro.

---

## Pendências conhecidas (backlog)

- **Volume pode crescer mais**: 64 startups é suficiente para o case, mas novas rodadas de discovery (e novas fontes) continuam alimentando o banco sem retrabalho, graças ao modelo de status.
- **24 startups em status `parcial`**: vale revisão manual eventual para decidir quais merecem reenriquecimento (ex: tentar outra fonte na cascata) e quais ficam como estão — o status dá a informação concreta para essa decisão, mas a decisão em si ainda não foi tomada.
- **`_strip_fences()` duplicado**: existe copiado em `wow_aceleradora.py`, `darwin_startups.py` e `ace_ventures.py`. Deveria estar num utilitário compartilhado (`scrapers/utils.py` ou similar).
- **Tabela `sources` sem lógica de consumo**: `ultima_sync` é gravada mas nada checa essa data para decidir se uma fonte deve rodar de novo.
- **Cubo Itaú**: fonte descartada por bug de infraestrutura do terceiro. Se quiser recuperar volume, vale buscar outra fonte de portfólio.
- **Threshold da cascata (200 chars) é frágil**: caso observado da SprayX, onde um resultado do ResearchGate com 222 chars passou no threshold mas não tinha conteúdo útil sobre a startup — resultou em `parcial`, não quebrou nada, mas é um ponto de atenção sobre qualidade vs quantidade de caracteres.
- **`setor` e `tipo_ia` são texto livre do LLM**: bom para o enrichment, mas vai complicar filtros no entregável 5 (interface) porque "saúde", "Saúde" e "healthtech" são tratados como valores diferentes hoje. Resolver quando chegar na fase de interface — registrado, não bloqueante agora.

## Fase RAG (pasta /rag) — em andamento, paralela à Fase 1

Iniciada numa pasta isolada `/rag`, sem tocar em nada do código de scraping. Estrutura: `/rag/data/raw` (markdown extraído por fonte), `/rag/data/chunks` (chunks com metadados em JSON), `/rag/scripts` (`01_extract.py`, `02_chunk.py`, `03_embed_upload.py`), `sources.py` (lista de URLs NVIDIA com tecnologia associada), `.env.example`, `requirements.txt`.

`sources.py` lista ~19 URLs cobrindo as tecnologias do TAPI (Inception, NIM, NeMo, NeMo Guardrails, Triton, TensorRT-LLM, RAPIDS, cuDF, cuML, CUDA, Riva, Omniverse, Isaac, Clara, Morpheus, AI Enterprise) mais 3 artigos estratégicos (Sequoia, Emergence, blog NVIDIA 5-layer-cake) marcados com tecnologia "Estrategico".

Pipeline planejado: extract (Firecrawl → markdown com front-matter) → chunk (`RecursiveCharacterTextSplitter`, 600 tokens, overlap 100, tiktoken para `text-embedding-3-small`) → embed+upload (OpenAI embeddings → Qdrant Cloud, collection `nvidia_tech_knowledge`, 1536 dims, cosine).

**Pontos de atenção identificados antes da execução, ainda não resolvidos no código:**
- Chunking é por tamanho fixo (`RecursiveCharacterTextSplitter`), não semântico — o TAPI pede chunking semântico explicitamente (seção 5.3). Decisão consciente a ser tomada: manter por tamanho fixo (mais simples, mais robusto) ou implementar chunking semântico de verdade.
- Sem fallback definido para título ausente na extração do Firecrawl (páginas SPA como `build.nvidia.com` podem não retornar `<title>` claro).
- Upload no Qdrant ainda não usa o `id` do chunk como `point_id` — rodar `03_embed_upload.py` duas vezes vai duplicar pontos na collection. Precisa de upsert por id antes de rodar em produção.
- Busca híbrida (vetorial + BM25) e reranking (Cohere) — partes obrigatórias do entregável 3 do TAPI — ainda não têm script. Os 3 scripts atuais cobrem só ingestão; falta a etapa de retrieval.

Os scripts foram criados mas **não executados ainda** — aguardando validação manual passo a passo antes de rodar.

---

## O que a Fase 2 (RAG com reranking) precisa saber

**A Fase 2 é conceitualmente independente de tudo acima.** O RAG não consulta o banco de startups — ele constrói e consulta uma base de conhecimento separada sobre **tecnologias NVIDIA** (NIM, NeMo, NeMo Guardrails, Triton, TensorRT-LLM, RAPIDS, cuDF, cuML, CUDA, Riva, Omniverse, Isaac, Clara, Morpheus, AI Enterprise, NVIDIA Inception — lista completa na seção 5.4/8.2 do documento do case).

Isso significa que a Fase 2 começa do zero em termos de dados: ingestão de documentos (blogs da NVIDIA, documentações oficiais, materiais do case), chunking, embeddings, vector database (Qdrant sugerido, mas ChromaDB/Pinecone/pgvector são aceitos), busca híbrida (vetorial + BM25 lexical) e reranking (Cohere Rerank sugerido).

**Onde as duas fases vão se conectar:** só na fase seguinte (Recommendation Agent), que vai cruzar o perfil de uma startup — vindo do banco que esta fase construiu — com os resultados de uma busca no RAG — vindo da base de conhecimento NVIDIA — para gerar a recomendação técnica final. Até lá, são pipelines paralelas e independentes.

**Reaproveitável da Fase 1 para a Fase 2:**
- `scrapers/firecrawl_scraper.py` — mesmo wrapper serve para coletar conteúdo das páginas oficiais NVIDIA antes da ingestão
- `config/settings.py` — mesma estrutura de configuração, só precisa expor a chave do Cohere (`settings.cohere_api_key`, já mapeada conforme mensagem original do projeto) e do Qdrant
- Padrão de erros isolados com `logger` — manter a mesma filosofia de robustez

**Não reaproveitável / não relevante para a Fase 2:**
- Tudo em `scrapers/sources/` — são scrapers de startups, não de documentação NVIDIA
- `db/supabase_client.py` como está — serve para a tabela `startups`, não para o vector database. Pode precisar de um cliente novo para o Qdrant
- A lógica de deduplicação por nome+fonte — não se aplica a chunks de documentos
