document.addEventListener("DOMContentLoaded", () => {
    /* ================================================================
       1. SISTEMA DE TEMA (MODO OSCURO / CLARO)
       ================================================================ 
    */
    const themeToggle = document.getElementById('btnTema');
    const body = document.body;

    // Iconos SVG (Geometría limpia y técnica)
    const iconSol = `
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="12" cy="12" r="5"></circle>
            <line x1="12" y1="1" x2="12" y2="3"></line>
            <line x1="12" y1="21" x2="12" y2="23"></line>
            <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line>
            <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line>
            <line x1="1" y1="12" x2="3" y2="12"></line>
            <line x1="21" y1="12" x2="23" y2="12"></line>
            <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line>
            <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line>
        </svg>`;

    const iconLuna = `
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path>
        </svg>`;

    const updateButtonIcon = (isDark) => {
        themeToggle.innerHTML = isDark ? iconSol : iconLuna;
    };

    // PERSISTENCIA: Revisar si el usuario ya había elegido un tema anteriormente
    if (localStorage.getItem('tema') === 'oscuro') {
        body.classList.add('dark-mode');
        updateButtonIcon(true);
    } else {
        updateButtonIcon(false);
    }

    // Evento Click: Alternar clase 'dark-mode' y guardar preferencia
    themeToggle.addEventListener('click', () => {
        const isDark = body.classList.toggle('dark-mode');
        localStorage.setItem('tema', isDark ? 'oscuro' : 'claro');
        updateButtonIcon(isDark);
        mostrarNotificacion(isDark ? "Modo Oscuro Activado" : "Modo Claro Activado");
    });

    /* ================================================================
       2. SISTEMA DE NOTIFICACIONES (TOASTS)
       ================================================================ 
       Crea pequeñas alertas flotantes que desaparecen automáticamente.
    */
    function mostrarNotificacion(mensaje) {
        let container = document.getElementById("toast-container");
        // Crear contenedor si no existe
        if (!container) {
            container = document.createElement("div");
            container.id = "toast-container";
            document.body.appendChild(container);
        }

        const toast = document.createElement("div");
        toast.className = "toast";
        toast.innerText = mensaje;
        
        container.appendChild(toast);

        // Eliminar notificación después de 3 segundos
        setTimeout(() => {
            toast.style.opacity = "0"; // Efecto desvanecer
            setTimeout(() => toast.remove(), 500); // Eliminar del DOM
        }, 3000);
    }

    // Detectar si la URL tiene el parámetro (viene del server.py tras enviar formulario)
    if (new URLSearchParams(window.location.search).get('exito')) {
        mostrarNotificacion("¡Mensaje enviado con éxito!");
    }

    /* ================================================================
       3. VALIDACIONES DE FORMULARIO
       ================================================================ 
    */
    const contactoForm = document.querySelector('.form-contacto');
    if (contactoForm) {
        contactoForm.addEventListener('submit', (e) => {
            const emailInput = document.getElementById('email_contacto');
            // Validación extra simple además del 'type=email' de HTML
            if (emailInput && !emailInput.value.includes('.')) {
                alert("Por favor, ingresa un correo electrónico válido (ejemplo@dominio.com).");
                e.preventDefault(); // Detener el envío si está mal
            }
        });
    }
});