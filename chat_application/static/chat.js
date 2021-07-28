document.getElementById('message-input').onkeyup = function(e) {
    if (e.keyCode === 13) {
        document.getElementById('message-submit').click();
    }
};

const roomName = document.getElementById('room-name').getAttribute('data-slug')
const user = document.getElementById('message-input').dataset.username
const chatWindow = document.getElementById('message-window')
chatWindow.scrollTop = chatWindow.scrollHeight
const audio = new Audio('https://bigsoundbank.com/UPLOAD/mp3/0128.mp3')


const chatSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/chat/'
    + roomName
    + '/'
)

chatSocket.onmessage = function(event) {
    const data = JSON.parse(event.data);
    if(data.event === 'connect') {
        chatWindow.innerHTML += '<div class="d-flex justify-content-center m-3">\n' +
        '                            <small class="rounded-pill p-1 px-2 border border-primary text-primary">' + data.user + ' присоединился к чату</small>\n' +
        '                        </div>'
        chatWindow.scrollTop = chatWindow.scrollHeight
    } else if(data.event === 'disconnect') {
        chatWindow.innerHTML += '<div class="d-flex justify-content-center m-3">\n' +
        '                            <small class="rounded-pill p-1 px-2 border border-primary text-primary">' + data.user + ' покинул чат</small>\n' +
        '                        </div>'
        chatWindow.scrollTop = chatWindow.scrollHeight
    } else {
        let alignment = ''
        if(data.user === user){
            alignment = 'float-end'
        }
        chatWindow.innerHTML += '<div class="m-3">\n' +
        '                            <div class="rounded-pill p-2 px-3 bg-primary text-white d-inline-block ' + alignment + '">' + data.message + '</div>\n' +
        '                            <div class="clearfix"></div>\n' +
        '                            <div class="d-inline-block ' + alignment + '">\n' +
        '                                <small><i>— <strong class="pe-2">' + data.user + ',</strong></i> <span class="text-muted">' + data.timestamp + '</span></small>\n' +
        '                            </div>\n' +
        '                            <div class="clearfix"></div>\n' +
        '                        </div>'
        chatWindow.scrollTop = chatWindow.scrollHeight
        audio.play()
    }
}


document.getElementById('message-submit').onclick = function(e) {
    const messageInput = document.getElementById('message-input')
    const message = messageInput.value
    if(message !== ''){
        chatSocket.send(JSON.stringify({
        'message': message,
        }));
        messageInput.value = ''
    }
}