document.addEventListener("DOMContentLoaded", function () {
  // Highlight the active navbar link
  let currentPath = window.location.pathname;
  let navLinks = document.querySelectorAll(".navbar a");

  navLinks.forEach(link => {
      if (link.getAttribute("href") === currentPath) {
          link.classList.add("active");
      }
  });

  // Existing feedback carousel functionality
  let feedbacks = document.querySelectorAll(".feedback-card");
  let index = 0;

  function showFeedback(i) {
      feedbacks.forEach((card, idx) => {
          card.style.display = (idx === i || idx === i + 1) ? "block" : "none";
      });
  }

  function prevFeedback() {
      index = (index - 1 + feedbacks.length) % feedbacks.length;
      showFeedback(index);
  }

  function nextFeedback() {
      index = (index + 1) % feedbacks.length;
      showFeedback(index);
  }

  // Show first two feedbacks
  showFeedback(0);
 
  
});


// hotel js 
// counter of people 
let adults = 1;
                      
function updatePeople(type, change) {
   if (type === 'adults') {
         adults = Math.max(1, adults + change); // Minimum 1 adulte
} 
document.getElementById("people-count").innerText = adults + " adults / " ;
}
// Country combobox 

const input = document.getElementById("country");
const dropdown = document.getElementById("country-list");

let selected = null;
let activeIndex = -1;
let countries = [];

async function loadCountries() {
 const res = await fetch("/api/countries/");
 countries = await res.json();
}

function filterCountries(query) {
 return countries.filter(country =>
   country.name.toLowerCase().includes(query.toLowerCase())
 );
}

function renderDropdown(items) {
 dropdown.innerHTML = "";
 if (items.length === 0) {
   dropdown.innerHTML = "<li class='no-results'>Nothing found.</li>";
   return;
 }

 items.forEach((country, index) => {
   const li = document.createElement("li");
   li.className = "option";
   if (selected && selected.id === country.id) li.classList.add("selected");

   li.innerHTML = `<span>${country.name}</span>${selected && selected.id === country.id ? '<span class="checkmark">✔</span>' : ''}`;

   li.addEventListener("click", () => {
     selected = country;
     input.value = country.name;
     dropdown.style.display = "none";
     loadCities(country.name); // 🔁 load cities for selected country
   });

   dropdown.appendChild(li);
 });
}

function updateDropdown() {
 const query = input.value;
 const filtered = query ? filterCountries(query) : countries;
 renderDropdown(filtered);
 dropdown.style.display = "block";
 activeIndex = -1;
}

input.addEventListener("input", updateDropdown);
input.addEventListener("focus", updateDropdown);
document.addEventListener("click", e => {
 if (!e.target.closest(".combobox")) dropdown.style.display = "none";
});

loadCountries(); // Initial fetch

// Cities  combobox
const cityInput = document.getElementById('city');
const cityDropdown = document.getElementById('cityDropdown');

let selectedCity = null;
let activeCityIndex = -1;
let cities = [];

async function loadCities(countryName = "") {
const res = await fetch(`/api/cities/?country=${countryName}`);
cities = await res.json();
//updateCityDropdown();
}

function filterCities(query) {
return cities.filter(city =>
  city.name.toLowerCase().replace(/\s+/g, '')
      .includes(query.toLowerCase().replace(/\s+/g, ''))
);
}

function renderCityDropdown(items) {
cityDropdown.innerHTML = '';
if (items.length === 0) {
  cityDropdown.innerHTML = '<li class="no-results">Nothing found.</li>';
  return;
}

items.forEach((city, index) => {
  const li = document.createElement('li');
  li.className = 'option';
  if (selectedCity && selectedCity.id === city.id) li.classList.add('selected');

  li.innerHTML = `<span>${city.name}</span>${selectedCity && selectedCity.id === city.id ? '<span class="checkmark">✔</span>' : ''}`;

  li.addEventListener('click', () => {
    selectedCity = city;
    cityInput.value = city.name;
    cityDropdown.style.display = 'none';
  });

  cityDropdown.appendChild(li);
});
}

function updateCityDropdown() {
const query = cityInput.value;
const filtered = query ? filterCities(query) : cities;
renderCityDropdown(filtered);
cityDropdown.style.display = 'block';
activeCityIndex = -1;
}

cityInput.addEventListener('input', updateCityDropdown);
cityInput.addEventListener('focus', updateCityDropdown);
document.addEventListener("click", e => {
if (!e.target.closest(".combobox")) cityDropdown.style.display = "none";
});
// departure checks 


document.addEventListener('DOMContentLoaded', function () {
const form = document.querySelector('.filter-container');
const checkinInput = document.getElementById('departure');
const checkoutInput = document.getElementById('return');

// Enable and set min for return date when check-in is chosen
checkinInput.addEventListener('change', function () {
  if (checkinInput.value) {
    checkoutInput.disabled = false;
    checkoutInput.min = checkinInput.value;

    // Optional reset: if checkout date is before new check-in, clear it
    if (checkoutInput.value && new Date(checkoutInput.value) <= new Date(checkinInput.value)) {
      checkoutInput.value = '';
    }
  }
});

// Prevent invalid date range on submit
form.addEventListener('submit', function (e) {
  const checkinDate = new Date(checkinInput.value);
  const checkoutDate = new Date(checkoutInput.value);

  if (!checkoutInput.value || checkoutDate <= checkinDate) {
    e.preventDefault();
    alert("Check-out date must be after check-in date.");
    return false;
  }
});
});
