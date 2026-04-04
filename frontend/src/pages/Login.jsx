import { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { useNavigate, Link } from 'react-router-dom';

export default function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const { login } = useAuth();
  const nav = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await login(username, password);
      nav('/challenges');
    } catch {
      setError('Invalid credentials');
    }
  };

  return (
    <div className="auth-form">
      <h2>Login</h2>
      {error && <p className="error">{error}</p>}
      <div className="form-group">
        <input placeholder="Username" value={username} onChange={(e) => setUsername(e.target.value)} />
        <input placeholder="Password" type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
        <button onClick={handleSubmit} className="btn-primary">Login</button>
      </div>
      <p className="auth-link">No account? <Link to="/register">Register</Link></p>
    </div>
  );
}
