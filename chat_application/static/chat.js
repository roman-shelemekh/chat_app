document.getElementById('message-input').onkeyup = function(e) {
    if (e.keyCode === 13) {
        document.getElementById('message-submit').click();
    }
};

const roomName = document.getElementById('room-name').getAttribute('data-slug')
const user = document.getElementById('message-input').dataset.username
const chatWindow = document.getElementById('message-window')
chatWindow.scrollTop = chatWindow.scrollHeight

const chatSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/chat/'
    + roomName
    + '/'
)

chatSocket.onmessage = function(event) {
    const data = JSON.parse(event.data);
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
}


document.getElementById('message-submit').onclick = function(e) {
    const messageInput = document.getElementById('message-input')
    const message = messageInput.value
    chatSocket.send(JSON.stringify({
        'message': message,
        'user': user,
        'room_slug': roomName
    }));
    messageInput.value = ''
}