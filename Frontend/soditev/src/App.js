import React from 'react';
import AdminDashboard from './composants/authentification/Technicien/dashboard';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import ListeTechniciens from './composants/authentification/Technicien/list';
//import LoginForm from './composants/authentification/Technicien/login';


const App = () => {
    return (
        
            
            <Router>
                <div className="App">
            <Routes>
                {/* Route par défaut pour afficher LoginForm */}
                
                {/* Route pour le tableau de bord */}
                <Route path="/home" element={<AdminDashboard/>} /> {/* Page d'accueil */}
                <Route path="/techniciens" element={<ListeTechniciens/>} /> {/* Route vers ListeTechniciens */}
                {/* Route pour les pages non trouvées */}
                <Route path="*" element={<h1>404 - Page non trouvée</h1>} />
            </Routes>
            </div> 
        </Router>
        
        
    );
}

export default App;
