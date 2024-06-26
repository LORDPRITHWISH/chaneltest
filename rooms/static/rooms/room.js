const roomName = JSON.parse(document.getElementById('json-roomname').textContent)
const UserName = JSON.parse(document.getElementById('json-username').textContent)
const chatArea = document.getElementById('chat-area')
const online = document.getElementById('online')
const locbase = document.getElementById('locbase')
const base = document.getElementById('base')
const members = document.getElementById('members')

chatArea.scrollTop = chatArea.scrollHeight;

const chatSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/'
    + roomName
    + '/'
);

(() => {
    let memwa = members.childNodes
    let not = true
    memwa.forEach((mem) => {
        if (not && mem.textContent === UserName) {
            not = false;
        }
    })
    if (not) {
        console.log('hi ', UserName)
        online.textContent = parseInt(online.textContent) + 1;
        members.innerHTML += `<li><a class="dropdown-item" href="/profile@${UserName}/">${UserName}</a></li>`
    }
})();

chatSocket.onmessage = function (e) {

    console.log('message received');
    const data = JSON.parse(e.data);


    if (data['message']) {
        if (data.username === UserName) {
            bloc = `<div class="p-1"><div class="d-flex justify-content-end">
                        <div class="card text-end text-primary-emphasis " style="background-color: rgb(12, 0, 82); width: max-content; min-width: 15%; max-width: 45%;">
                            <div class="card-header" style="padding: 0.5%;padding-left: 2%;font-size: smaller;">${data.username}</div>
                                <div class="card-body" style="padding: 2%;">
                                    <blockquote class="blockquote mb-0">
                                        <p> ${data.message} </p>
                                        <footer class="blockquote-footer" style="font-size: 50%;">at <cite title="Source Title">${data.time}/cite></footer>
                                    </blockquote>
                                </div>
                            </div>
                        </div>
                    </div>`
        }

        else {

            bloc = `<div class="p-1"><div class="d-flex justify-content-start">
                        <div class="card text-success-emphasis " style="background-color: rgb(0, 47, 85); width: max-content; min-width: 15%; max-width: 45%;">
                            <div class="card-header"style="padding: 0.5%;padding-left: 2%;font-size: smaller;">${data.username}</div>
                                <div class="card-body"style="padding: 2%;">
                                    <blockquote class="blockquote mb-0">
                                        <p> ${data.message} </p>
                                        <footer class="blockquote-footer" style="font-size: 50%;"">at <cite title="Source Title">${data.time}</cite></footer>
                                    </blockquote>
                                </div>
                            </div>
                        </div>
                    </div>`
        }
        document.getElementById('chat-area').innerHTML += bloc;
        if (UserName === data.username)
            chatArea.scrollTop = chatArea.scrollHeight;
    }
    if (data['newuser']) {
        online.textContent = parseInt(online.textContent) + 1;
        members.innerHTML += `<li><a class="dropdown-item" href="/profile@${data['newuser']}/">${data['newuser']}</a></li>`
        let newDiv = document.createElement('div');
        newDiv.innerHTML += `<div class="alert alert-success" role="alert" style="position: fixed; top: 10%; left: 50%; transform: translateX(-50%);">
                        ${data['newuser']} joined the room</div>`;
        base.appendChild(newDiv)
        setTimeout(() => { newDiv.remove() }, 1000)
    }
    if (data['goneuser']) {
        online.textContent = parseInt(online.textContent) - 1;
        let newDiv = document.createElement('div');
        let memwa = members.childNodes
        memwa.forEach((mem) => {
            if (mem.textContent === data['goneuser']) {
                mem.remove()
            }
        })
        newDiv.innerHTML += `<div class="alert alert-warning" role="alert" style="position: fixed; top: 10%; left: 50%; transform: translateX(-50%);">
                        ${data['goneuser']} left the room</div>`;
        base.appendChild(newDiv)
        setTimeout(() => { newDiv.remove() }, 1000)

    }
};

chatSocket.onclose = function (e) {
    console.log('Chat socket closed ');
};

document.querySelector('#chat-message-submit').onclick = function (e) {
    e.preventDefault();
    const messageInputDom = document.querySelector('#chat-message-input');
    const message = messageInputDom.value;
    chatSocket.send(JSON.stringify({
        'message': message,
        'username': UserName,
        'room': roomName,
        'time': new Date().toLocaleTimeString()
    }));
    messageInputDom.value = '';
    return false;
};











