console.log("TESTE PRA VER SE O JS TA CARREGANDO!!!!");

// Espera o HTML inteiro ser carregado antes de rodar
document.addEventListener("DOMContentLoaded", function() {
    // Div onde fica a galeria de animais para adoção
    const galleryContainer = document.getElementById("gallery-container");
    // Endereço da API
    const apiUrl = "http://localhost:8000/animais/";
    // Função que busca os animais no backend
    async function fetchAnimais() {
        try {
            // Chama a API e aguarda retorno
            const response = await fetch(apiUrl);
            // Erro
            if (!response.ok) {
                throw new Error(`Oops! Erro de rede. status: ${response.status}`);
            }
            // Se está tudo ok pega resposta e transforma em JSON -> lista de animais
            const animais = await response.json();
            // Chama função que vai desenhar os cards
            renderAnimais(animais);
        // catch -> se o try falhar cai aqui
        } catch (error) {
            // Mostra o erro no console pra saber qual o erro
            console.error("falha ao buscar animais:", error);
            // Avisa o usuário na tela que deu erro
            galleryContainer.innerHTML = "<p>Não foi possível carregar os dados. Por favor, tente novamente mais tarde.</p>";
        }
    }
    // Função que desenha os cards no HTML
    function renderAnimais(animais) {
        // Limpa a galeria antes de adicionar os cards (pra não duplicar)
        galleryContainer.innerHTML = "";
        // Checa se a lista de animais veio vazia
        if (animais.length === 0) {
            // Se veio vazia retorna:
            galleryContainer.innerHTML = "<p>Nenhum animal disponível para adoção no momento.</p>";
            return;
        }
        // Para cada animal que a API mandou
        animais.forEach(animal => {
            // Cria um div novo na memória
            const card = document.createElement("div");
            // Coloca a classe animal-card do css nesse div
            card.className = "animal-card"; 
// Monta o HTML dntro do card usando os dados do animal                
let htmlConteudo = `
    <div class="animal-card-image">
        <img src="images/cachorro-de-rua-pet.jpg" alt="Foto de ${animal.nome}">
    </div>
    <div class="animal-card-content">
        <h3>${animal.nome}</h3>
        <p><strong>Espécie:</strong> ${animal.especie}</p>
        <p><strong>Idade:</strong> ${animal.idade_meses} meses</p>
`;
// Só adiciona porte caso seja cachorro (gato não tem porte)
if (animal.especie.toLowerCase() === 'cachorro') {
    htmlConteudo += `<p><strong>Porte:</strong> ${animal.porte}</p>`;
}
// Botão
htmlConteudo += `
        <a href="#" class="animal-card-button">Quero Adotar</a>
    </div>
`;
// Define o HTML final do card
card.innerHTML = htmlConteudo;
            // Coloca o card pronto dentro da gallery-container
            galleryContainer.appendChild(card);
        });
    }
    // Chama a função principal pra iniciar
    fetchAnimais();
});