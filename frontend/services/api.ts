/**
 * Servicio centralizado para peticiones a la API de Django.
 */

const API_BASE_URL = '/api';

export const apiService = {
    /**
     * Obtiene la lista de cátedras desde el backend.
     */
    async getCatedras() {
        const response = await fetch(`${API_BASE_URL}/catedras/`);
        if (!response.ok) throw new Error('Error al obtener cátedras');
        const data = await response.json();
        return data.results; // DRF devuelve los resultados en la propiedad 'results' debido a la paginación
    },

    /**
     * Obtiene la lista de grupos de scraping.
     */
    async getGrupos() {
        const response = await fetch(`${API_BASE_URL}/grupos/`);
        if (!response.ok) throw new Error('Error al obtener grupos');
        const data = await response.json();
        return data.results;
    },

    /**
     * Obtiene las tareas de scraping.
     */
    async getTareas() {
        const response = await fetch(`${API_BASE_URL}/tareas/`);
        if (!response.ok) throw new Error('Error al obtener tareas');
        const data = await response.json();
        return data.results;
    },

    /**
     * Obtiene las sesiones de scraping.
     */
    async getSesiones() {
        const response = await fetch(`${API_BASE_URL}/sesiones/`);
        if (!response.ok) throw new Error('Error al obtener sesiones');
        const data = await response.json();
        return data.results;
    },

    /**
     * Obtiene los posts scrapeados.
     */
    async getPosts() {
        const response = await fetch(`${API_BASE_URL}/posts/`);
        if (!response.ok) throw new Error('Error al obtener posts');
        const data = await response.json();
        return data.results;
    }
};
