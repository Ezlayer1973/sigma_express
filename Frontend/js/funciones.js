document.getElementById("formulario").addEventListener("submit", async function(event) {
  event.preventDefault();

  const expediente = document.getElementById("expediente").value;
  const resultadoDiv = document.getElementById("resultado");
  const errorDiv = document.getElementById("error");

  resultadoDiv.style.display = "none";
  resultadoDiv.innerHTML = "";
  errorDiv.innerText = "";

  try {
    const response = await fetch(`http://127.0.0.1:8000/expedientes/${expediente}`);
    if (!response.ok) {
      throw new Error("No se encontró el expediente.");
    }

    const data = await response.json();
    const datos = data.datos;

    resultadoDiv.innerHTML = `
      <strong>Fecha:</strong> ${datos[0]}<br>
      <strong>Descripción:</strong> ${datos[1]}<br>
      <strong>Iniciador:</strong> ${datos[2]}<br>
      <strong>Estado:</strong> ${datos[4]}<br>
      <strong>Última actualización:</strong> ${datos[5]}
    `;
    resultadoDiv.style.display = "block";
  } catch (error) {
    errorDiv.innerText = error.message;
  }
});
