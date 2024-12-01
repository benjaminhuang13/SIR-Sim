const API_GATEWAY =
  "https://gp8rnrotf4.execute-api.us-east-1.amazonaws.com/prd/sirsim/data";
const input_form = document.getElementById("input_form_section");
const graph_section_msg = document.getElementById("graph_data_msg");
const graph_section = document.getElementById("graph_data_div");
const submit_data_response = document.getElementById("submit_data_response");
const start_button = document.getElementById("start_button");

start_button.addEventListener("click", (e) => {
  const population_size = document.getElementById("population_size");
  const initial_infection_rate = document.getElementById(
    "initial_infection_rate"
  );
  const initial_number_of_infected = document.getElementById(
    "initial_number_of_infected"
  );
  const recovery_rate = document.getElementById("recovery_rate");
  const timeStepsDays = document.getElementById("timeStepsDays");
  e.preventDefault(); //stops the form from submitting in the traditional way, which would refresh the page.
  console.log("start button clicked!");
  submit_input(
    population_size.value,
    initial_infection_rate.value,
    initial_number_of_infected.value,
    recovery_rate.value,
    timeStepsDays.value
  );
});

config = {
  headers: {
    "Content-Type": "application/json",
  },
};

async function submit_input(
  pop_size,
  initial_infection_rate,
  initial_number_of_infected,
  recovery_rate,
  timeStepsDays
) {
  graph_section.innerHTML = "";
  graph_section_msg.innerHTML = "";
  console.log("Sending user data!");
  body = JSON.stringify({
    userInputs: {
      populationSize: `${pop_size}`,
      infectionRate: `${initial_infection_rate}`,
      numInfected: `${initial_number_of_infected}`,
      recoveryRate: `${recovery_rate}`,
      timeStepsDays: `${timeStepsDays}`,
    },
  });
  await axios
    .put(API_GATEWAY, body, {
      headers: {
        "Content-Type": "application/json",
      },
    })
    .then((response) => {
      console.log(response);
      submit_data_response.innerHTML = `<p>Successfully submitted data!</p>`;
      fade_element(submit_data_response);
      console.log("Successfully sent data :)");
      fetchData();
    })
    .catch((error) => {
      console.log(error);
      console.log("Error sending data :(");
    });
}

const fetchData = async () => {
  console.log("fetching...");
  sleep(2000);
  const response = await axios
    .get(API_GATEWAY, config)
    .then((response) => {
      console.log("fetched data: " + response.data["data"]);
      if (response.data["message"] == "Message retrieved from SQS") {
        console.log("Response Status:", response.status);

        const data = JSON.parse(JSON.parse(response.data["data"]))["results"];
        graph_section_msg.innerHTML = `<p>Got data from success_results sqs!</p>`;
        fade_element(graph_section_msg);
        // var display_results = document.createElement("p");   // for displaying the results in text form
        // display_results.textContent = JSON.stringify(data);
        // graph_section.appendChild(display_results);

        // Convert the time from Unix timestamp to a Date object and prepare the chart data
        const labels = data.map((entry) =>
          new Date(entry.time * 1000).toLocaleString()
        ); // Convert Unix time to Date
        const susceptibleData = data.map((entry) => entry.numSusceptible);
        const infectedData = data.map((entry) => entry.numInfected);
        const recoveredData = data.map((entry) => entry.numRecovered);
        // Dynamically create the canvas element
        const canvas = document.createElement("canvas");
        canvas.width = 400;
        canvas.height = 200;
        canvas.id = "myChart";
        graph_section.appendChild(canvas);
        // Create chart
        const ctx = document.getElementById("myChart").getContext("2d");
        const myChart = new Chart(ctx, {
          type: "line", // Type of chart
          data: {
            labels: labels, // X-axis labels (time)
            datasets: [
              {
                label: "Susceptible",
                data: susceptibleData, // Data for Susceptible
                borderColor: "blue",
                fill: false,
                tension: 0.1,
              },
              {
                label: "Infected",
                data: infectedData, // Data for Infected
                borderColor: "red",
                fill: false,
                tension: 0.1,
              },
              {
                label: "Recovered",
                data: recoveredData, // Data for Recovered
                borderColor: "green",
                fill: false,
                tension: 0.1,
              },
            ],
          },
          options: {
            responsive: true,
            scales: {
              x: {
                type: "category",
                title: {
                  display: true,
                  text: "Time",
                },
              },
              y: {
                title: {
                  display: true,
                  text: "Count",
                },
              },
            },
          },
        });
      } else if (
        response.data["message"] == "Not Found" ||
        response.data["message"] == "No messages in the queue"
      ) {
        console.log("SQS empty");
        graph_section_msg.innerHTML = `<p>sqs empty!</p>`;
        fade_element(graph_section_msg);
      } else {
        print("Unknown response?");
      }
    })
    .catch((error) => {
      console.log(error.message);
      graph_section.innerHTML = `<p>No data!</p>`;
    });
};

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function fade_element(element) {
  var op = 1; // initial opacity
  var timer = setInterval(function () {
    if (op <= 0.1) {
      clearInterval(timer);
      element.style.display = "none";
    }
    element.style.opacity = op;
    element.style.filter = "alpha(opacity=" + op * 100 + ")";
    op -= op * 0.2;
  }, 100);
}
