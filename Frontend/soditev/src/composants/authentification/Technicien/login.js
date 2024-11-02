// LoginForm.js
import React, { useState } from 'react';
import authService from '../../../services/authentification/technicien/login';
import technicienService from '../../../services/authentification/technicien/register';
import '../../../styles/login.css';
import { useNavigate, Link } from 'react-router-dom';

const LoginForm = () => {
  const navigate = useNavigate();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [isSignUpActive, setSignUpActive] = useState(false);

  const handleSignInClick = () => {
    setSignUpActive(false);
    setError('');
  };

  const handleSignUpClick = () => {
    setSignUpActive(true);
    setError('');
  };

  const handleSubmitLogin = async (e) => {
    e.preventDefault();
    setError('');

    try {
      await authService.technicienLogin(username, password);
      navigate("/home");
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div className={`container ${isSignUpActive ? 'right-panel-active' : ''}`} id="container">
      <div className="form-container sign-up-container">
        {isSignUpActive && <InscriptionTechnicien />}
      </div>

      <div className="form-container sign-in-container">
        <form onSubmit={handleSubmitLogin}>
          <h1>Se connecter</h1>
          <div className="social-container">
            <a href="#" className="social"><i className="fab fa-facebook-f"></i></a>
            <a href="#" className="social"><i className="fab fa-google-plus-g"></i></a>
            <a href="#" className="social"><i className="fab fa-linkedin-in"></i></a>
          </div>
          <span>ou utilisez votre compte</span>
          <input
            type="text"
            placeholder="Nom d'utilisateur"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            className="input-field"
          />
          <input
            type="password"
            placeholder="Mot de passe"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="input-field"
          />
           <Link to="/forgot-password" className="forgot-password">Mot de passe oublié ?</Link>
          <button type="submit" className="btn">Se connecter</button>
          {error && <p className="error">{error}</p>}
        </form>
      </div>

      <Overlay onSignInClick={handleSignInClick} onSignUpClick={handleSignUpClick} />
    </div>
  );
};

const InscriptionTechnicien = () => {
  const [step, setStep] = useState(1);
  const [formData, setFormData] = useState({
    username: '',
    adresse: '',
    telephone: '',
    indicatif_telephone: '',
    photo: null,
    email: '',
    password: ''
  });

  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleFileChange = (e) => {
    setFormData({ ...formData, photo: e.target.files[0] });
  };

  const handleNextStep = () => setStep((prevStep) => prevStep + 1);
  const handlePrevStep = () => setStep((prevStep) => prevStep - 1);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setSuccess(false);

    const data = new FormData();
    for (let key in formData) {
      data.append(key, formData[key]);
    }

    try {
      await technicienService.inscrireTechnicien(data);
      setSuccess(true);
    } catch (error) {
      setError(error.message);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="inscription-form">
      <h1>S'inscrire</h1>
          <div className="social-container">
            <a href="#" className="social"><i className="fab fa-facebook-f"></i></a>
            <a href="#" className="social"><i className="fab fa-google-plus-g"></i></a>
            <a href="#" className="social"><i className="fab fa-linkedin-in"></i></a>
          </div>
          <span>ou créez votre compte</span>
      {step === 1 && (
        <div className="step-content">
          <input type="text" name="username" placeholder="Nom" value={formData.username} onChange={handleChange} required className="input-field" />
          <input type="email" name="email" placeholder="Email" value={formData.email} onChange={handleChange} required className="input-field" />
          <button type="button" className="btn" onClick={handleNextStep}>Suivant</button>
        </div>
      )}
      {step === 2 && (
        <div className="step-content">
          <input type="password" name="password" placeholder="Mot de passe" value={formData.password} onChange={handleChange} required className="input-field" />
          <input type="text" name="adresse" placeholder="Adresse" value={formData.adresse} onChange={handleChange} required className="input-field" />
          <div className='button-container'>
          <button type="button" className="btn" onClick={handlePrevStep}>Précédent</button>
          <button type="button" className="btn" onClick={handleNextStep}>Suivant</button>
          </div>
        </div>
      )}
      {step === 3 && (
        <div className="step-content">
          <div className="phone-input">
            <select name="indicatif_telephone" value={formData.indicatif_telephone} onChange={handleChange} required className="input-field phone-select">
              <option value="">Indicatif</option>
              <option value="+33">+33</option>
              <option value="+221">+221</option>
            </select>
            <input type="text" name="telephone" placeholder="Téléphone" value={formData.telephone} onChange={handleChange} required className="input-field phone-number" />
          </div>
          <div className='button-container'>
          <button type="button" className="btn" onClick={handlePrevStep}>Précédent</button>
          <button type="button" className="btn" onClick={handleNextStep}>Suivant</button>
          </div>
        </div>
      )}
      {step === 4 && (
        <div className="step-content">
          <div className="photo-upload">
            <input type="file" name="photo" id="photo" onChange={handleFileChange} required />
            {formData.photo && <img src={URL.createObjectURL(formData.photo)} alt="Prévisualisation" className="photo-preview" />}
          </div>
          <div className='button-container'>
          <button type="button" id='prev' className="btn" onClick={handlePrevStep}>Précédent</button>
          <button type="submit" className="btn">S'inscrire</button>
          </div>
        </div>
      )}
      {error && <p className="error">{error}</p>}
      {success && <p className="success">Inscription réussie !</p>}
    </form>
  );
};

const Overlay = ({ onSignInClick, onSignUpClick }) => (
  <div className="overlay-container">
    <div className="overlay">
      <div className="overlay-panel overlay-left">
        <h1>Bienvenue de retour !</h1>
        <p>Pour rester connecté, connectez-vous avec vos informations personnelles</p>
        <button className="ghost" onClick={onSignInClick}>Se connecter</button>
      </div>
      <div className="overlay-panel overlay-right">
        <h1>Bonjour !</h1>
        <p>Entrez vos informations personnelles et commencez votre aventure avec nous</p>
        <button className="ghost" onClick={onSignUpClick}>S'inscrire</button>
      </div>
    </div>
  </div>
);

export default LoginForm;
