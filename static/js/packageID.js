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

const stars = document.querySelectorAll('#rating-stars .star');
    let selectedRating = 0;

    stars.forEach(star => {
        star.addEventListener('mouseenter', () => {
            const rating = parseInt(star.dataset.rating);
            highlightStars(rating);
        });

        star.addEventListener('mouseleave', () => {
            highlightStars(selectedRating);
        });

        star.addEventListener('click', () => {
            selectedRating = parseInt(star.dataset.rating);
            highlightStars(selectedRating);
            // Optionnel : tu peux stocker cette valeur ou l'envoyer avec "Apply"
            console.log("User selected rating:", selectedRating);
        });
    });

    function highlightStars(rating) {
        stars.forEach(star => {
            const starRating = parseInt(star.dataset.rating);
            star.classList.toggle('selected', starRating <= rating);
        });
    }
