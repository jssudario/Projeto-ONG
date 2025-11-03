console.log("TESTE PRA VER SE O JS TA CARREGANDO!!!!");

// espera o html inteiro ser carregado antes de rodar
document.addEventListener("DOMContentLoaded", function() {

    // pego a div lá do html onde os cards vao entrar
    const galleryContainer = document.getElementById("gallery-container");

    // endereço da api (backend) pra buscar os animais
    const apiUrl = "http://localhost:8000/animais/";

    // função principal pra buscar os animais no backend
    async function fetchAnimais() {
        // try -> tentar fazer a conexão
        try {
            // liga pra api e espera a resposta
            const response = await fetch(apiUrl);

            // se a resposta não for ok (erro 404 ou 500), força um erro
            if (!response.ok) {
                throw new Error(`Oops! Erro de rede. status: ${response.status}`);
            }

            // se deu tudo ok pega resposta e transforma em json -> lista de animais
            const animais = await response.json();

            // chama funcao que vai desenhar os cards, mandando a lista de animais pra ela
            renderAnimais(animais);

        // catch -> se o try falhar cai aqui
        } catch (error) {
            // mostra o erro no console pra saber o que deu errado
            console.error("falha ao buscar animais:", error);
            // avisa o usuário na tela que deu erro
            galleryContainer.innerHTML = "<p>Não foi possível carregar os dados. Por favor, tente novamente mais tarde.</p>";
        }
    }

    // função que desenha os cards no html
    function renderAnimais(animais) {
        // limpa a galeria antes de adicionar os cards (pra não duplicar)
        galleryContainer.innerHTML = "";

        // checa se a lista de animais veio vazia
        if (animais.length === 0) {
            // se veio vazia, coloca uma mensagem na tela ->
            galleryContainer.innerHTML = "<p>Nenhum animal disponível para adoção no momento.</p>";
            // -> e para a função aqui
            return;
        }

        // pra cada animal que a api mandou:
        animais.forEach(animal => {
            // 1 -> criar um div novo na memória
            const card = document.createElement("div");
            // 2 -> botar a classe animal-card do css nesse div
            card.className = "animal-card"; 
            // 3 -> montar o html de dentro do card, usando os dados do animal: animal.nome, etc
                card.innerHTML = `
                    <div class="animal-card-image">
                        <img src="images/cachorro-de-rua-pet.jpg" alt="Foto de ${animal.nome}">
                    </div>
                    <div class="animal-card-content">
                        <h3>${animal.nome}</h3>
                        <p><strong>Espécie:</strong> ${animal.especie}</p>
                        <p><strong>Idade:</strong> ${animal.idade_meses} meses</p>
                        <p><strong>Porte:</strong> ${animal.porte}</p>
                        <a href="#" class="animal-card-button">Quero Adotar</a>
                    </div>
                `;

            // 4 -> colocar o card pronto lá pra dentro da gallery-container no html
            galleryContainer.appendChild(card);
        });
    }

    // aqui chama a função principal pra iniciar
    fetchAnimais();

});