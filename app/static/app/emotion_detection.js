
class Sentiment{

    constructor(id, comment) {
        this.id = id;
        this.comment = comment;
    }

   

    
    
    
}

function sanitizeInput(input){
    // Remove any script tags
    let sanitizedInput = input.replace(/<script[^>]*?>.*?<\/script>/gi, '');
    // Encode special characters
    sanitizedInput = sanitizedInput.replace(/</g, "&lt;").replace(/>/g, "&gt;");
    return sanitizedInput;
}

function sanitizeInput_2(str) {
    var div = document.createElement('div');
    div.appendChild(document.createTextNode(str));
    return div.innerHTML;
}

function cleanForm(){
    var inputs = document.getElementById('subscriberForm').getElementsByTagName('input');
    // Clear all input type="text" fields
    for (var i = 0; i < inputs.length; i++) {
        if (inputs[i].type.toLowerCase() == 'text' || inputs[i].type.toLowerCase() == 'email') {
            inputs[i].value = '';
        }
        
    }
}


document.getElementById('sentimentAnalyserForm').addEventListener('submit', async e => {
    e.preventDefault();   
    
    const baseUrl = window.location.origin;
    const dataForm = new FormData();
    //const data = [{'name': 'laurindo', 'age': 12},{'name': 'mauro', 'age': 111}]    

    var token = document.querySelector('meta[name="token"]').getAttribute('content')

    var alertmessage = document.querySelector('.form-message p')
    var response = document.getElementById('response')
    var comment = sanitizeInput(document.getElementById('comment').value);

    let decimalPlace = 2 // number of decimal places
    let factor = Math.pow(10, decimalPlace)
    
    if (comment.length > 255){
        return
    }
    var obj = new Sentiment(1, comment);
    dataForm.append('comment', obj.comment)
    //

    try {
        const res = await fetch(
            `${baseUrl}/data-science/project/emotion-detector/${ token }`,
            {
              method: 'POST',
              body: dataForm
            },
          );
      
        const resData = await res.json();
        
        //console.log(resData);
        
        if(resData){
            if(resData[1] == 400){
                
                alertmessage.classList.add(resData[0].category)
                alertmessage.textContent = ''
                alertmessage.textContent = resData[0].message;
            }else if(resData[1] == 200){
                //
                cleanForm()
                let max_score = 0
                const emotions = resData[0].emotions
                emotions.forEach((element) => {
                    var ol = document.createElement('ol')
                    ol.className = "list-group list-group-numbered"
                    var p = document.createElement('p')
                    var li_anger = document.createElement('li')
                    var li_disgust = document.createElement('li')
                    var li_fear = document.createElement('li')
                    var li_joy = document.createElement('li')
                    var li_sadness = document.createElement('li')

                    li_anger.className = "list-group-item d-flex justify-content-between align-items-start"
                    
                    var divChild = document.createElement('div')
                    divChild.className = "fw-bold"
                    divChild.textContent = "Anger"

                    var divParent = document.createElement('div')
                    divParent.className = "ms-2 me-auto"
                    p.textContent = `The anger is a bad feeling. Score: [${element.anger}]`                    

                    var span = document.createElement('span')
                    span.className = "badge text-bg-primary rounded-pill"
                 
                    span.textContent = `${Math.round(parseFloat(element.anger) * factor)}%`
                    max_score = parseFloat(element.anger) > max_score? parseFloat(element.anger) : max_score
                    
                    if(max_score == parseFloat(element.anger)){
                        li_anger.classList.add('active')
                        li_disgust.classList.remove('active')
                        li_fear.classList.remove('active')
                        li_joy.classList.remove('active')
                        li_sadness.classList.remove('active')
                        
                    }
                    divParent.appendChild(divChild)   
                    divParent.appendChild(p)
                    li_anger.appendChild(divParent)
                    li_anger.appendChild(span)
                    

                    /**
                     * 
                     */

                    var p_disgust = document.createElement('p')

                    
                    li_disgust.className = "list-group-item d-flex justify-content-between align-items-start"

                    var divChild_disgust = document.createElement('div')
                    divChild_disgust.className = "fw-bold"
                    divChild_disgust.textContent = "DISGUST"

                    var divParent_disgust = document.createElement('div')
                    divParent_disgust.className = "ms-2 me-auto"                                       

                    var span_disgust = document.createElement('span')
                    span_disgust.className = "badge text-bg-primary rounded-pill"
                    span_disgust.textContent = `${Math.round(parseFloat(element.disgust) * factor)}%`
                    
                    p_disgust.textContent = `The Disgust is a bad feeling. Score: [${element.disgust}]`

                    max_score = parseFloat(element.disgust) > max_score? parseFloat(element.disgust) : max_score
                    
                    if(max_score == parseFloat(element.disgust)){
                        li_anger.classList.remove('active')
                        li_disgust.classList.add('active')
                        li_fear.classList.remove('active')
                        li_joy.classList.remove('active')
                        li_sadness.classList.remove('active')
                        
                    }

                    divParent_disgust.appendChild(divChild_disgust) 
                    divParent_disgust.appendChild(p_disgust)

                    li_disgust.appendChild(divParent_disgust)
                    li_disgust.appendChild(span_disgust)

                    /**
                     * 
                     */

                    var p_fear = document.createElement('p')

                    
                    li_fear.className = "list-group-item d-flex justify-content-between align-items-start"

                    var divChild_fear = document.createElement('div')
                    divChild_fear.className = "fw-bold"
                    divChild_fear.textContent = "FEAR"

                    var divParent_fear = document.createElement('div')
                    divParent_fear.className = "ms-2 me-auto"                                       

                    var span_fear = document.createElement('span')
                    span_fear.className = "badge text-bg-primary rounded-pill"
                    span_fear.textContent = `${Math.round(parseFloat(element.fear) * factor)}%`
                    
                    p_fear.textContent = `The Fear is a bad feeling. Score: [${element.fear}]`
                    max_score = parseFloat(element.anger) > max_score? parseFloat(element.fear) : max_score
                    
                    if(max_score == parseFloat(element.fear)){
                        li_anger.classList.remove('active')
                        li_disgust.classList.remove('active')
                        li_fear.classList.add('active')
                        li_joy.classList.remove('active')
                        li_sadness.classList.remove('active')
                        
                    }

                    divParent_fear.appendChild(divChild_fear) 
                    divParent_fear.appendChild(p_fear)

                    li_fear.appendChild(divParent_fear)
                    li_fear.appendChild(span_fear)

                    /**
                     * 
                     */

                    var p_joy = document.createElement('p')
                    
                    li_joy.className = "list-group-item d-flex justify-content-between align-items-start"
                    li_joy.id = "joy-element"

                    var divChild_joy = document.createElement('div')
                    divChild_joy.className = "fw-bold"
                    divChild_joy.textContent = "JOY"

                    var divParent_joy = document.createElement('div')
                    divParent_joy.className = "ms-2 me-auto"                                       

                    var span_joy = document.createElement('span')
                    span_joy.className = "badge text-bg-primary rounded-pill"
                    span_joy.textContent = `${Math.round(parseFloat(element.joy) * factor)}%`
                    
                    p_joy.textContent = `The Joy is a GOOD feeling. Score: [${element.joy}]`

                    max_score = parseFloat(element.joy) > max_score? parseFloat(element.joy) : max_score
                    
                    if(max_score == parseFloat(element.joy)){
                        li_anger.classList.remove('active')
                        li_disgust.classList.remove('active')
                        li_fear.classList.remove('active')
                        li_joy.classList.add('active')
                        li_sadness.classList.remove('active')
                        li_joy.classList.add('active')
                        li_joy.setAttribute('data-bs-toggle', 'tooltip')
                        li_joy.setAttribute('data-bs-placement', 'top')
                        li_joy.setAttribute('data-bs-custom-class', 'custom-tooltip')
                        li_joy.setAttribute('data-bs-title', `This is the dominante emotion detected with ${max_score}% of max score`)
                    }

                    divParent_joy.appendChild(divChild_joy) 
                    divParent_joy.appendChild(p_joy)

                    li_joy.appendChild(divParent_joy)
                    li_joy.appendChild(span_joy)

                    /**
                     * 
                     */

                    var p_sadness = document.createElement('p')
                    
                    li_sadness.className = "list-group-item d-flex justify-content-between align-items-start"

                    var divChild_sadness = document.createElement('div')
                    divChild_sadness.className = "fw-bold"
                    divChild_sadness.textContent = "SADNESS"

                    var divParent_sadness = document.createElement('div')
                    divParent_sadness.className = "ms-2 me-auto"                                       

                    var span_sadness = document.createElement('span')
                    span_sadness.className = "badge text-bg-primary rounded-pill"
                    span_sadness.textContent = `${Math.round(parseFloat(element.sadness) * factor)}%`
                    
                    p_sadness.textContent = `The Sadness is a BAD feeling. Score: [${element.sadness}]`
                    
                    max_score = parseFloat(element.sadness) > max_score? parseFloat(element.sadness) : max_score
                    
                    if(max_score == parseFloat(element.sadness)){
                        li_anger.classList.remove('active')
                        li_disgust.classList.remove('active')
                        li_fear.classList.remove('active')
                        li_joy.classList.remove('active')
                        li_sadness.classList.add('active')

                    }

                    divParent_sadness.appendChild(divChild_sadness) 
                    divParent_sadness.appendChild(p_sadness)

                    li_sadness.appendChild(divParent_sadness)
                    li_sadness.appendChild(span_sadness)

                    /* ==============   =============*/
                    
                    ol.appendChild(li_anger)                    
                    ol.appendChild(li_disgust)
                    ol.appendChild(li_fear)
                    ol.appendChild(li_joy)
                    ol.appendChild(li_sadness)
                    
                    response.innerHTML = '';
                    response.appendChild(ol)
                })

                
                alertmessage.classList.add(resData[0].category)
                alertmessage.textContent = ''
                alertmessage.textContent = resData[0].message;
            }
        }
    } catch (err) {
        console.log(err);
        console.log(err.message);
    }

    

});




/*document.addEventListener('DOMContentLoaded', (ev) => {
    document.getElementById('subscriberForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        var email = document.getElementById("subscriber").value;
        var obj = new Subscriber(1, email);
        //

        const res = await fetch(
            //baseUrl + '/auth/register',
            baseUrl + '/register/user/create',
            {
              method: 'POST',
              body: dataForm
            },
          );
      
        const resData = await res.json();

    })
})*/