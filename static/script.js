document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('login-form');
    const usernameInput = document.getElementById('username');
    const passwordInput = document.getElementById('password');

    form.addEventListener('submit', (e) => {
        e.preventDefault();
        
        if (validateForm()) {
            // Aquí iría la lógica de autenticación
            console.log('Formulario enviado');
            alert('Inicio de sesión exitoso!');
        }
    });

    function validateForm() {
        let isValid = true;

        if (usernameInput.value.trim() === '') {
            showError(usernameInput, 'Por favor, ingresa tu nombre de usuario');
            isValid = false;
        } else {
            removeError(usernameInput);
        }

        if (passwordInput.value.trim() === '') {
            showError(passwordInput, 'Por favor, ingresa tu contraseña');
            isValid = false;
        } else {
            removeError(passwordInput);
        }

        return isValid;
    }

    function showError(input, message) {
        const formControl = input.parentElement;
        formControl.classList.add('error');
        const small = document.createElement('small');
        small.innerText = message;
        formControl.appendChild(small);
    }

    function removeError(input) {
        const formControl = input.parentElement;
        if (formControl.classList.contains('error')) {
            formControl.classList.remove('error');
            formControl.removeChild(formControl.lastElementChild);
        }
    }
});