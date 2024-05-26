// Example starter JavaScript for disabling form submissions if there are invalid fields

const form = document.getElementById('form-register');
const alertmessage = document.querySelector('.alert p');
alertmessage.style.color = "red";

form.addEventListener("submit", async event => {
    event.preventDefault();

  const data = new FormData(form);

  console.log(Array.from(data));
  const baseUrl = window.location.origin;
  //alert("base url" +baseUrl);

  try {
    const res = await fetch(
      baseUrl + '/auth/register',
      {
        method: 'POST',
        body: data
      },
    );

    const resData = await res.json();
    
    

    console.log(resData[0].object);
    if(resData){
      console.log(resData[0].object);
      //alert(resData[0].object)
      alertmessage.textContent = "Username or password wrong!";
      window.open(baseUrl + '/auth/login', '_self');
    }
  } catch (err) { 
    //alert("Erro ao realizar o cadastro, tente novamente mais tarde " + err.message);
    console.log(err.message);
  }
  
});
