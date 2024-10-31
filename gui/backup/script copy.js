function getIp(){
    var ipAddress = window.location.hostname;
    return (ipAddress);
}
let tools;

window.onload = loadJSON('./tools.json')
    .then(data => {
        console.log(data);
        loadTools(data);
        tools = data;
    })
    .catch(error => {
        console.error('Erro ao carregar o JSON:', error);
    });

async function fetchUserInfo() {
    try {
        const response = await fetch(`http://${getIp()}:5000/user_info`);
        const data = await response.json();

        document.getElementById('user-name').textContent = `Nome: ${data.name}`;
        document.getElementById('user-cardid').textContent = `Idade: ${data.card_id}`;

        if(data.tools !== undefined){
            loadTools(data.tools);
        }


    } catch (error) {
        console.error('Erro ao buscar os dados:', error);
    }
}

function loadTools_saved(tools){
    var container = document.getElementById('tool-cards');

    while(container.firstChild){
        container.removeChild(container.firstChild);
    }

    tools.forEach(tool => {
        
        var div = document.createElement('div');
        div.classList.add('tool-info');

        var img = document.createElement('img');
        img.src = "images/tools/martelo_bola.webp"
        img.id = "user-photo"

        var toolDataDiv = document.createElement('div');
        toolDataDiv.classList.add('user-data');

        var toolNameP = document.createElement('p');
        toolNameP.textContent = `${tool}`;

        toolDataDiv.appendChild(toolNameP);
        div.appendChild(img);
        div.appendChild(toolDataDiv);

        container.appendChild(div);


    });

    setInterval(fetchUserInfo, 500);
}




function loadTools(tools, searchQuery = '') {
    var container = document.getElementById('tools-container');
    
    // Limpa o container antes de adicionar os itens
    while (container.firstChild) {
        container.removeChild(container.firstChild);
    }

    // Filtra as ferramentas de acordo com o nome (case insensitive)
    const filteredTools = tools.filter(tool => 
        tool.name.toLowerCase().includes(searchQuery.toLowerCase())
    );

    // Cria os elementos apenas para as ferramentas filtradas
    filteredTools.forEach(tool => {
        var div = document.createElement('div');
        div.classList.add('tool');
        div.classList.add('glass-transparent');

        var img = document.createElement('img');
        img.src = "images/tools/martelo_bola.webp";  // Aqui você pode modificar para carregar a imagem específica da ferramenta
        img.id = `${tool.name}`;

        var toolNameP = document.createElement('p');
        toolNameP.textContent = `${tool.name}`;

        var toolid = document.createElement('span');
        toolid.textContent = `Localização: ${tool.id}`;

        toolNameP.appendChild(document.createElement('br'));
        toolNameP.appendChild(toolid);

        div.appendChild(img);
        div.appendChild(toolNameP);

        container.appendChild(div);
    });
}

// Adiciona o evento de filtro na barra de pesquisa
document.getElementById('search-bar').addEventListener('input', function() {
    var searchQuery = this.value;
    loadTools(tools, searchQuery);
});

const acessText = document.getElementById('acess-text');
const video_source = document.getElementById('video_image');
window.addEventListener('load', function() {
    console.log('All assets are loaded')
    acessText.style.display = ""
    document.getElementById('video_image').src = `http://${getIp()}:5000/video_feed`;
})

async function loadJSON(url) {
    const response = await fetch(url);
    const jsonData = await response.json();
    return jsonData;
}

