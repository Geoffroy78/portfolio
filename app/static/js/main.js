const toggle = document.querySelector(".navbar-toggle");
const links = document.querySelector(".navbar-links");
const items = document.querySelectorAll(".navbar-links a");

toggle.addEventListener("click", () => {
    links.classList.toggle("active");
});

// quand on clique sur un lien → on ferme le menu
items.forEach(item => {
    item.addEventListener("click", () => {
        links.classList.remove("active");
    });
});

const buttons = document.querySelectorAll(".filter-btn");
const cards = document.querySelectorAll(".skill-card");

buttons.forEach(button => {

    button.addEventListener("click", () => {

        document.querySelector(".active").classList.remove("active");
        button.classList.add("active");

        const filter = button.dataset.filter;

        cards.forEach(card => {

            if(filter === "all" || card.dataset.category === filter){
                card.style.display = "block";
            }
            else{
                card.style.display = "none";
            }

        });

    });

});

const form = document.getElementById("contact-form");
const status = document.getElementById("form-status");

if (form) {
    form.addEventListener("submit", async function(e) {
        e.preventDefault();

        const data = new FormData(form);

        fetch("https://formspree.io/f/TON_ID", {
            method: "POST",
            body: data,
            headers: {
                'Accept': 'application/json'
            }
        })
        .then(response => {
            if (response.ok) {
                status.textContent = "✅ Message envoyé avec succès !";
                form.reset();
            } else {
                status.textContent = "❌ Une erreur est survenue.";
            }
        })
        .catch(() => {
            status.textContent = "❌ Impossible d'envoyer le message.";
        });

    });
};