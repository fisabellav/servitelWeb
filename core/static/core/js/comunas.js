fetch('cargar_comunas_rm_desde_api/')  // Reemplaza con la URL de tu vista Django
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            console.log('Comunas cargadas exitosamente.');
        } else {
            console.error('Error al cargar comunas.');
        }
    })
    .catch(error => console.error('Error:', error));