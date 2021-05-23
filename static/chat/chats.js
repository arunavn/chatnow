setInterval(loadChats, 1000)
var api_base_url = getCookie('api_base_url');
async function loadChats() {
  const options = {
    method: 'get',
    credentials: 'same-origin',
    origin: 'http://127.0.0.1:8000',
    headers: {
      'X-CSRF-TOKEN': getCookie('csrf_access_token'),
    },
  };
  var filterString = document.getElementById('filterString').value;
  let apiUrl = (window.location.href).split('://')[(window.location.href).split('://').length - 1]
  let proto = (window.location.href).split('://')[0]
  apiUrl = proto + '://' + (apiUrl).split('/')[0]
  apiUrl= apiUrl + '/api/chats?filterstring=' + filterString;
  const response = await fetch(apiUrl, options);

  if (!response.ok) {
    const message = `An error has occured: ${response.status}`;
    throw new Error(message);
  }

  const chats = await response.json();
  if (response.ok) {
    var chatDiv = document.getElementById('chatArea');
    chatDiv.innerHTML= ''; 
    for (c of chats) {
      // code block to be executed4
      id_str = 'chat_' + c['reciever'];
      pannelString = '<div id= "';
      pannelString = pannelString + id_str;
      pannelString = pannelString + '" class="panel panel-default"><div class="panel-body" class="msg-pannel">';
      pannelString = pannelString +  '<span class= "chatName">' + '<h4>'+ c['othername'] +'</h4>'+ '<h5>'+ '(' + c['otheruserid'] + ')' + '</h5>' + '</span>';
      let sender = 'You';
      if( c['reciever'] == c['lastmessageby'] ){
        sender = c['othername'].split(' ')[0];
      }
      
      if ( (c['lastmessagestatus'] == 'N') && (c['reciever'] == c['lastmessageby']) ){
        pannelString = pannelString + '<span class= "chatMsg">' + '<strong>' + sender + ': ' +c['lastmessage']  + '</strong>' + '</br></span>';
      }
      else{
        pannelString = pannelString + '<span class= "chatMsg">' + sender + ': ' +  c['lastmessage'].slice(0,20) + '..' + '</br></span>';
      }
      pannelString = pannelString + '<span class= "chatUnread"">' + c['unread'] + '</span>';
      pannelString = pannelString + '</div></div>';
      chatDiv.innerHTML = chatDiv.innerHTML + pannelString;
    
    }
    addClick()
  }
  return chats;
}
loadChats().catch(error => {
  error.message; // 'An error has occurred: 404'
});

function addClick(){
  var x= document.querySelectorAll('.panel')
  for ( y of x){
    y.addEventListener('click', actionClick);
  }
  
  
}

function actionClick(e){
  e.preventDefault();
      let messageurl= '/message/' + this.id.split('_')[1];
      window.location = messageurl;
    }

    function getCookie(name) {
      const value = `; ${document.cookie}`;
      const parts = value.split(`; ${name}=`);
      if (parts.length === 2) return parts.pop().split(';').shift();
    }

  function findPeople(){
    let filterString = document.getElementById('filterString').value;
    if (filterString.length <= 0){
      alert("please provide some filter text" )
    }else{
    let messageurl= '/findpeople/' + filterString;
    window.location = messageurl;
    }
  }