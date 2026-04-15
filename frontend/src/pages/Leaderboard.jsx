import { useState, useEffect } from 'react';
import api from '../api/client';

export default function Leaderboard() {
  const [players, setPlayers] = useState([]);
  const [tab, setTab] = useState('individual');
  const [teams, setTeams] = useState([]);

  useEffect(() => {
    api.get('/leaderboard/').then((r) => setPlayers(r.data));
    api.get('/teams/leaderboard').then((r) => setTeams(r.data));
  }, []);

  return (
    <div>
      <h2>Leaderboard</h2>
      <div className="filters" style={{ marginBottom: '1rem' }}>
        <button
          className={tab === 'individual' ? 'filter-btn active' : 'filter-btn'}
          onClick={() => setTab('individual')}
        >
          Individual
        </button>
        <button
          className={tab === 'teams' ? 'filter-btn active' : 'filter-btn'}
          onClick={() => setTab('teams')}
        >
          Teams
        </button>
      </div>

      <table className="leaderboard-table">
        <thead>
          <tr>
            <th>#</th>
            <th>{tab === 'individual' ? 'Player' : 'Team'}</th>
            <th style={{ textAlign: 'right' }}>Score</th>
          </tr>
        </thead>
        <tbody>
          {tab === 'individual'
            ? players.map((p) => (
                <tr key={p.rank}>
                  <td>{p.rank}</td>
                  <td>{p.username}</td>
                  <td className="score">{p.score}</td>
                </tr>
              ))
            : teams.map((t, i) => (
                <tr key={t.team}>
                  <td>{i + 1}</td>
                  <td>{t.team}</td>
                  <td className="score">{t.score}</td>
                </tr>
              ))}
        </tbody>
      </table>
    </div>
  );
}
