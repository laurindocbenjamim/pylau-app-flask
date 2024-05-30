// Example starter JavaScript for disabling form submissions if there are invalid fields

const form = document.getElementById('form-register');
//const form2fa = document.getElementById('form-check-2fa');
const divalert = document.querySelector('.alert');
const alertmessage = document.querySelector('.alert p');
alertmessage.style.color = "red";
divalert.style.display = "none";

form.addEventListener("submit", async event => {
    event.preventDefault();

  const data = new FormData(form);

  const password = data.get('password');
  const confirmPassword = data.get('confirm');

  if (password !== confirmPassword) {
    divalert.style.display = "block";
    alertmessage.textContent = "The passwords do not match!";
    return;
  }else{
    divalert.style.display = "none";
    alertmessage.textContent = "";
  }

  //console.log(Array.from(data));
  const baseUrl = window.location.origin;
  
  //alert("base url" +baseUrl);

  try {
    const res = await fetch(
      //baseUrl + '/auth/register',
      baseUrl + '/users/create',
      {
        method: 'POST',
        body: data
      },
    );

    const resData = await res.json();
    
    console.log(resData);
    
    if(resData){
      if(resData[1] == 400){

        console.log(resData[0].object);      
        divalert.style.display = "block";
        alertmessage.textContent = resData[0].message;

      }else if(resData[1] == 200){

        divalert.style.display = "block";
        alertmessage.textContent = resData[0].message;
        setTimeout(() => {
            //window.open(baseUrl + '/' + resData[0].redirectUrl, '_self');
        });

      }
        
    }
  } catch (err) { 
    console.log(resData);
    //alert("Erro ao realizar o cadastro, tente novamente mais tarde " + err.message);
    console.log(err.message);
  }
  
});






function captureUserData() {
  const ipAddress = fetch('https://api.ipify.org?format=json')
    .then(response => response.json())
    .then(data => data.ip)
    .catch(error => {
      console.log('Error fetching IP address:', error);
      return null;
    });

  const macAddress = fetch('https://api.macaddress.io/v1?apiKey=YOUR_API_KEY')
    .then(response => response.json())
    .then(data => data.macAddress)
    .catch(error => {
      console.log('Error fetching MAC address:', error);
      return null;
    });

  const deviceType = navigator.userAgent;

  Promise.all([ipAddress, macAddress])
    .then(([ip, mac]) => {
      console.log('IP Address:', ip);
      console.log('MAC Address:', mac);
      console.log('Device Type:', deviceType);
      // Use the captured data as needed
    })
    .catch(error => {
      console.log('Error capturing user data:', error);
    });
}

captureUserData();


