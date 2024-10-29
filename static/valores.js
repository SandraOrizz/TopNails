document.addEventListener('DOMContentLoaded', function() {
    const modal = document.getElementById('aboutUsModal');
    const btn = document.getElementById('aboutUsBtn');
    const span = document.getElementsByClassName('close')[0];
    const valuesList = document.getElementById('valuesList');

    const values = [
        "Calidad en cada servicio.",
        "Innovación constante en tendencias.",
        "Cuidado al cliente con atención personalizada.",
        "Profesionalismo y confianza.",
        "Sostenibilidad en productos y técnicas.",
        "Creatividad en cada diseño.",
        "Higiene y seguridad garantizadas.",
        "Empoderamiento a través de la belleza."
    ];

    values.forEach(value => {
        const li = document.createElement('li');
        li.textContent = value;
        valuesList.appendChild(li);
    });

    btn.onclick = function() {
        modal.style.display = "block";
    }

    span.onclick = function() {
        modal.style.display = "none";
    }

    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }

    const logoutBtn = document.getElementById('logoutBtn');
    logoutBtn.onclick = function() {
        if (confirm('¿Estás seguro de que quieres cerrar sesión?')) {
            window.location.href = '/logout';
        }
    }

    lucide.createIcons();
});