const API_GATEWAY =
  "https://gp8rnrotf4.execute-api.us-east-1.amazonaws.com/prd/sirsim";
const input_form = document.getElementById("input_form_section");
const graph_section = document.getElementById("graph_section");
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
  e.preventDefault(); //stops the form from submitting in the traditional way, which would refresh the page.
  console.log("start button clicked!");
  submit_input(
    population_size.value,
    initial_infection_rate.value,
    initial_number_of_infected.value,
    recovery_rate.value
  );
});

// TODO
function submit_input(
  pop_size,
  initial_infection_rate,
  initial_number_of_infected,
  recovery_rate
) {
  axios
    .post(
      "https://gp8rnrotf4.execute-api.us-east-1.amazonaws.com/prd/sirsim/data",
      {
        api: "post",
        pop_size: `${pop_size}`,
        initial_infection_rate: `${initial_infection_rate}`,
        initial_number_of_infected: `${initial_number_of_infected}`,
        recovery_rate: `${recovery_rate}`,
      }
    )
    .then((response) => {
      console.log(response);
      submit_data_response.innerHTML = `<p>Successfully submitted data!</p>`;
      console.log("Successfully posted data!");
    })
    .catch((error) => {
      console.log(error);
      console.log("Something went wrong!");
    });
}

// TODO
function returnGraphData() {
  console.log("Fetching " + API_GATEWAY + "/path");
  fetch(API_GATEWAY + "/path").then((res) => res.json());

  saved_customers_list.appendChild(div_saved_checklist);
}
