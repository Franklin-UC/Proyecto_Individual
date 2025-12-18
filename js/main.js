document.addEventListener("DOMContentLoaded", () => {
    // --- 1. Configuración de Modo Oscuro ---
    const themeToggle = document.getElementById('btnTema');
    const body = document.body;

    const updateButtonText = (isDark) => {
        themeToggle.textContent = isDark ? "☀️" : "🌙";
    };

    // Cargar preferencia guardada
    if (localStorage.getItem('tema') === 'oscuro') {
        body.classList.add('dark-mode');
        updateButtonText(true);
    }

    themeToggle.addEventListener('click', () => {
        const isDark = body.classList.toggle('dark-mode');
        localStorage.setItem('tema', isDark ? 'oscuro' : 'claro');
        updateButtonText(isDark);
        mostrarNotificacion(isDark ? "Modo oscuro activado" : "Modo claro activado");
    });

    // --- 2. Sistema de Notificaciones (Toasts) ---
    function mostrarNotificacion(mensaje) {
        let container = document.getElementById("toast-container");
        if (!container) {
            container = document.createElement("div");
            container.id = "toast-container";
            document.body.appendChild(container);
        }

        const toast = document.createElement("div");
        toast.className = "toast";
        toast.innerText = mensaje;
        
        container.appendChild(toast);

        setTimeout(() => {
            toast.style.opacity = "0";
            setTimeout(() => toast.remove(), 500);
        }, 3000);
    }

    // Detectar éxito en el envío del formulario 
    if (new URLSearchParams(window.location.search).get('exito')) {
        mostrarNotificacion("¡Mensaje enviado con éxito!");
    }

    // --- 3. Validación de Formulario ---
    const contactoForm = document.querySelector('.form-contacto');
    if (contactoForm) {
        contactoForm.addEventListener('submit', (e) => {
            const emailInput = document.getElementById('email_contacto');
            if (emailInput && !emailInput.value.includes('.')) {
                alert("Por favor, ingresa un correo electrónico válido (ejemplo@dominio.com).");
                e.preventDefault();
            }
        });
    }
});