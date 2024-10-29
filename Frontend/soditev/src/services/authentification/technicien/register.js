import apiClient from '../../../utils/apiClient'; // Assure-toi que le chemin est correct

const API_URL = 'inscription/'; // Remplace ceci par l'URL appropriée de ton API

// Fonction d'inscription du technicien
const inscrireTechnicien = async (formData) => {
    try {
        const response = await apiClient.post(API_URL, formData, {
            headers: {
                'Content-Type': 'multipart/form-data', // Si tu envoies des fichiers
            }
        });
        return response.data; // Retourne les données de réponse en cas de succès
    } catch (error) {
        // Gérer les erreurs
        if (error.response) {
            // La requête a été faite et le serveur a répondu avec un code d'état
            throw new Error(error.response.data.detail || 'Erreur lors de l\'inscription');
        } else if (error.request) {
            // La requête a été faite mais aucune réponse n'a été reçue
            throw new Error('Erreur réseau, veuillez réessayer plus tard');
        } else {
            // Quelque chose s'est mal passé lors de la configuration de la requête
            throw new Error('Erreur lors de l\'inscription');
        }
    }
};

export default {
    inscrireTechnicien,
};