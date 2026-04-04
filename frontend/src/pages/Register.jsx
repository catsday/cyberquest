import { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { useNavigate, Link } from 'react-router-dom';

export default function Register() {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const { register } = useAuth();
  const nav = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await register(username, email, password);
      nav('/challenges');
    } catch (err) {
      setError(err.response?.data?.detail || 'Registration failed');
    }
  };

  return (
    <div className="auth-form">
      <h2>Register</h2>
      {error && <p className="error">{error}</p>}
      <div className="form-group">
        <input placeholder="Username" value={username} onChange={(e) => setUsername(e.target.value)} />
        <input placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} />
        <input placeholder="Password" type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
        <button onClick={handleSubmit} className="btn-primary">Register</button>
      </div>
      <p className="auth-link">Already have an account? <Link to="/login">Login</Link></p>
    </div>
  );
}
