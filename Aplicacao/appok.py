import streamlit as st
from modelo import (
    Plataforma, Avaliacao, JogoSingle, JogoMultiplayer, Usuario
)

# 1. Configuração da Página
st.set_page_config(
    page_title="Biblioteca de Games",
    page_icon="🎮",
    layout="wide"
)

# 2. Inicialização do Estado da Aplicação (Cache/Session Storage)
if "usuario" not in st.session_state:
    ps5 = Plataforma("PS5", "Sony")
    steam = Plataforma("Steam", "Valve")
    xbox = Plataforma("Xbox", "Microsoft")

    lucas = Usuario("Lucas Mendes", "lucasgamer", "lucas@email.com")

    # Cadastrando jogos de exemplo na Tabela Hash da Biblioteca [source: 1]
    j1 = JogoSingle("Hollow Knight", "Metroidvania", steam, 40, 35)
    j1.zerado = True
    j1.favorito = True
    j1.avaliar(Avaliacao(9, "Obra de arte, vale cada centavo."))

    j2 = JogoSingle("God of War", "Ação/Aventura", ps5, 25, 20)
    j2.zerado = True
    j2.avaliar(Avaliacao(10, "Narrativa impecável."))

    j3 = JogoSingle("Hades", "Roguelike", steam, 60, runs=47)
    j3.zerado = True
    j3.favorito = True
    j3.avaliar(Avaliacao(10, "Impossível parar de jogar."))

    j4 = JogoSingle("Resident Evil 4", "Survival Horror", xbox, 15, 16)
    j5 = JogoMultiplayer("Valorant", "FPS Tático", steam, 121, 301)

    for jogo in (j1, j2, j3, j4, j5):
        lucas.biblioteca.adicionar_jogo(jogo)

    st.session_state["usuario"] = lucas

user = st.session_state["usuario"]
lib = user.biblioteca

# 3. Cabeçalho Principal
st.title("🎮 Dashboard do Usuário")
st.text(user.exibir())
st.markdown("---")

# 4. Painel de Métricas (Consumindo Recursão de Soma Total)
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total de Jogos", len(lib))
col2.metric("Horas Jogadas (Soma Recursiva)", f"{lib.total_horas():.0f}h")
col3.metric("Média por Jogo", f"{lib.media_horas():.1f}h")
mais_jogado = lib.jogo_mais_jogado()
col4.metric("Jogo Mais Jogado", mais_jogado.titulo if mais_jogado else "-", f"{mais_jogado.horas_jogadas:.0f}h" if mais_jogado else "")

st.markdown("---")

# 5. Filtros Interativos utilizando as Tabelas Hash
st.sidebar.header("🔍 Filtros & Busca em Tabela Hash")

filtro_status = st.sidebar.selectbox(
    "Filtrar por Status",
    ["Todos", "Zerados", "Em Andamento", "Favoritos"]
)

generos = ["Todos"] + lib.generos_disponiveis()
filtro_genero = st.sidebar.selectbox("Buscar em Hash por Gênero", generos)

termo_busca = st.sidebar.text_input("Busca Parcial em Gênero", "")

# 6. Processamento dos Filtros
if filtro_status == "Zerados":
    jogos_exibicao = lib.listar_zerados()
elif filtro_status == "Em Andamento":
    jogos_exibicao = lib.listar_em_andamento()
elif filtro_status == "Favoritos":
    jogos_exibicao = lib.listar_favoritos()
else:
    jogos_exibicao = lib.jogos

if filtro_genero != "Todos":
    # Busca de ordem constante via índice hash O(1)
    jogos_filtrados_genero = lib.buscar_por_genero(filtro_genero)
    jogos_exibicao = [j for j in jogos_exibicao if j in jogos_filtrados_genero]

if termo_busca:
    jogos_parciais = lib.buscar_por_genero_parcial(termo_busca)
    jogos_exibicao = [j for j in jogos_exibicao if j in jogos_parciais]

# 7. Listagem na Interface (Visual Moderno em Cards)
st.subheader(f"📚 Catálogo ({len(jogos_exibicao)} jogos encontrados)")

if not jogos_exibicao:
    st.warning("Nenhum jogo encontrado com os filtros aplicados.")
else:
    for jogo in jogos_exibicao:
        # Cria um card com borda para cada jogo.
        with st.container(border=True):
            col_header1, col_header2 = st.columns([3, 1])
            
            # Título com ícone de favorito e status
            fav = " ❤️" if jogo.favorito else ""
            status_badge = "✅ Zerado" if jogo.zerado else "⚠️ Em andamento"
            
            with col_header1:
                st.markdown(f"### {jogo.titulo}{fav}")
                st.caption(f"**{jogo.genero}**  •  {jogo.tipo()}  •  🖥️ {jogo.plataforma.nome}")
            
            with col_header2:
                st.markdown(f"**Status:** {status_badge}")
                st.markdown(f"**Tempo:** `{jogo.horas_jogadas:.0f}h jogadas`")
            
            # Informações específicas de Single-player ou Multiplayer.
            if jogo.tipo() == "Single-player":
                prog = jogo.progresso()
                st.progress(int(prog) / 100.0, text=f"Progresso da Campanha: **{prog:.1f}%**")
                if getattr(jogo, "_runs", 0) > 0:
                    st.caption(f"🔁 **Runs completadas:** {jogo._runs}")
            
            elif jogo.tipo() == "Multiplayer":
                partidas = getattr(jogo, "_partidas", 0)
                st.markdown(f"🎯 **Total de Partidas Jogadas:** `{partidas}`")
            
            # Exibição da Avaliação (se existir)
            if jogo.avaliacao:
                rec_icon = "👍 Recomendado" if jogo.avaliacao.recomenda else "👎 Não recomendado"
                st.info(
                    f"⭐ **Nota: {jogo.avaliacao.nota:.1f}/10** ({rec_icon})\n\n"
                    f"*\"{jogo.avaliacao.comentario}\"*"
                )