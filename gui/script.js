
function getIp(){
    var ipAddress = window.location.hostname;
    return (ipAddress);
}
let tools;

const tools_link_location = `http://${getIp()}:5000/tools_info`
const gate_state_route = `http://${getIp()}:5000/gate_state`


const acessText = document.getElementById('acess-text');

window.onload = loadJSON(tools_link_location)
    .then(data => {
        console.log(data);
        loadTools(data);
        tools = data;
    })
    .catch(error => {
        console.error('Erro ao carregar o JSON:', error);
    });

window.onload = loadJSON(gate_state_route)
    .then(data => {
        fetchGateState()
    })


searchDiv = document.getElementById('search-container');
userPhoto = document.getElementById('user-photo');

    async function fetchGateState() {
        try {
            const response = await fetch(`http://${getIp()}:5000/gate_state`);
            console.log("Requisição feita com sucesso");
            
            const data = await response.json();
            console.log("bb");
    
            if (data.locked_gate == false) {
                acessText.style.display = "block";
                searchDiv.style.display = "none";

                
                const response = await fetch(`http://${getIp()}:5000/user_info`);
                const data = await response.json();
                userPhoto.src =  `images/users/${data.card_id}.png`;  // Aqui você pode modificar para carregar a imagem específica da ferramenta
            } else {
                acessText.style.display = "none";
                searchDiv.style.display = "block";
                userPhoto.src =  `images/users/user-photo.jpg`;  // Aqui você pode modificar para carregar a imagem específica da ferramenta
            }
        } catch (error) {
            console.error("Erro ao buscar o estado do portão:", error);
        }
    }
    
    setInterval(fetchGateState, 300);
        


async function fetchUserInfo() {
    try {
        const response = await fetch(`http://${getIp()}:5000/user_info`);
        const data = await response.json();

        document.getElementById('user-name').textContent = `Nome: ${data.name}`;
        document.getElementById('user-cardid').textContent = `Id: ${data.card_id}`;
        


    } catch (error) {
        console.error('Erro ao buscar os dados:', error);
    }
}
function formatString(str) {
    return str.toLowerCase().replace(/\s+/g, '_');
}

function loadTools(tools, searchQuery = '') {
    var container = document.getElementById('tools-container');
    
    // Limpa o container antes de adicionar os itens
    while (container.firstChild) {
        container.removeChild(container.firstChild);
    }

    // Filtra as ferramentas de acordo com o nome (case insensitive)
    const filteredTools = tools
    .filter(tool => tool.ferramenta.toLowerCase().includes(searchQuery.toLowerCase()))
    .sort((a, b) => a.ferramenta.localeCompare(b.ferramenta));

    // Cria os elementos apenas para as ferramentas filtradas
    filteredTools.forEach(tool => {
        var div = document.createElement('div');
        div.classList.add('tool');
        div.classList.add('glass-transparent');

        var img = document.createElement('img');
        // console.log(`gui/images/tools/${formatString(tool.ferramenta)}.webp`)
        img.src = `images/tools/${formatString(tool.ferramenta)}.webp`;  // Aqui você pode modificar para carregar a imagem específica da ferramenta
        img.id = `${tool.ferramenta}`;

        var toolNameP = document.createElement('p');
        toolNameP.textContent = `${tool.ferramenta}`;

        var toolid = document.createElement('span');
        toolid.textContent = `Localização: ${tool.pessoa}`;

        toolNameP.appendChild(document.createElement('br'));
        toolNameP.appendChild(toolid);

        var availablediv = document.createElement('div');
        availablediv.classList.add('border_available');
        availablediv.classList.add(tool.pessoa == "Armário" ? 'green' : 'red');

        div.appendChild(img);
        div.appendChild(toolNameP);
        div.appendChild(availablediv);

        container.appendChild(div);
    });
}

// Adiciona o evento de filtro na barra de pesquisa
document.getElementById('search-bar').addEventListener('input', function() {
    var searchQuery = this.value;
    loadTools(tools, searchQuery);
});

const popup = document.getElementById('pop_up_div');
const video_source = document.getElementById('video_image');
window.addEventListener('load', function() {
    console.log('All assets are loaded')
    acessText.style.display = "none";
    popup.style.display = "none";
    document.getElementById('video_image').src = `http://${getIp()}:5000/video_feed`;
})

setInterval(fetchUserInfo, 500);


async function loadJSON(url) {
    const response = await fetch(url);
    const jsonData = await response.json();
    return jsonData;
}

const supportButton = document.getElementById('support-button');
supportButton.addEventListener('click',function(){
    popup.style.display = 'block';
});
const exitButton = document.getElementById('exit-button');
exitButton.addEventListener('click',function(){
    popup.style.display = 'none';
});