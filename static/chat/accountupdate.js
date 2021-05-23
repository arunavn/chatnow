
var api_base_url = getCookie('api_base_url');
window.onload = function(){
    loadDetails()
}
async function loadDetails() {
  const options = {
    method: 'get',
    credentials: 'include',
    origin: 'http://127.0.0.1:8000',
    headers: {
      'X-CSRF-TOKEN': getCookie('csrf_access_token'),
    },
  };
  let apiUrl= api_base_url + '/accounts/user';
  const response = await fetch(apiUrl, options);

  if (!response.ok) {
    const message = `An error has occured: ${response.status}`;
    throw new Error(message);
  }

  const details = await response.json();
  if (response.ok) {
    document.getElementById('name').value = details['name'];
    document.getElementById('phone').value = details['phone'];
    document.getElementById('about').value = details['about'];
  }
  return chats;
}
loadDetails().catch(error => {
  error.message; // 'An error has occurred: 404'
});

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    }