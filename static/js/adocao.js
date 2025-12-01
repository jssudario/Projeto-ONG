document.addEventListener("DOMContentLoaded", () => {

    // --- SELETORES DE ELEMENTOS ---
    const formulario = document.getElementById("form-adocao")
    const botaoEnviar = document.getElementById("botao-enviar")
    const modalSucesso = document.getElementById("modal-sucesso")

    // Elementos de Feedback de Erro
    const alertaErro = document.getElementById("mensagem-erro")
    const detalheErro = document.getElementById("erro-detalhe")

    // Campos de Seleção de Endereço
    const selecaoEstado = document.getElementById("estado")
    const selecaoCidade = document.getElementById("cidade")

    // Elementos de Informação do Animal
    const campoOcultoIdAnimal = document.getElementById('id_animal')
    const caixaInfoAnimal = document.getElementById("caixa-info-animal")
    const imagemInfoAnimal = document.getElementById("img-info-animal")
    const nomeInfoAnimal = document.getElementById("nome-info-animal")

    // --- FUNÇÕES AUXILIARES ---

    /**
     * Formata a mensagem de erro retornada pela API
     * Se for lista de erros de validação, retorna mensagem genérica
     */
    function formatarMensagemErro(erroJson) {
        if (Array.isArray(erroJson.detail)) {
            return "Por favor, preencha todos os campos obrigatórios corretamente."
        }
        return erroJson.detail || "Erro desconhecido no servidor."
    }

    /**
     * Valida se a data de nascimento indica maioridade (18 anos)
     */
    function ehMaiorDeIdade(dataNascimento) {
        if (!dataNascimento) return false
        const dataNasc = new Date(dataNascimento)
        const hoje = new Date()
        const dataMaioridade = new Date(
            hoje.getFullYear() - 18, hoje.getMonth(), hoje.getDate()
        )
        return dataNasc <= dataMaioridade
    }

    /**
     * Carrega a lista de estados da API do IBGE
     * Filtra apenas estados da região Sudeste (ID 3)
     */
    async function carregarEstados() {
        try {
            const resp = await fetch("https://servicodados.ibge.gov.br/api/v1/localidades/regioes/3/estados?orderBy=nome")
            const estados = await resp.json()
            if (selecaoEstado) {
                selecaoEstado.innerHTML = '<option value="">Selecione um estado...</option>'
                estados.forEach(estado => {
                    const opt = document.createElement("option")
                    opt.value = estado.sigla
                    opt.text = estado.nome
                    selecaoEstado.appendChild(opt)
                })
            }
        } catch (e) { console.error("Erro IBGE:", e) }
    }

    /**
     * Carrega a lista de cidades com base no estado selecionado
     */
    async function carregarCidades(uf) {
        if (!uf) return
        selecaoCidade.innerHTML = '<option value="">Carregando...</option>'
        selecaoCidade.disabled = true
        try {
            const resp = await fetch(`https://servicodados.ibge.gov.br/api/v1/localidades/estados/${uf}/municipios`)
            const cidades = await resp.json()
            selecaoCidade.innerHTML = '<option value="">Selecione uma cidade...</option>'
            cidades.forEach(cidade => {
                const opt = document.createElement("option")
                opt.value = cidade.nome
                opt.text = cidade.nome
                selecaoCidade.appendChild(opt)
            })
            selecaoCidade.disabled = false
        } catch (e) { console.error("Erro Cidades:", e) }
    }

    /**
     * Busca os dados do animal selecionado para exibir no topo do formulário
     */
    async function carregarInfoDoAnimal(id) {
        if (!id) return
        try {
            const resp = await fetch(`http://127.0.0.1:8000/animais/${id}`)
            if (!resp.ok) throw new Error("Animal não encontrado")
            const animal = await resp.json()

            nomeInfoAnimal.textContent = animal.nome
            let urlFoto = "http://127.0.0.1:8000/img/placeholder.jpg"
            
            // Tratamento da URL da imagem
            if (animal.foto) {
                urlFoto = animal.foto.startsWith("http")
                    ? animal.foto
                    : `http://127.0.0.1:8000/${animal.foto.replace(/^\/+/, "")}`
            }
            imagemInfoAnimal.src = urlFoto
            caixaInfoAnimal.style.display = "flex"
        } catch (e) { caixaInfoAnimal.style.display = "none" }
    }

    // --- INICIALIZAÇÃO ---

    // Captura o ID do animal da URL (query param)
    const params = new URLSearchParams(window.location.search)
    const idAnimal = params.get('animal_id')

    if (idAnimal && campoOcultoIdAnimal) {
        campoOcultoIdAnimal.value = idAnimal
        carregarInfoDoAnimal(idAnimal)
    } else {
        // Bloqueia o formulário se não houver animal selecionado
        detalheErro.innerText = "(Nenhum animal selecionado)"
        if (alertaErro) alertaErro.style.display = "block"
        if (botaoEnviar) botaoEnviar.disabled = true
    }

    // Inicializa carregamento de endereços
    carregarEstados()
    if (selecaoEstado) selecaoEstado.addEventListener("change", () => carregarCidades(selecaoEstado.value))

    // --- PROCESSAMENTO DO ENVIO DO FORMULÁRIO ---
    if (formulario) {
        formulario.addEventListener("submit", async (e) => {
            e.preventDefault() // Impede o reload padrão da página

            // Bloqueia o botão para evitar múltiplos envios
            botaoEnviar.disabled = true
            botaoEnviar.innerText = "Enviando..."
            if (alertaErro) alertaErro.style.display = "none"

            const formData = new FormData(formulario)

            // Validação de Idade no Frontend
            if (!ehMaiorDeIdade(formData.get("data_nascimento"))) {
                detalheErro.innerText = "(Você deve ser maior de 18 anos)"
                alertaErro.style.display = "block"
                alertaErro.scrollIntoView({ behavior: 'smooth', block: 'center' })

                botaoEnviar.disabled = false
                botaoEnviar.innerText = "Enviar Interesse"
                return
            }

            // Prepara o objeto de dados
            const dadosAdotante = Object.fromEntries(formData.entries())
            // Remove o animal_id pois ele vai para outra tabela
            delete dadosAdotante.animal_id

            try {
                // Passo 1: Cadastrar ou Buscar Adotante
                const respAdotante = await fetch("http://127.0.0.1:8000/adotantes/", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(dadosAdotante)
                })

                if (!respAdotante.ok) {
                    const errJson = await respAdotante.json()
                    throw new Error(formatarMensagemErro(errJson))
                }
                const adotante = await respAdotante.json()

                // Passo 2: Criar Solicitação de Adoção
                const respSol = await fetch("http://127.0.0.1:8000/solicitacoes/", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({
                        animal_id: parseInt(idAnimal),
                        adotante_id: adotante.id
                    })
                })

                if (!respSol.ok) {
                    const errJson = await respSol.json()
                    throw new Error(formatarMensagemErro(errJson))
                }

                // Sucesso: Exibe o modal
                modalSucesso.classList.add("mostrar")
                formulario.reset()

            } catch (erro) {
                console.error(erro)
                detalheErro.innerText = `(${erro.message})`
                alertaErro.style.display = "block"
                alertaErro.scrollIntoView({ behavior: 'smooth', block: 'center' })

                botaoEnviar.disabled = false
                botaoEnviar.innerText = "Enviar Interesse"
            }
        })
    }
})