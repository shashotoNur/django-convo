
window.onload = () =>
{
    window.scrollTo(0, document.body.scrollHeight);
}

const root = document.getElementById('root');
const user = document.getElementById('user').value;
const lastPage = parseInt(document.getElementById('last-page').value);
const onPage = parseInt(document.getElementById('prev-page').value) + 1;
const spaceDiv = document.getElementById('space-div');

const speechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
const recognition = new speechRecognition();
const speechSynthesis = window.speechSynthesis;

const theForm = document.getElementById('form');
const switchBtn = document.getElementById('switchBtn');
const speakBtn = document.getElementById('speakBtn');
const chatHolder = document.getElementById('chat-holder');

var endpoint = 'ws://' + window.location.host + window.location.pathname;
var socket = new WebSocket(endpoint);

var recognitionActivated = false;
var checkedForSpeech = false;
var btwMode = false; // btwMode = (too-)busy-to-write-Mode
var nextMsg = '';

var observe;

// functions -------------------------------------------------------------------
theForm.addEventListener('submit', (event) => { event.preventDefault(); });

const insertMsg = (theMsg, theAuthor) =>
{
    var containerDiv = document.createElement('div');
    containerDiv.className = "row";

    var blankDiv = document.createElement('div');
    blankDiv.className = "col-sm";

    var msgDiv = document.createElement('div');

    var msgPara = document.createElement("P");
    msgPara.innerText = theMsg;

    if(user == theAuthor)
    {
        msgPara.className = "card-body text-right";
        msgDiv.className = "card bg-light col-sm m-sm-2 rounded";
        msgDiv.append(msgPara);
        containerDiv.append(blankDiv);
        containerDiv.append(msgDiv);
    }
    else
    {
        msgPara.className = "card-body text-left";
        msgDiv.className = "card text-white bg-dark col-sm m-sm-2 rounded";
        msgDiv.append(msgPara);
        containerDiv.append(msgDiv);
        containerDiv.append(blankDiv);
    }
    chatHolder.append(containerDiv);
}

const switchRecogState = () =>
{
    if(recognitionActivated)
    {
        checkedForSpeech = true;
        stopRecog()
    }
    else
    {
        checkedForSpeech = false;
        startRecog(); 
    }
}

const stopRecog = () =>
{
    recognition.stop();
    recognitionActivated = false;
    speakBtn.value = 'Speak';
}

const startRecog = () =>
{
    if (!recognitionActivated)
    {
        recognition.start();
        recognitionActivated = true;
        speakBtn.value = 'Text';
    }
    if(speechSynthesis.speaking) speechSynthesis.cancel();
}

const endSpeech = (msg) =>
{
    checkedForSpeech = true;
    end = msg.search('stop recognition');
    msg = msg.slice(0, end);
    return msg;
}

const postTheData = () =>
{
    var msgText = root.value;
    var msgObj = { 'message': msgText };

    socket.send(JSON.stringify(msgObj));
    root.value = '';
}

const readText = (msg) =>
{
    if(recognitionActivated) stopRecog();
    var speech = new SpeechSynthesisUtterance();
    speech.text = msg;
    speech.volume = 1; speech.rate = 1; speech.pitch = 1;

    speechSynthesis.speak(speech);

    speech.onend = () =>
    {
        if(nextMsg != '')
        {
            readText(nextMsg);
            nextMsg = '';
        }
        else startRecog();
    }
}

// web socket -----------------------------------------------------------------
socket.onmessage = (event) =>
{
    var chatMsgData = JSON.parse(event.data);
    if(chatMsgData.message)
    {
        var theMsg = chatMsgData.message;
        var theAuthor = chatMsgData.username;

        if(lastPage != onPage)
            window.location.href = `?page=${lastPage}`;
            
        insertMsg(theMsg, theAuthor);
        window.scrollTo(0, document.body.scrollHeight);

        if(btwMode && theAuthor != user)
        {
            if(speechSynthesis.speaking) nextMsg += theMsg;
            else readText(theMsg);
        }
    }
}

socket.onopen = (event) => { console.log('opened', event); }
socket.onerror = (event) => { console.log('error', event); }
socket.onclose = (event) => { console.log('closed', event); }

// speech recognition ---------------------------------------------------------

recognition.onend = () =>
{
    if(checkedForSpeech)
    {
        postTheData();
        recognitionActivated = false;
        speakBtn.value = 'Speak';
    }
    else
    {
        checkedForSpeech = true;
        recognition.start();
    }
};

recognition.onerror = (event) =>
{
    recognitionActivated = false;
    console.log('Speech recognition error detected: ' + event.error);
};

// get text & write in the textarea
recognition.onresult = (event) =>
{
    checkedForSpeech = false;
    const current = event.resultIndex;
    var msg = event.results[current][0].transcript;

    if(msg.includes('switch to text')) switchMode();
    else
    {
        if(msg.includes('stop recognition')) msg = endSpeech(msg);
        root.value += (msg + '\n');
    }
}

const switchMode = () =>
{
    btwMode = !btwMode;
    if(btwMode)
    {
        checkedForSpeech = false;
        startRecog();
        speakBtn.style = "display: block;";
        spaceDiv.style = "display: block;";
        switchBtn.value = 'BTW On';
        switchBtn.className = 'btn btn-danger btn-sm col-sm';
    }
    else
    {
        checkedForSpeech = true;
        stopRecog();
        speakBtn.style = "display: none;";
        spaceDiv.style = "display: none;";
        switchBtn.value = 'BTW Off';
        switchBtn.className = 'btn btn-outline-danger btn-sm col-sm';
    }
}