var api_base_url = getCookie('api_base_url');
window.onload = function(){
    var filterString = (window.location.href).split('/')[(window.location.href).split('/').length - 1];
    filterString = decodeURIComponent(filterString)
    document.getElementById('filterString').value = filterString
    loadPeople()
}
async function loadPeople() {
  const options = {
    method: 'get',
    credentials: 'include',
    origin: 'http://127.0.0.1:8000',
    headers: {
      'X-CSRF-TOKEN': getCookie('csrf_access_token'),
    },
  };
  var filterString = document.getElementById('filterString').value;
  let apiUrl = (window.location.href).split('://')[(window.location.href).split('://').length - 1]
  let proto = (window.location.href).split('://')[0]
  apiUrl = proto + '://' + (apiUrl).split('/')[0]
  apiUrl=  apiUrl + '/api/people?filterstring=' + filterString;
  const response = await fetch(apiUrl, options);

  if (!response.ok) {
    const message = `An error has occured: ${response.status}`;
    throw new Error(message);
  }

  const chats = await response.json();
  if (response.ok) {
    var peopleDiv = document.getElementById('peopleArea');
    peopleDiv.innerHTML= ''; 
    for (c of chats) {
      // code block to be executed4
      id_str = 'person_' + c['id'];
      pannelString = '<div id= "';
      pannelString = pannelString + id_str;
      pannelString = pannelString + '" class="panel panel-default"><div class="panel-body" class="person-pannel">';
      pannelString = pannelString +  '<span class= "personName">' + '<h4>'+ c['name'] +'</h4>'+ '<h5>'+ '(' + c['userid'] + ')' + '</h5>' + '</span>';
      pannelString = pannelString + '<span class= "personEmail"">' + c['email'] + '</span>';
      pannelString = pannelString + '</div></div>';
      peopleDiv.innerHTML = peopleDiv.innerHTML + pannelString;
    
    }
    addClick()
  }
  return chats;
}
loadPeople().catch(error => {
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
      let messageurl= '/details/' + this.id.split('_')[1];
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