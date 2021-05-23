var singleTab= 'Y';
var firstLoad = 'Y';
var api_base_url = getCookie('api_base_url');
window.onbeforeunload = function(){
    firstLoad = 'Y';
    //console.log(document.getElementById('messageArea').offsetHeight)
}
window.onload = function(){
    firstLoad = 'Y';
    console.log('i am loading')
    //console.log(document.getElementById('messageArea').offsetHeight)
    document.cookie = 'lastMsg=; expires=Thu, 01 Jan 2000 00:00:00 UTC;';
    let lastMsg = getCookie('lastMsg');
    console.log(lastMsg)
    setInterval(loadMessages, 1000)
} 


async function loadMessages() {
    var messageDiv = document.getElementById('messageArea');
    var topNavDiv = document.getElementById('topNav');
    var bottomNavDiv = document.getElementById('bottomNav');
    padString = String(topNavDiv.offsetHeight + 10) + "px 0px " + String(bottomNavDiv.offsetHeight + 10) + "px 0px";
    messageDiv.style.padding = padString
    validateChatTab()
    if (messageDiv.innerHTML == '' ){
        firstLoad = 'Y'
    }           
    if (singleTab == 'Y'){
        let lastMessageNo  = 'X';
        let lastMsg = getCookie('lastMsg');
        let otherUser = (window.location.href).split('/')[(window.location.href).split('/').length - 1];
        let apiUrl = (window.location.href).split('://')[(window.location.href).split('://').length - 1]
        let proto = (window.location.href).split('://')[0]
        apiUrlBase = proto + '://' + (apiUrl).split('/')[0]
        apiUrl= apiUrlBase + '/api' + '/messages?otheruser='+ otherUser +'&nprev=100';
        let fromMsg= 'X'
        if (messageDiv.innerHTML == '' ){
            firstLoad = 'Y'
            apiUrl= apiUrlBase + '/api' + '/messages?otheruser='+ otherUser +'&nprev=100';
            console.log(apiUrl)
        } else if (lastMsg  && ( lastMsg.split('-')[0] == otherUser )     ){
            fromMsg = String(Number(lastMsg.split('-')[1]) + 1 )
            apiUrl= apiUrlBase + '/api' + '/messages?otheruser='+ otherUser + '&frommsg=' + fromMsg;
        }

        
        const options = {
            method: 'get',
            credentials: 'same-origin',
            origin: 'http://127.0.0.1:8000',
            headers: {
            'X-CSRF-TOKEN': getCookie('csrf_access_token'),
            },
        };
        const response = await fetch(apiUrl, options);

        if (!response.ok) {
            const message = `An error has occured: ${response.status}`;
            throw new Error(message);
        }

        const messages = await response.json();
        if (response.ok) {
            var oldHeight = document.documentElement.scrollHeight
            //console.log(document.documentElement.scrollHeight)
            var newMessages = 0
            for (m of messages) {
                if (m['direction'] == 'R'){
                    messageString = '<div class= "row">\
                    <div class= "col-xs-10">\
                        <div class="msg_cotainer">' + m["message"]+ '<span class="msg_time">8:40 AM, Today</span>\
                        </div>\
                    </div>\
                </div>\
                </br>'
                if (m['status']== 'N'){
                    newMessages = newMessages + 1;
                }
                }
                else{
                    messageString = '   <div class= "row">\
                    <div class= "col-xs-2"></div>\
                    <div class= "col-xs-10">\
                        <div class="msg_cotainer_send">' + m["message"] + '<span class="msg_time_send">8:55 AM, Today</span>\
                        </div>\
                    </div>\
                </div>\
                <div >\
                </br>'
                }
                messageDiv.innerHTML = messageDiv.innerHTML + messageString;
                lastMessageNo = m['id']
            }
            var newHeight = document.documentElement.scrollHeight
            //console.log(document.documentElement.scrollHeight)
            if ( firstLoad == 'N' && newMessages > 0 ){
                document.getElementById('xyz').play();
            }
            pageScroll(newHeight - oldHeight)
            if (lastMessageNo != 'X'){
                document.cookie = 'lastMsg=' +  otherUser + '-'+ lastMessageNo +';';
            }
        }
        firstLoad = 'N';
        return messages;
        
    }
}
loadMessages().catch(error => {
  error.message; // 'An error has occurred: 404'
});

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
  }

