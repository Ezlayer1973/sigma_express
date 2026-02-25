// Agrega el evento de escucha al formulario de inicio de sesión
document.getElementById('loginForm').addEventListener('submit', async (event) => {
    event.preventDefault(); // Evita que el formulario se envíe de forma predeterminada

    // Obtén los valores de email y password
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const errorMessage = document.getElementById('error-message');

    // Limpia el mensaje de error antes de la nueva solicitud
    errorMessage.textContent = '';

    try {
        // Realiza la solicitud POST al endpoint de inicio de sesión
        const response = await fetch('http://127.0.0.1:8000/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: new URLSearchParams({
                'username': email,
                'password': password
            })
        });

        console.log('Estado de respuesta:', response.status); // Para debug: estado de la respuesta

        if (response.ok) {
            // Si la respuesta es 200 OK, procesar el JSON recibido
            const data = await response.json();
            console.log('Respuesta del servidor:', data); // Para debug: datos completos de la respuesta

            // Verifica que el token esté presente en la respuesta
            if (data.access_token) {
                console.log('Token de acceso:', data.access_token);
                // Redirige a home.html
                window.location.href = 'home.html';
            } else {
                errorMessage.textContent = 'Error: Token no recibido.';
            }
        } else {
            // Si hay un error, muestra el mensaje de error en pantalla
            const data = await response.json();
            errorMessage.textContent = data.detail || 'Error desconocido.';
        }
    } catch (error) {
        // Maneja cualquier error de red
        console.error('Error de conexión:', error);
        errorMessage.textContent = 'Error de conexión. Asegúrate de que el servidor está en funcionamiento.';
    }
});
