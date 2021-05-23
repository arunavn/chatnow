var api_base_url = getCookie('api_base_url');
window.onload = function(){
    let image =  document.getElementById('profilePicture');
    loadProfileImage(image);
    console.log("hey")
  
}

function updateDisplayArea(){
    let image =  document.getElementById('profileImage');
    let newProfilePic = document.getElementById('newProfilePic');
    let file = newProfilePic.files[0];
    let url = URL.createObjectURL(file); 
    image.src = url
    //imageDiv.innerHTML = '<img src= "'+ url + '" class="rounded-circle" width="100%">';

}

function populateImageModal(){
    let image =  document.getElementById('profileImage');
    loadProfileImage(image); 
}

function onImageUpload(){
    uploadProfilePicture()
}


async function loadProfileImage(image) {
  const options = {
    method: 'get',
    credentials: 'same-origin',
    origin: 'http://127.0.0.1:8000',
    headers: {
      'X-CSRF-TOKEN': getCookie('csrf_access_token'),
    },
  };
  var requestedUser = (window.location.href).split('/')[(window.location.href).split('/').length - 1];
  let versionString = String(Math.random ())
  let apiUrl = (window.location.href).split('://')[(window.location.href).split('://').length - 1]
  let proto = (window.location.href).split('://')[0]
  apiUrl = proto + '://' + (apiUrl).split('/')[0]
  apiUrl =  apiUrl + '/api/profilepic/' + requestedUser + '?version=' + versionString;
  const response = await fetch(apiUrl, options);

  if (!response.ok) {
    console.log(response.json())
    const message = `An error has occured: ${response.status}`;
    throw new Error(message);
  }

  const imageBlob = await response.blob();
  if (response.ok) {
        let url = URL.createObjectURL(imageBlob); 
        image.src = url;

}

}

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

async function uploadProfilePicture() {     
    let User = (window.location.href).split('/')[(window.location.href).split('/').length - 1];
    let apiUrl= api_base_url + '/accounts/profilepic/' + User
    let data = new FormData()
    let newProfilePic = document.getElementById('newProfilePic');
    let file = newProfilePic.files[0];
    data.append('file', file)
    const options = {
        method: 'patch',
        credentials: 'include',
        origin: 'http://127.0.0.1:8000',
        body: data,
        headers: {
        'X-CSRF-TOKEN': getCookie('csrf_access_token')
        },
    };
    const response = await fetch(apiUrl, options);

    if (!response.ok) {
        const message = `An error has occured: ${response.status}`;
        throw new Error(message);
    }

    if (response.ok) {
        let detailsurl= '/details/' + User;
        window.location = detailsurl;

     }
        
    
}



