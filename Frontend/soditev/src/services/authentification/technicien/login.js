import apiClient from '../../../utils/apiClient';

const technicienLogin = async (username, password) => {
    try {
        const response = await apiClient.post('connexion/', {
            username,
            password,
        });

        // Stocker le token dans le local storage
        localStorage.setItem('token', response.data.token);

        return response.data; // Retourne les données (par exemple, le token)
    } catch (error) {
        // Gérer les erreurs
        if (error.response) {
            throw new Error(error.response.data.error || 'Erreur de connexion');
        } else {
            throw new Error('Erreur de connexion');
        }
    }
};

export default {
    technicienLogin,
};