function setCookie(cname, cvalue, seconds) {
    var d = new Date();
    d.setTime(d.getTime() + (seconds * 1000));
    var expires = "expires="+ d.toUTCString();
    document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}

function validateChatTab() {
    if (!window.name) {
        window.name = Math.random().toString();
    }

    if (!getCookie('chat_window_id') || window.name == getCookie('chat_window_id')) {
        // This means they are using just one tab. Set/clobber the cookie to prolong the tab's validity.
        setCookie('chat_window_id', window.name, '3');
        singleTab = 'Y'
    } else if (getCookie('chat_window_id') != window.name) {
        // this means another browser tab is open, alert them to close the tabs until there is only one remaining
        var message = 'You cannot chat in multiple tabs. ' +
            'Please close all others and reload. Thanks!';
            var messageDiv = document.getElementById('messageArea');
            messageDiv.innerHTML= message; 
            singleTab= 'N';
            throw new Error(message);
    }
}

function on_input(element, event) {
    var messageDiv = document.getElementById('messageArea');
    var topNavDiv = document.getElementById('topNav');
    var bottomNavDiv = document.getElementById('bottomNav');
    var sHeight = bottomNavDiv.offsetHeight;
    if(event.keyCode === 13){
        //event.preventDefault(); // Ensure it is only this code that runs
        //alert("Enter was pressed was presses");
        on_send();
        //element.value = '';
    }else{
    element.style.height = "5px";
    element.style.height = (element.scrollHeight)+"px";
    }
    padString = String(topNavDiv.offsetHeight + 10) + "px 0px " + String(bottomNavDiv.offsetHeight + 10) + "px 0px";
    messageDiv.style.padding = padString;
    sHeight = bottomNavDiv.offsetHeight - sHeight;
    pageScroll(sHeight);
}

function on_send(){
    var otherUser = (window.location.href).split('/')[(window.location.href).split('/').length - 1];
    msgTmp = document.getElementById('textArea').value
    msg= ''
    for( var i = 0; i < msgTmp.length; i++ ) 
        if( !(msgTmp[i] == '\n' || msgTmp[i] == '\r') )
            msg += msgTmp[i];
    if ( msg != '' ){        
        var msg_load = '[{ "reciever": "' + otherUser + '", "messagetype": "TXT", "message": "' + msg +'" }]';
        sendMessage(msg_load);
    }else{
        document.getElementById('textArea').value = ''   
    }
    document.getElementById('textArea').style.height = '30px';
    return document.getElementById('textArea').focus();
}


function pageScroll(sHeight) {
    console.log(sHeight)
    window.scrollBy(0,sHeight); // horizontal and vertical scroll increments
    //scrolldelay = setTimeout('pageScroll()',100); // scrolls every 100 milliseconds
}


async function sendMessage(msg) {     
    var otherUser = (window.location.href).split('/')[(window.location.href).split('/').length - 1];
    let apiUrl = (window.location.href).split('://')[(window.location.href).split('://').length - 1]
    let proto = (window.location.href).split('://')[0]
    apiUrl = proto + '://' + (apiUrl).split('/')[0]
    apiUrl = apiUrl + '/api'  + '/messages'
    const options = {
        method: 'post',
        credentials: 'include',
        origin: 'http://127.0.0.1:8000',
        body: msg,
        headers: {
        'X-CSRF-TOKEN': getCookie('csrf_access_token'),
        'Content-Type': 'application/json',
        },
    };
    const response = await fetch(apiUrl, options);

    if (!response.ok) {
        const message = `An error has occured: ${response.status}`;
        throw new Error(message);
    }

    const message = await response.json();
    if (response.ok) {
        document.getElementById('textArea').value = '';
        document.getElementById('textArea').style.height = document.getElementById('textArea').scrollHeight ;
    }
    return message;
        
    
}



