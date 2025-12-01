document.addEventListener("DOMContentLoaded", function () {

    // --- SELETORES GERAIS ---
    // Container onde os cartões dos animais serão renderizados
    const containerGaleria = document.getElementById("conteiner-galeria")
    // Botões para filtrar a lista por espécie (Todos, Cães, Gatos)
    const botoesFiltro = document.querySelectorAll(".botao-filtro")

    // Configuração da URL base da API
    // Ajuste aqui caso o endereço do servidor backend mude
    const urlApi = "http://localhost:8000/animais/"
    const origemApi = new URL(urlApi).origin

    // --- FUNÇÕES AUXILIARES ---

    /**
     * Resolve o caminho completo da imagem do animal
     * Se não houver foto, retorna uma imagem placeholder padrão
     * Trata caminhos relativos e absolutos
     */
    const resolverFoto = (valor) => {
        if (!valor || typeof valor !== "string") {
            return `${origemApi}/img/placeholder.jpg`
        }
        let caminhoFoto = valor.trim()
        
        // Se já for uma URL completa (http/https), retorna ela mesma
        if (caminhoFoto.startsWith("http://") || caminhoFoto.startsWith("https://")) {
            return caminhoFoto
        }
        
        // Normaliza o caminho relativo removendo barras iniciais duplicadas
        if (caminhoFoto.startsWith("/static/uploads") || caminhoFoto.startsWith("static/uploads")) {
            return `${origemApi}/${caminhoFoto.replace(/^\/+/, "")}`
        }
        
        // Padrão: adiciona o prefixo da pasta de uploads
        return `${origemApi}/static/uploads/${caminhoFoto.replace(/^\/+/, "")}`
    }

    /**
     * Formata a idade em meses para uma string legível (Anos e Meses)
     * Exemplo: 14 meses -> "1 ano e 2 meses"
     */
    function formatarIdade(mesesTotal) {
        // Se for menos de 1 ano, exibe apenas os meses
        if (mesesTotal < 12) {
            return `${mesesTotal} meses`
        }

        const anos = Math.floor(mesesTotal / 12)
        const meses = mesesTotal % 12

        const textoAnos = anos === 1 ? "1 ano" : `${anos} anos`

        // Se a divisão for exata (ex: 24 meses), exibe apenas os anos
        if (meses === 0) {
            return textoAnos
        }

        const textoMeses = meses === 1 ? "1 mês" : `${meses} meses`

        return `${textoAnos} e ${textoMeses}`
    }

    // --- FUNÇÕES DA GALERIA (COM ANIMAÇÃO DE FILTRO) ---

    /**
     * Busca os dados dos animais na API e atualiza a galeria
     * Aceita um parâmetro opcional 'especie' para filtragem
     */
    async function buscarAnimais(especie = "") {
        // Inicia a animação de saída (Fade-Out)
        if (containerGaleria) {
            containerGaleria.classList.add("escondido")
        }

        // Aguarda 300ms para a animação CSS completar antes de trocar os dados
        setTimeout(async () => {
            try {
                // Constrói a URL com o filtro de query string, se houver
                let urlCompleta = urlApi
                if (especie) {
                    urlCompleta += `?especie_filter=${especie}`
                }

                const resposta = await fetch(urlCompleta)
                if (!resposta.ok) {
                    throw new Error(`Status: ${resposta.status}`)
                }
                const animais = await resposta.json()

                // Renderiza os novos cartões
                renderizarAnimais(animais)

            } catch (erro) {
                console.error("Erro ao buscar:", erro)
                if (containerGaleria) {
                    containerGaleria.innerHTML = "<p>Erro ao carregar animais.</p>"
                }
            } finally {
                // Inicia a animação de entrada (Fade-In)
                if (containerGaleria) {
                    containerGaleria.classList.remove("escondido")
                }
            }
        }, 300)
    }

    /**
     * Gera o HTML dos cartões de animais e insere no DOM
     */
    function renderizarAnimais(animais) {
        if (!containerGaleria) return

        containerGaleria.innerHTML = ""

        // Exibe mensagem caso o filtro não retorne resultados
        if (animais.length === 0) {
            containerGaleria.innerHTML = "<p style='grid-column: 1/-1;'>Nenhum animal encontrado nesta categoria.</p>"
            return
        }

        // Dicionário para formatar o sexo (banco -> visual)
        const mapSexo = { "femea": "Fêmea", "macho": "Macho" }

        animais.forEach(animal => {
            const cartao = document.createElement("div")
            cartao.className = "cartao-animal"

            const sexoFormatado = mapSexo[animal.sexo] || animal.sexo
            const idadeTexto = formatarIdade(animal.idade_meses)

            // Construção do HTML do cartão
            let conteudoHtml = `
                <div class="imagem-cartao-animal">
                    <img src="${resolverFoto(animal.foto)}" alt="Foto de ${animal.nome}" onerror="this.onerror=null;this.src='${origemApi}/img/placeholder.jpg';">
                </div>
                <div class="conteudo-cartao-animal">
                    <h3>${animal.nome}</h3>
                    <p><strong>Espécie:</strong> <span style="text-transform: capitalize;">${animal.especie}</span></p>
                    <p><strong>Sexo:</strong> ${sexoFormatado}</p>
                    <p><strong>Idade:</strong> ${idadeTexto}</p>
                    <a href="formulario.html?animal_id=${animal.id}" class="botao-cartao-animal">Quero Adotar</a>
                </div>
            `
            cartao.innerHTML = conteudoHtml
            containerGaleria.appendChild(cartao)
        })
    }

    // --- INICIALIZAÇÃO ---

    // Verifica se estamos na página que contém a galeria
    if (containerGaleria) {
        // Carregamento inicial sem filtros
        buscarAnimais("")

        // Adiciona eventos de clique aos botões de filtro
        if (botoesFiltro) {
            botoesFiltro.forEach(btn => {
                btn.addEventListener("click", (e) => {
                    // Gerencia a classe 'ativo' para estilo visual
                    botoesFiltro.forEach(b => b.classList.remove("ativo"))
                    e.target.classList.add("ativo")

                    // Determina o filtro com base no texto do botão
                    let filtro = ""
                    const texto = e.target.textContent.toLowerCase()
                    if (texto.includes("cães") || texto.includes("cachorro")) filtro = "cachorro"
                    if (texto.includes("gatos") || texto.includes("gato")) filtro = "gato"

                    // Dispara a busca com o novo filtro
                    buscarAnimais(filtro)
                })
            })
        }
    }
})