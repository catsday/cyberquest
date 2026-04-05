import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export default function Navbar() {
  const { user, logout } = useAuth();

  return (
    <nav className="navbar">
      <Link to="/challenges" className="navbar-brand">CyberQuest</Link>
      {user && (
        <div className="navbar-links">
          <Link to="/challenges">Challenges</Link>
          <Link to="/leaderboard">Leaderboard</Link>
          <Link to="/teams">Teams</Link>
          {user.is_admin && <Link to="/admin" className="admin-link">Admin</Link>}
          <span className="user-info">{user.username} ({user.score} pts)</span>
          <button onClick={logout} className="btn-outline">Logout</button>
        </div>
      )}
    </nav>
  );
}
