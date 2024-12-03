const API_GATEWAY =
  "https://o1tzuafmkh.execute-api.us-east-1.amazonaws.com/sirsim/data"; //gp8rnrotf4
const input_form = document.getElementById("input_form_section");
const graph_section_msg = document.getElementById("graph_data_msg");
const graph_data_div = document.getElementById("graph_data_div");
const submit_data_response = document.getElementById("submit_data_response");
const start_button = document.getElementById("start_button");
const test_button = document.getElementById("test_button");

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

// test
test_button.addEventListener("click", async (e) => {
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
  console.log("test button clicked!");
  for (let i = 0; i < 900; i++) {
    await sleep(2000);
    console.log("iteration: " + i);
    submit_input(
      population_size.value,
      initial_infection_rate.value,
      initial_number_of_infected.value,
      recovery_rate.value,
      timeStepsDays.value
    );
  }
});
function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

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
  graph_data_div.innerHTML = "";
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
  const response = await axios
    .get(API_GATEWAY, config)
    .then((response) => {
      console.log("fetched data: " + response.data["data"]);
      if (response.data["message"] == "Message retrieved from SQS") {
        console.log("Response Status:", response.status);
        const data = JSON.parse(response.data["data"])["results"];
        graph_section_msg.innerHTML = `<p>Got data from success_results sqs!</p>`;
        fade_element(graph_section_msg);
        const labels = data.map((entry) =>
          new Date(entry.time * 1000).toLocaleDateString("en-US", {
            year: "numeric",
            month: "short",
            day: "numeric",
          })
        );
        const susceptibleData = data.map((entry) => entry.numSusceptible);
        const infectedData = data.map((entry) => entry.numInfected);
        const recoveredData = data.map((entry) => entry.numRecovered);
        const canvas1 = document.createElement("canvas");
        canvas1.width = 450;
        canvas1.height = 300;
        canvas1.id = "susceptibleChart";
        const canvas2 = document.createElement("canvas");
        canvas2.width = 450;
        canvas2.height = 300;
        canvas2.id = "infectedRecoveredChart";
        graph_data_div.appendChild(canvas1);
        graph_data_div.appendChild(canvas2);
        const ctx1 = document
          .getElementById("susceptibleChart")
          .getContext("2d");
        new Chart(ctx1, {
          type: "line",
          data: {
            labels: labels,
            datasets: [
              {
                label: "Susceptible",
                data: susceptibleData,
                borderColor: "rgba(75, 192, 192, 1)",
                backgroundColor: "rgba(75, 192, 192, 0.2)",
                fill: true,
                tension: 0.1,
              },
            ],
          },
          options: {
            scales: {
              y: {
                type: "logarithmic",
                title: {
                  display: true,
                  text: "Number of Susceptible Individuals",
                },
                ticks: {
                  callback: function (value) {
                    return value.toLocaleString();
                  },
                },
              },
              x: {
                title: {
                  display: true,
                  text: "Time",
                },
              },
            },
          },
        });
        const ctx2 = document
          .getElementById("infectedRecoveredChart")
          .getContext("2d");
        new Chart(ctx2, {
          type: "line",
          data: {
            labels: labels,
            datasets: [
              {
                label: "Infected",
                data: infectedData,
                borderColor: "rgba(255, 99, 132, 1)",
                backgroundColor: "rgba(255, 99, 132, 0.2)",
                fill: true,
                tension: 0.1,
              },
              {
                label: "Recovered",
                data: recoveredData,
                borderColor: "rgba(54, 162, 235, 1)",
                backgroundColor: "rgba(54, 162, 235, 0.2)",
                fill: true,
                tension: 0.1,
              },
            ],
          },
          options: {
            scales: {
              y: {
                type: "logarithmic",
                title: {
                  display: true,
                  text: "Number of Infected/Recovered Individuals",
                },
                ticks: {
                  callback: function (value) {
                    return value.toLocaleString();
                  },
                },
              },
              x: {
                title: {
                  display: true,
                  text: "Time",
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
      graph_data_div.innerHTML = `<p>No data!</p>`;
    });
};

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
