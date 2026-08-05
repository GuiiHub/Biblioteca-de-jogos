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

# 2. Inicialização do Estado da Aplicação (Cache na Sessão)
if "usuario" not in st.session_state:
    ps5 = Plataforma("PS5", "Sony")
    steam = Plataforma("Steam", "Valve")
    xbox = Plataforma("Xbox", "Microsoft")

    lucas = Usuario("Lucas Mendes", "lucasgamer", "lucas@email.com")

    # Jogos iniciais de exemplo [source: 1]
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

# 4. Painel de Métricas
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total de Jogos", len(lib))
col2.metric("Horas Jogadas (Recursivo)", f"{lib.total_horas():.0f}h")
col3.metric("Média por Jogo", f"{lib.media_horas():.1f}h")
mais_jogado = lib.jogo_mais_jogado()
col4.metric(
    "Jogo Mais Jogado", 
    mais_jogado.titulo if mais_jogado else "-", 
    f"{mais_jogado.horas_jogadas:.0f}h" if mais_jogado else ""
)

st.markdown("---")

# 5. FORMULÁRIO INTERATIVO: ADICIONAR NOVO JOGO
with st.expander("➕ Adicionar Novo Jogo à Biblioteca", expanded=False):
    with st.form("form_novo_jogo", clear_on_submit=True):
        st.subheader("Cadastrar Jogo")
        col_f1, col_f2 = st.columns(2)

        with col_f1:
            titulo = st.text_input("Título do Jogo*")
            genero = st.text_input("Gênero* (ex: RPG, Metroidvania, FPS)")
            plataforma_nome = st.selectbox(
                "Plataforma", 
                ["Steam", "PS5", "Xbox", "Nintendo Switch", "PC"]
            )
            horas = st.number_input("Horas Jogadas", min_value=0.0, step=1.0)

        with col_f2:
            tipo_jogo = st.radio("Tipo de Jogo", ["Single-player", "Multiplayer"])
            zerado = st.checkbox("Já zerou este jogo?")
            favorito = st.checkbox("Marcar como Favorito ❤️")

            if tipo_jogo == "Single-player":
                campanha = st.number_input("Duração da Campanha (horas)", min_value=0.0, step=1.0)
                runs = st.number_input("Número de Runs (opcional)", min_value=0, step=1)
            else:
                partidas = st.number_input("Número de Partidas Jogadas", min_value=0, step=1)

        st.markdown("---")
        st.caption("Avaliação (Opcional)")
        add_avaliacao = st.checkbox("Adicionar Avaliação / Nota agora?")
        if add_avaliacao:
            col_ev1, col_ev2 = st.columns([1, 3])
            with col_ev1:
                nota = st.slider("Nota", 0.0, 10.0, 8.0, step=0.5)
            with col_ev2:
                comentario = st.text_input("Comentário", "Excelente jogo!")

        btn_salvar = st.form_submit_button("💾 Salvar Jogo na Tabela Hash")

        if btn_salvar:
            if not titulo.strip() or not genero.strip():
                st.error("⚠️ Título e Gênero são obrigatórios!")
            else:
                plat_obj = Plataforma(plataforma_nome, "Fabricante")
                
                if tipo_jogo == "Single-player":
                    novo_jogo = JogoSingle(
                        titulo.strip(), genero.strip(), plat_obj, 
                        horas, campanha, int(runs)
                    )
                else:
                    novo_jogo = JogoMultiplayer(
                        titulo.strip(), genero.strip(), plat_obj, 
                        horas, int(partidas)
                    )

                novo_jogo.zerado = zerado
                novo_jogo.favorito = favorito

                if add_avaliacao:
                    novo_jogo.avaliar(Avaliacao(nota, comentario))

                # Insere na Tabela Hash em O(1)
                sucesso = lib.adicionar_jogo(novo_jogo)
                if sucesso:
                    st.success(f"✅ Jogo **'{titulo}'** adicionado com sucesso!")
                    st.rerun()  # Atualiza a interface instantaneamente
                else:
                    st.error(f"❌ O jogo **'{titulo}'** já existe na sua biblioteca!")

