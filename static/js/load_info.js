/**
 * --- VARIABLES GLOBALES DE ESTADO ---
 */
let currentPage = 1;
const recordsPerPage = 6; 
let globalData = [];      
let globalContext = "";   

/**
 * Muestra una notificación Toast con el diseño oficial de Bootstrap
 */
function showToast(title, message, type = 'success') {
    let toastContainer = document.getElementById('toast-container');
    if (!toastContainer) {
        toastContainer = document.createElement('div');
        toastContainer.id = 'toast-container';
        toastContainer.className = 'toast-container position-fixed bottom-0 end-0 p-3';
        document.body.appendChild(toastContainer);
    }

    const toastId = `toast-${Date.now()}`;
    const colorClass = type === 'success' ? 'bg-success' : type === 'danger' ? 'bg-danger' : 'bg-info';
    
    const toastHTML = `
        <div id="${toastId}" class="toast" role="alert" aria-live="assertive" aria-atomic="true">
            <div class="toast-header">
                <div class="rounded me-2 ${colorClass}" style="width: 15px; height: 15px;"></div>
                <strong class="me-auto">${title}</strong>
                <small class="text-body-secondary">ahora</small>
                <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
            <div class="toast-body">
                ${message}
            </div>
        </div>
    `;

    toastContainer.insertAdjacentHTML('beforeend', toastHTML);
    const toastElement = document.getElementById(toastId);
    const toast = new bootstrap.Toast(toastElement, { delay: 3000 });
    toast.show();

    toastElement.addEventListener('hidden.bs.toast', () => toastElement.remove());
}

/**
 * Obtiene los datos del servidor
 */
async function getTeachers(fetchUrl) {
    try {
        const response = await fetch(fetchUrl);
        const result = await response.json();

        let rawData = result.DATA;
        
        if (typeof rawData === 'string') {
            const validJsonString = rawData.replace(/'/g, '"');
            rawData = JSON.parse(validJsonString);
        }

        showToast("Servidor", "Datos sincronizados correctamente", "success");
        return rawData; 
    } catch (error) {
        showToast("Error", "No se pudo obtener la información", "danger");
        console.error("Fetch Error:", error);
        return [];
    }
}

/**
 * Renderiza la tabla dinámica y los controles de paginación
 */
function renderList(context, data) {
    globalData = data;
    globalContext = context;
    const renderArea = document.getElementById("render-area");

    if (!data || data.length === 0) {
        renderArea.innerHTML = `<p class="text-center text-muted my-5">No se encontraron registros.</p>`;
        return;
    }

    const totalPages = Math.ceil(data.length / recordsPerPage);
    
    // SEGURIDAD: Ajustar página actual si sale de los límites
    if (currentPage < 1) currentPage = 1;
    if (currentPage > totalPages) currentPage = totalPages;

    const startIndex = (currentPage - 1) * recordsPerPage;
    const paginatedItems = data.slice(startIndex, startIndex + recordsPerPage);

    let headers = "";
    switch (context) {
        case "profesor":
            headers = `<th>ID</th><th>Nombre</th><th>Especialidad</th><th>Correo</th><th>Contratación</th>`;
            break;
        case "alumno":
            headers = `<th>ID</th><th>Nombre</th><th>Correo</th><th>Grado</th>`;
            break;
        case "curso":
            headers = `<th>ID</th><th>Nombre Curso</th><th>ID Profesor</th>`;
            break;
        default:
            headers = `<th>ID</th><th>Nombre</th><th>Información</th>`;
    }

    let tableHTML = `
        <div class="table-responsive" style="min-height: 380px;">
            <table class="table table-hover align-middle shadow-sm bg-white mb-0">
                <thead class="table-success"><tr>${headers}</tr></thead>
                <tbody>`;

    paginatedItems.forEach(item => {
        tableHTML += "<tr>";
        switch (context) {
            case "profesor":
                tableHTML += `
                <td><span class="badge bg-secondary">${item.id_profesor}</span></td>
                <td><span class="fw-bold">${item.nombre}</span></td>
                <td>${item.correo}</td>
                <td><span class="text-uppercase small">${item.especialidad}</span></td>
                <td>${new Date(item.fecha_contratacion).toLocaleDateString()}</td>`;
                break;
            case "alumno":
                tableHTML += `
                <td>${item.id_alumno || item.id}</td>
                <td>${item.nombre}</td>
                <td>${item.correo || '-'}</td>
                <td>${item.grado || '-'}</td>`;
                break;
            case "curso":
                tableHTML += `
                <td>${item.id_curso || item.id}</td>
                <td>${item.nombre_curso}</td>
                <td><span class="badge bg-info text-dark">${item.id_profesor}</span></td>`;
                break;
        }
        tableHTML += "</tr>";
    });
    tableHTML += "</tbody></table></div>";

    const paginationHTML = `
        <nav class="mt-3">
            <ul class="pagination justify-content-center">
                <li class="page-item ${currentPage === 1 ? 'disabled' : ''}">
                    <button class="btn btn-sm btn-outline-success px-3 me-2" 
                            onclick="${currentPage > 1 ? 'changePage(-1)' : ''}" 
                            ${currentPage === 1 ? 'disabled' : ''}>Anterior</button>
                </li>
                <li class="page-item d-flex align-items-center mx-3 small fw-bold">
                    Página ${currentPage} de ${totalPages}
                </li>
                <li class="page-item ${currentPage === totalPages ? 'disabled' : ''}">
                    <button class="btn btn-sm btn-outline-success px-3 ms-2" 
                            onclick="${currentPage < totalPages ? 'changePage(1)' : ''}" 
                            ${currentPage === totalPages ? 'disabled' : ''}>Siguiente</button>
                </li>
            </ul>
        </nav>`;

    renderArea.innerHTML = tableHTML + paginationHTML;
}

/**
 * Maneja el cambio de página con validación de límites
 */
window.changePage = function(step) {
    const totalPages = Math.ceil(globalData.length / recordsPerPage);
    const newPage = currentPage + step;

    // VALIDACIÓN CRÍTICA: Impedir que baje de 1 o suba del máximo
    if (newPage >= 1 && newPage <= totalPages) {
        currentPage = newPage;
        showToast("Navegación", `Cargando página ${currentPage}`, "info");
        renderList(globalContext, globalData);
    }
};

/**
 * Inicialización al cargar el DOM
 */
document.addEventListener("DOMContentLoaded", () => {
    const button = document.getElementById("load-config");
    const renderArea = document.getElementById("render-area");
    const actualPath = window.location.pathname;

    button.addEventListener("click", async () => {
        let fetchUrl = null;
        let context = "";

        if (actualPath.startsWith("/profesores")) {
            fetchUrl = "/obtain-profesores";
            context = "profesor";
        } else if (actualPath.startsWith("/alumnos")) {
            fetchUrl = "/obtain-alumnos";
            context = "alumno";
        } else if (actualPath.startsWith("/cursos")) {
            fetchUrl = "/obtain-cursos";
            context = "curso";
        }

        if (fetchUrl) {
            renderArea.innerHTML = `
                <div class="d-flex justify-content-center my-5">
                    <div class="spinner-border text-success" style="width: 3rem; height: 3rem;" role="status"></div>
                </div>`;

            currentPage = 1; 
            const data = await getTeachers(fetchUrl);
            
            if (data) {
                renderList(context, data);
            }
        } else {
            showToast("Aviso", "Ruta no configurada para carga de datos", "warning");
        }
    });
});