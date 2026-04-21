import { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import api from '../api/client';

export default function Teams() {
  const { user } = useAuth();
  const [name, setName] = useState('');
  const [msg, setMsg] = useState('');
  const [msgType, setMsgType] = useState('success');

  const handleAction = async (action) => {
    try {
      const endpoint = action === 'create' ? '/teams/create' : '/teams/join';
      const res = await api.post(endpoint, { name });
      setMsg(`${action === 'create' ? 'Created' : 'Joined'} team "${res.data.name}"! Refresh to see changes.`);
      setMsgType('success');
    } catch (e) {
      setMsg(e.response?.data?.detail || 'Error');
      setMsgType('error');
    }
  };

  return (
    <div className="teams-page">
      <h2>Teams</h2>
      {user?.team_id ? (
        <p>You are in a team (ID: {user.team_id})</p>
      ) : (
        <div className="team-actions">
          <input
            placeholder="Team name"
            value={name}
            onChange={(e) => setName(e.target.value)}
          />
          <button onClick={() => handleAction('create')} className="btn-primary">Create</button>
          <button onClick={() => handleAction('join')} className="btn-outline">Join</button>
        </div>
      )}
      {msg && <p className={msgType === 'error' ? 'error' : 'result-correct'}>{msg}</p>}
    </div>
  );
}
