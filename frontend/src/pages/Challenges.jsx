import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import api from '../api/client';

const CATEGORIES = ['all', 'web', 'crypto', 'forensics', 'reversing', 'osint'];
const DIFFICULTIES = ['all', 'easy', 'medium', 'hard'];

export default function Challenges() {
  const [challenges, setChallenges] = useState([]);
  const [category, setCategory] = useState('all');
  const [difficulty, setDifficulty] = useState('all');

  useEffect(() => {
    const params = {};
    if (category !== 'all') params.category = category;
    if (difficulty !== 'all') params.difficulty = difficulty;
    api.get('/challenges/', { params }).then((r) => setChallenges(r.data));
  }, [category, difficulty]);

  return (
    <div>
      <h2>Challenges</h2>
      <div className="filters">
        {CATEGORIES.map((c) => (
          <button
            key={c}
            onClick={() => setCategory(c)}
            className={category === c ? 'filter-btn active' : 'filter-btn'}
          >
            {c}
          </button>
        ))}
        <span className="filter-sep">|</span>
        {DIFFICULTIES.map((d) => (
          <button
            key={d}
            onClick={() => setDifficulty(d)}
            className={difficulty === d ? 'filter-btn active' : 'filter-btn'}
          >
            {d}
          </button>
        ))}
      </div>
      <div className="challenge-grid">
        {challenges.map((ch) => (
          <Link to={`/challenges/${ch.id}`} key={ch.id} className="challenge-card">
            <h3>{ch.title}</h3>
            <p className="challenge-meta">{ch.category} · {ch.difficulty} · {ch.points} pts</p>
          </Link>
        ))}
        {challenges.length === 0 && <p className="muted">No challenges found.</p>}
      </div>
    </div>
  );
}
