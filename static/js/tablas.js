$(function () {
    $('.tabla-datos').DataTable({
        pageLength: 10,
        language: {
            search: 'Buscar:', lengthMenu: 'Mostrar _MENU_ registros',
            info: 'Registros _START_ a _END_ de _TOTAL_', infoEmpty: 'Sin registros',
            infoFiltered: '(filtrados de _MAX_)', zeroRecords: 'No hay coincidencias',
            emptyTable: 'Todavía no hay registros',
            paginate: {first: 'Primero', last: 'Último', next: 'Siguiente', previous: 'Anterior'}
        }
    });
});