st.markdown("---")

# 6. FILTROS & BUSCA EM TABELA HASH
st.sidebar.header("🔍 Filtros & Busca em Hash")

filtro_status = st.sidebar.selectbox(
    "Filtrar por Status",
    ["Todos", "Zerados", "Em Andamento", "Favoritos"]
)

generos = ["Todos"] + lib.generos_disponiveis()
filtro_genero = st.sidebar.selectbox("Buscar em Hash por Gênero O(1)", generos)
termo_busca = st.sidebar.text_input("Busca Parcial em Gênero", "")

# Aplicar Filtros
if filtro_status == "Zerados":
    jogos_exibicao = lib.listar_zerados()
elif filtro_status == "Em Andamento":
    jogos_exibicao = lib.listar_em_andamento()
elif filtro_status == "Favoritos":
    jogos_exibicao = lib.listar_favoritos()
else:
    jogos_exibicao = lib.jogos

if filtro_genero != "Todos":
    jogos_filtrados_genero = lib.buscar_por_genero(filtro_genero)
    jogos_exibicao = [j for j in jogos_exibicao if j in jogos_filtrados_genero]

if termo_busca:
    jogos_parciais = lib.buscar_por_genero_parcial(termo_busca)
    jogos_exibicao = [j for j in jogos_exibicao if j in jogos_parciais]


# 7. LISTAGEM DOS CARDS + BOTÃO DE REMOÇÃO
st.subheader(f"📚 Catálogo ({len(jogos_exibicao)} jogos)")

if not jogos_exibicao:
    st.info("Nenhum jogo encontrado.")
else:
    for jogo in jogos_exibicao:
        with st.container(border=True):
            col_header1, col_header2 = st.columns([3, 1])
            
            fav = " ❤️" if jogo.favorito else ""
            status_badge = "✅ Zerado" if jogo.zerado else "⚠️ Em andamento"
            
            with col_header1:
                st.markdown(f"### {jogo.titulo}{fav}")
                st.caption(f"**{jogo.genero}** • {jogo.tipo()} • 🖥️ {jogo.plataforma.nome}")
            
            with col_header2:
                st.markdown(f"**Status:** {status_badge}")
                st.markdown(f"**Tempo:** `{jogo.horas_jogadas:.0f}h`")
                
                # BOTÃO DE EXCLUIR O JOGO
                if st.button("🗑️ Excluir", key=f"del_{jogo.titulo}"):
                    # Remove da Tabela Hash da Biblioteca em O(1)
                    lib.remover_jogo(jogo.titulo)
                    st.toast(f"Jogo '{jogo.titulo}' removido!", icon="🗑️")
                    st.rerun()  # Atualiza a interface instantaneamente

            # Detalhes específicos de Single-player ou Multiplayer
            if jogo.tipo() == "Single-player":
                prog = jogo.progresso()
                # A barra sempre será exibida
                st.progress(int(prog) / 100.0, text=f"Progresso da Campanha: **{prog:.1f}%**")
                
                if getattr(jogo, "_runs", 0) > 0:
                    st.caption(f"🔁 **Runs completadas:** {jogo._runs}")
            
            elif jogo.tipo() == "Multiplayer":
                partidas = getattr(jogo, "_partidas", 0)
                st.markdown(f"🎯 **Total de Partidas Jogadas:** `{partidas}`")
            
            # Exibição de Avaliação
            if jogo.avaliacao:
                rec_icon = "👍 Recomendado" if jogo.avaliacao.recomenda else "👎 Não recomendado"
                st.info(
                    f"⭐ **Nota: {jogo.avaliacao.nota:.1f}/10** ({rec_icon})\n\n"
                    f"*\"{jogo.avaliacao.comentario}\"*"
                )