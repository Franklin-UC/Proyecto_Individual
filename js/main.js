document.addEventListener("DOMContentLoaded", () => {
    // --- 1. Modo Oscuro Persistente ---
    const themeToggle = document.getElementById('btnTema');
    const body = document.body;

    // Función para actualizar el texto del botón
    const updateButtonText = (isDark) => {
        themeToggle.textContent = isDark ? "☀️" : "🌙";
    };

    // Carga inicial
    const savedTheme = localStorage.getItem('tema');
    if (savedTheme === 'oscuro') {
        body.classList.add('dark-mode');
        updateButtonText(true);
    }

    themeToggle.addEventListener('click', () => {
        const isDark = body.classList.toggle('dark-mode');
        localStorage.setItem('tema', isDark ? 'oscuro' : 'claro');
        updateButtonText(isDark);
        
        // Si tienes el sistema de notificaciones del proyecto de referencia:
        if (typeof mostrarNotificacion === "function") {
            mostrarNotificacion(isDark ? "Modo oscuro activado" : "Modo claro activado", "info");
        }
    });

    // --- 2. Notificaciones (Toast) ---
    function mostrarNotificacion(mensaje) {
        const container = document.getElementById("toast-container") || (() => {
            const c = document.createElement("div");
            c.id = "toast-container";
            document.body.appendChild(c);
            return c;
        })();
        const toast = document.createElement("div");
        toast.className = "toast";
        toast.innerText = mensaje;
        container.appendChild(toast);
        setTimeout(() => toast.remove(), 3000);
    }

    // Notificación al enviar formulario con éxito
    if (new URLSearchParams(window.location.search).get('exito')) {
        mostrarNotificacion("¡Mensaje enviado con éxito!");
    }

    // --- 3. Validación de Formulario  ---
    const form = document.querySelector("form");
    if (form) {
        form.addEventListener("submit", (e) => {
            const email = document.getElementById("email_contacto").value;
            if (!email.includes("@")) {
                alert("Por favor, ingresa un correo válido.");
                e.preventDefault();
            }
        });
    }
});