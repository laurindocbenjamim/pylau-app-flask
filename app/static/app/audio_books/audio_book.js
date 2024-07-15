
  function sanitizeInput(input) {
    // Remove any script tags
    let sanitizedInput = input.replace(/<script[^>]*?>.*?<\/script>/gi, "");
    // Encode special characters
    sanitizedInput = sanitizedInput.replace(/</g, "&lt;").replace(/>/g, "&gt;");
    return sanitizedInput;
  }
  
  function sanitizeInput_2(str) {
    var div = document.createElement("div");
    div.appendChild(document.createTextNode(str));
    return div.innerHTML;
  }
  
  function filterString(input) {
    // This regular expression matches words with or without accentuation and punctuation
    var regex = /[A-Za-zÀ-ÖØ-öø-ÿ.,;?!'"\s]+/g;
    var result = input.match(regex);
    return result ? result.join('') : '';
  }
  
  function cleanForm() {
    var inputs = document
      .getElementById("subscriberForm")
      .getElementsByTagName("input");
    // Clear all input type="text" fields
    for (var i = 0; i < inputs.length; i++) {
      if (
        inputs[i].type.toLowerCase() == "text" ||
        inputs[i].type.toLowerCase() == "email"
      ) {
        inputs[i].value = "";
      }
    }
  }
  
  var navCharts = document.getElementById('nav-charts')
  
  document
    .getElementById("audio-book-fom")
    .addEventListener("submit", async (e) => {
        e.preventDefault()

        const baseUrl = window.location.origin;
        const dataForm = new FormData();
      
       
        dataForm.append("audio", "play");
        //
       
          const res = await fetch(
            `${baseUrl}/ai/audio-book`,
            {
              method: "POST",
              body: dataForm,
            }
          );
    
          const resData = await res.json();
    
          console.log(resData);

    });
  



 
  /**
   *  This method is used to remove existent canvas child element from
   * the chart container
   */
  function removeCanvasChildElement(container) {
    try {
      var old = document.querySelector("canvas");
      if (old) {
        container.removeChild(old);
      } else {
        console.log(old);
      }
    } catch (error) {
      console.log(error);
    }
  }
  
  /**
   *
   */
  let barChart = (type, tagID,data) => {
    //console.log(data[0].scores[0])
    const xValues = data[0].emotions;
    const yValues = data[0].scores;
    const barColors = ["#b91d47", "#00aba9", "#2b5797", "#e8c3b9", "#1e7145"];
  
    new Chart(`${tagID}`, {
      type: `${type}`,
      data: {
        labels: xValues,
        datasets: [
          {
            backgroundColor: barColors,
            data: yValues ,
          },
        ],
      },
      options: {
        title: {
          display: true,
          text: "Emotions Rate Analysis",
        },
      },
    });
  };
  
  var lineChart = (data) => {
    const xValues = data[0].emotions;
    const yValues = data[0].scores;
    const barColors = ["#b91d47", "#00aba9", "#2b5797", "#e8c3b9", "#1e7145"];
  
    new Chart("lineChart", {
      type: "line",
      data: {
        labels: xValues,
        datasets: [
          {
            fill: false,
            lineTension: 0,
            backgroundColor: "rgba(0,0,255,1.0)",
            borderColor: "rgba(0,0,255,0.1)",
            data: yValues,
          },
        ],
      },
      options: {
        title: {
          display: true,
          text: "Emotions Rate Analysis",
        },
        legend: { display: false },
        scales: {
          yAxes: [{ ticks: { min: 6, max: 100 } }],
        },
      },
    });
  };
  
  let multipleLineChart = (data) => {
    const xValues = data[0].emotions;
    const yValues = data[0].scores;
  
    new Chart("multipleLineChart", {
      type: "line",
      data: {
        labels: xValues,
        datasets: [
          {
            fill: false,
            lineTension: 0,
            backgroundColor: "rgba(0,0,255,1.0)",
            borderColor: "rgba(0,0,255,0.1)",
            data: yValues,
          },
        ],
      },
      options: {
        title: {
          display: true,
          text: "Emotions Rate Analysis",
        },
        legend: { display: false },
      },
    });
  };
  
  let pieChart = (data) => {
    const xValues = data[0].emotions;
    const yValues = data[0].scores;
    const barColors = ["#b91d47", "#00aba9", "#2b5797", "#e8c3b9", "#1e7145"];
  
    new Chart("pieChart", {
      type: "pie",
      data: {
        labels: xValues,
        datasets: [
          {
            backgroundColor: barColors,
            data: yValues,
          },
        ],
      },
      options: {
        title: {
          display: true,
          text: "Emotions Rate Analysis",
        },
      },
    });
  };
  
  let doughnutChart = (data) => {
    const xValues = data[0].emotions;
    const yValues = data[0].scores;
    const barColors = ["#b91d47", "#00aba9", "#2b5797", "#e8c3b9", "#1e7145"];
  
    new Chart("doughnutChart", {
      type: "doughnut",
      data: {
        labels: xValues,
        datasets: [
          {
            backgroundColor: barColors,
            data: yValues,
          },
        ],
      },
      options: {
        title: {
          display: true,
          text: "Emotions Rate Analysis",
        },
      },
    });
  };
  