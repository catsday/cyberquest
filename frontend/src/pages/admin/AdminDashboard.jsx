import { useState, useEffect } from 'react';
import api from '../../api/client';

const EMPTY = { title: '', description: '', category: 'web', difficulty: 'easy', points: 100, flag: '' };

export default function AdminDashboard() {
  const [challenges, setChallenges] = useState([]);
  const [form, setForm] = useState({ ...EMPTY });
  const [editing, setEditing] = useState(null);
  const [msg, setMsg] = useState('');

  const load = () => api.get('/challenges/').then((r) => setChallenges(r.data));
  useEffect(() => { load(); }, []);

  const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async () => {
    try {
      const payload = { ...form, points: Number(form.points) };
      if (editing) {
        await api.put(`/admin/challenges/${editing}`, payload);
        setMsg('Challenge updated');
      } else {
        await api.post('/admin/challenges', payload);
        setMsg('Challenge created');
      }
      setForm({ ...EMPTY });
      setEditing(null);
      load();
    } catch (e) {
      setMsg(e.response?.data?.detail || 'Error');
    }
  };

  const handleDelete = async (id) => {
    if (!confirm('Delete this challenge?')) return;
    await api.delete(`/admin/challenges/${id}`);
    load();
  };

  const startEdit = (ch) => {
    setEditing(ch.id);
    setForm({ title: ch.title, description: ch.description, category: ch.category, difficulty: ch.difficulty, points: ch.points, flag: '' });
  };

  return (
    <div>
      <h2>Admin Dashboard</h2>

      <div className="admin-form">
        <h3>{editing ? 'Edit Challenge' : 'New Challenge'}</h3>
        <input name="title" placeholder="Title" value={form.title} onChange={handleChange} />
        <textarea name="description" placeholder="Description" value={form.description} onChange={handleChange} rows={3} />
        <div className="admin-row">
          <select name="category" value={form.category} onChange={handleChange}>
            <option value="web">web</option>
            <option value="crypto">crypto</option>
            <option value="forensics">forensics</option>
            <option value="reversing">reversing</option>
            <option value="osint">osint</option>
          </select>
          <select name="difficulty" value={form.difficulty} onChange={handleChange}>
            <option value="easy">easy</option>
            <option value="medium">medium</option>
            <option value="hard">hard</option>
          </select>
          <input name="points" type="number" placeholder="Points" value={form.points} onChange={handleChange} style={{ width: 100 }} />
        </div>
        <input name="flag" placeholder="Flag (e.g. FLAG{...})" value={form.flag} onChange={handleChange} />
        <div className="admin-row">
          <button onClick={handleSubmit} className="btn-primary">
            {editing ? 'Update' : 'Create'}
          </button>
          {editing && (
            <button onClick={() => { setEditing(null); setForm({ ...EMPTY }); }} className="btn-outline">
              Cancel
            </button>
          )}
        </div>
        {msg && <p className="muted">{msg}</p>}
      </div>

      <h3>Existing Challenges ({challenges.length})</h3>
      <table className="leaderboard-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Title</th>
            <th>Category</th>
            <th>Difficulty</th>
            <th>Points</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {challenges.map((ch) => (
            <tr key={ch.id}>
              <td>{ch.id}</td>
              <td>{ch.title}</td>
              <td>{ch.category}</td>
              <td>{ch.difficulty}</td>
              <td>{ch.points}</td>
              <td>
                <button onClick={() => startEdit(ch)} className="btn-small">Edit</button>{' '}
                <button onClick={() => handleDelete(ch.id)} className="btn-small btn-danger">Del</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
