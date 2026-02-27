document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("register-form");
    const sameAddressCheckbox = document.getElementById("sameAddress");

    // Campos de facturación
    const direccionFac = document.getElementById("direccion_fac");
    const localidadFac = document.getElementById("localidad_fac");
    const codPostalFac = document.getElementById("cod_postal_fac");
    const provinciaFac = document.getElementById("provincia_fac");

    // Campos de envío
    const direccionEnv = document.getElementById("direccion_env");
    const localidadEnv = document.getElementById("localidad_env");
    const codPostalEnv = document.getElementById("cod_postal_env");
    const provinciaEnv = document.getElementById("provincia_env");

    // Función para copiar o limpiar los campos de envío
    sameAddressCheckbox.addEventListener("change", function () {
        if (sameAddressCheckbox.checked) {
            direccionEnv.value = direccionFac.value;
            localidadEnv.value = localidadFac.value;
            codPostalEnv.value = codPostalFac.value;
            provinciaEnv.value = provinciaFac.value;
        } else {
            direccionEnv.value = "";
            localidadEnv.value = "";
            codPostalEnv.value = "";
            provinciaEnv.value = "";
        }
    });

    // Manejo del envío del formulario
    form.addEventListener("submit", async function (event) {
        event.preventDefault();
        
        // Obtener los valores de los campos del formulario
        const userData = {
            email: document.getElementById("email").value,
            password: document.getElementById("password").value,
            apellido: document.getElementById("apellido").value,
            nombres: document.getElementById("nombres").value,
            direccion_fac: direccionFac.value,
            localidad_fac: localidadFac.value,
            cod_postal_fac: codPostalFac.value,
            provincia_fac: provinciaFac.value,
            telefono: document.getElementById("telefono").value,
            direccion_env: direccionEnv.value,
            localidad_env: localidadEnv.value,
            cod_postal_env: codPostalEnv.value,
            provincia_env: provinciaEnv.value,
            tipo_doc: document.getElementById("tipo_doc").value,
            nro_doc: Number(document.getElementById("nro_doc").value),
            fecha_alta: "2024-08-15T00:00:00",
            baja: false
        };
        

        try {
            const response = await fetch("http://localhost:8000/usersapp", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(userData)
            });

            const result = await response.json();

            if (response.status === 201) {
                alert("Usuario creado exitosamente. Código de usuario: " + result.codigo);
                form.reset();
            } else {
                alert(result.Atención || result.Error || "Error desconocido al crear el usuario.");
            }
        } catch (error) {
            console.error("Error al enviar los datos:", error);
            alert("Error de conexión con el servidor.");
        }
    });
});

// Función para validar que el teléfono contenga solo números
function validarTelefono(event) {
    const telefonoInput = document.getElementById("telefono");
    const telefono = telefonoInput.value;

    // Verifica si el valor ingresado tiene caracteres no numéricos
    if (/[^0-9]/.test(telefono)) {
        telefonoInput.setCustomValidity("Solo se permiten números en el teléfono.");
    } else {
        telefonoInput.setCustomValidity("");
    }
}

// Asignar el evento de validación al campo de teléfono
document.getElementById("telefono").addEventListener("input", validarTelefono);

// Asignar el evento de envío del formulario
document.getElementById("register-form").addEventListener("submit", function(event) {
    const telefono = document.getElementById("telefono").value;
    if (telefono.length < 10) {
        event.preventDefault(); // Evitar el envío si el teléfono es muy corto
        alert("El teléfono debe tener al menos 10 dígitos.");
    }
});
