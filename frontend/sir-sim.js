const API_GATEWAY =
  "https://gp8rnrotf4.execute-api.us-east-1.amazonaws.com/prd/sirsim/data";
const input_form = document.getElementById("input_form_section");
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
  console.log("Sending user data!");
  payload = JSON.stringify();
  await axios
    .post(
      API_GATEWAY,
      {
        userInputs: {
          populationSize: `${pop_size}`,
          infectionRate: `${initial_infection_rate}`,
          numInfected: `${initial_number_of_infected}`,
          recoveryRate: `${recovery_rate}`,
          timeStepsDays: `${timeStepsDays}`,
        },
      }
      // {
      //   headers: {
      //     // "Content-Type": "application/json;charset=UTF-8",
      //     "Content-Type": "application/x-www-form-urlencoded",
      //     // "Access-Control-Allow-Origin": "*",
      //   },
      // }
    )
    .then((response) => {
      console.log(response);
      submit_data_response.innerHTML = `<p>Successfully submitted data!</p>`;
      console.log("Successfully posted data!");
      fetchData();
    })
    .catch((error) => {
      console.log(error);
      console.log("Something went wrong!");
    });
}

// TODO;
function getData() {
  console.log("Fetching " + API_GATEWAY);
  fetch(API_GATEWAY).then((res) => res.json());
  saved_customers_list.appendChild(div_saved_checklist);
  graph_section.innerHTML = `<p>Got data from success_results sqs!</p>`;
}

const fetchData = async () => {
  try {
    const response = await axios.get(API_GATEWAY, config);
    console.log("fetching");
    console.log(response.data);
    if (response.data["message"] == "Not Found" || "No messages in the queue") {
      console.log("SQS empty");
      return;
    }
    setData(response.data);
    setLoading(false);
    graph_section.innerHTML = `<p>Got data from success_results sqs!</p>`;
  } catch (error) {
    //setError(error.message);
    console.log(error.message);
    graph_section.innerHTML = `<p>can't get data!</p>`;
    setLoading(false);
  }
};
