const API_GATEWAY = "";
const input_form = document.getElementById("input_form_section");
const graph_section = document.getElementById("graph_section");
const submit_data_response = document.getElementById("submit_data_response");

async function returnCustomerData(url) {
  const start_button = document.getElementById("start_button");
  const population_size = document.getElementById("population_size");
  const initial_infection_rate = document.getElementById(
    "initial_infection_rate"
  );
  const initial_number_of_infected = document.getElementById(
    "initial_number_of_infected"
  );
  const recovery_rate = document.getElementById("recovery_rate");

  start_button.addEventListener("click", (e) => {
    e.preventDefault(); //stops the form from submitting in the traditional way, which would refresh the page.
    submit_input(
      population_size.value,
      initial_infection_rate.value,
      initial_number_of_infected.value,
      recovery_rate.value
    );
  });
}

async function submit_input(
  pop_size,
  initial_infection_rate,
  initial_number_of_infected,
  recovery_rate
) {
  const response = await fetch(API_GATEWAY + "/path", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      pop_size: `${pop_size}`,
      initial_infection_rate: `${initial_infection_rate}`,
      initial_number_of_infected: `${initial_number_of_infected}`,
      recovery_rate: `${recovery_rate}`,
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      console.log("Success:", data);
      submit_data_response.innerHTML = `<p>Successfully submitted data!</p>`;
      location.reload();
    });
}

// TODO
function returnGraphData() {
  console.log("Fetching " + API_GATEWAY + "/path");
  fetch(API_GATEWAY + "/path").then((res) => res.json());

  saved_customers_list.appendChild(div_saved_checklist);
}
