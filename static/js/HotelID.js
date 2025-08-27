function toggleSortMenu() {
    let menu = document.getElementById("sort-menu");
    menu.classList.toggle("show"); // Alterne entre affiché et caché
}

function sortBy(criteria) {
    console.log("Sorting by: " + criteria); // Affiche le critère dans la console

    // Mettre à jour le texte du bouton
    document.getElementById("sort-button").innerText = "Sorted By: " + formatCriteria(criteria);

    // Cacher le menu après la sélection
    document.getElementById("sort-menu").classList.remove("show");
}

// Fonction pour formater le texte
function formatCriteria(criteria) {
    switch (criteria) {
        case 'price-high': return 'Price: High to Low';
        case 'price-low': return 'Price: Low to High';
        default: return 'Sorted By';
    }
}

document.addEventListener("DOMContentLoaded", function () {
    const filterButtons = document.querySelectorAll(".filter-option");
    const priceSlider = document.getElementById("price-slider");
    const minPrice = document.getElementById("min-price");
    const maxPrice = document.getElementById("max-price");
    const resetButton = document.getElementById("reset-button");

    // Sélection des filtres
    filterButtons.forEach(button => {
        button.addEventListener("click", function () {
            this.classList.toggle("selected");
        });
    });

    // Mise à jour du prix max sélectionné
    priceSlider.addEventListener("input", function () {
        maxPrice.textContent = this.value;
    });

    // Réinitialisation des filtres
    resetButton.addEventListener("click", function () {
        filterButtons.forEach(button => button.classList.remove("selected"));
        priceSlider.value = 1000;
        maxPrice.textContent = 1000;
        document.getElementById("departure-date").value = "";
        document.getElementById("return-date").value = "";
        document.getElementById("departBy").innerText = "Depart By";
        document.getElementById("returnBy").innerText = "Return By";
    });

    // Fonction pour afficher/masquer le menu
    window.toggleFilterMenu = function () {
        document.getElementById("filter-menu").classList.toggle("show");
    };

    // Fonction pour gérer l'affichage du calendrier
    function setupDatePicker(buttonId, inputId, labelText) {
        const button = document.getElementById(buttonId);
        const input = document.getElementById(inputId);

        button.addEventListener("click", function (event) {
            event.stopPropagation(); // Empêche la fermeture immédiate
            input.classList.toggle("show"); // Afficher/Masquer
            input.focus();
        });

        input.addEventListener("change", function () {
            button.innerText = `${labelText}: ${input.value}`;
            button.classList.add("selected");
            input.classList.remove("show"); // Masquer après sélection
        });

        // Fermer quand on clique ailleurs
        document.addEventListener("click", function (event) {
            if (!button.contains(event.target) && !input.contains(event.target)) {
                input.classList.remove("show");
            }
        });
    }

    setupDatePicker("departBy", "departure-date", "Depart");
    setupDatePicker("returnBy", "return-date", "Return");
});

document.addEventListener("DOMContentLoaded", () => {
    const filterMenu = document.querySelector(".filter-menu");
    const footer = document.querySelector(".about-us");

    const originalTop = 100; // même que dans ton CSS

    window.addEventListener("scroll", () => {
        const footerTop = footer.getBoundingClientRect().top;
        const filterHeight = filterMenu.offsetHeight;

        // Si le filtre touche le footer, on le rend "bloqué" au-dessus
        if (footerTop < filterHeight + originalTop + 20) {
            filterMenu.style.position = "absolute";
            filterMenu.style.top = (footer.offsetTop - filterHeight - 20) + "px";
        } else {
            filterMenu.style.position = "fixed";
            filterMenu.style.top = originalTop + "px";
        }
    });
});

const stars = document.querySelectorAll('.rating-stars .star');
let selectedRating = 0;

function highlightStars(rating) {
    stars.forEach(star => {
        const starRating = parseInt(star.dataset.rating);
        star.classList.toggle('selected', starRating <= rating);
    });
}

function highlightHover(rating) {
    stars.forEach(star => {
        const starRating = parseInt(star.dataset.rating);
        star.classList.toggle('hover', starRating <= rating);
    });
}

stars.forEach(star => {
    const rating = parseInt(star.dataset.rating);

    // Hover in
    star.addEventListener('mouseenter', () => {
        highlightHover(rating);
    });

    // Hover out
    star.addEventListener('mouseleave', () => {
        highlightHover(0); // remove all hovers
    });

    // Click = select rating
    star.addEventListener('click', () => {
        selectedRating = rating;
        highlightStars(selectedRating);
        console.log('Selected rating:', selectedRating);
    });
});






  let selectedHotelType = null;

  document.querySelectorAll('.filter-option[data-type]').forEach(button => {
    button.addEventListener('click', function () {
      // Unselect all other buttons
      document.querySelectorAll('.filter-option[data-type]').forEach(btn => btn.classList.remove('selected'));
      
      // Toggle selection
      if (selectedHotelType === this.dataset.type) {
        selectedHotelType = null; // unselect if already selected
      } else {
        selectedHotelType = this.dataset.type;
        this.classList.add('selected');
      }
    });
  });

  document.getElementById('apply-filters').addEventListener('click', function () {
    const params = new URLSearchParams();

    if (selectedHotelType) {
      params.append('type', selectedHotelType);
    }

    // You can also append other filters here later (price, rating...)

    // Use HTMX or fetch to get updated results
    fetch(`/hotel-id/cards/?${params.toString()}`)
      .then(response => response.text())
      .then(html => {
        document.getElementById('hotel-cards').outerHTML = html;
      });
  });



  // price range functions 
  let min = 1000;
  let max = 5000;
  const step = 1000;
  const minLimit = 0;
  const maxLimit = 10000;
  
  function changePrice(type, value) {
    if (type === 'min') {
      min = Math.min(max - step, Math.max(min + value, minLimit));
      document.getElementById('min-price').textContent = `${min} DZD`;
    } else {
      max = Math.max(min + step, Math.min(max + value, maxLimit));
      document.getElementById('max-price').textContent = `${max} DZD`;
    }
  }