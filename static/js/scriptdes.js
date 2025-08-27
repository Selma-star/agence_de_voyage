const cards = document.querySelectorAll('.card');
const cardsPerPage = 16; // Combien de cartes par page
const totalPages = 50; // Nombre total de pages
const pageNumbersContainer = document.querySelector('.page-numbers');
const prevButton = document.querySelector('.prev');
const nextButton = document.querySelector('.next');
let currentPage = 1;

// Pagination affichée par "groupe" de pages
const pagesToShow = 3; 
let currentGroup = 0;

function createPageNumbers() {
    pageNumbersContainer.innerHTML = '';
    const startPage = currentGroup * pagesToShow + 1;
    const endPage = Math.min(startPage + pagesToShow - 1, totalPages);

    for (let i = startPage; i <= endPage; i++) {
        const button = document.createElement('button');
        button.textContent = i;
        if (i === currentPage) {
            button.classList.add('active');
        }
        button.addEventListener('click', () => {
            currentPage = i;
            updateCards();
            updateActiveButton();
        });
        pageNumbersContainer.appendChild(button);
    }
}

function updateCards() {
    const start = (currentPage - 1) * cardsPerPage;
    const end = start + cardsPerPage;

    cards.forEach((card, index) => {
        if (index >= start && index < end) {
            card.style.display = 'block';
        } else {
            card.style.display = 'none';
        }
    });
}

function updateActiveButton() {
    const buttons = document.querySelectorAll('.page-numbers button');
    buttons.forEach((btn) => {
        if (parseInt(btn.textContent) === currentPage) {
            btn.classList.add('active');
        } else {
            btn.classList.remove('active');
        }
    });
}

prevButton.addEventListener('click', () => {
    if (currentGroup > 0) {
        currentGroup--;
        createPageNumbers();
        updateActiveButton();
    }
});

nextButton.addEventListener('click', () => {
    const maxGroup = Math.floor((totalPages - 1) / pagesToShow);
    if (currentGroup < maxGroup) {
        currentGroup++;
        createPageNumbers();
        updateActiveButton();
    }
});

// Initialiser
createPageNumbers();
updateCards();
updateActiveButton();