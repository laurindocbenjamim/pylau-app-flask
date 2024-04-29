// Example starter JavaScript for disabling form submissions if there are invalid fields

const form = document.getElementById('form-code');

form.addEventListener("submit", async event => {
    event.preventDefault();

  const data = new FormData(form);

  console.log(Array.from(data));

  try {
    const res = await fetch(
      'http://localhost:5000/person',
      {
        method: 'POST',
        body: data
      },
    );

    const resData = await res.json();
 
    console.log(resData);
    if(resData){
        alert(resData.object)
    }
  } catch (err) { 
    console.log(err.message);
  }
  
});
