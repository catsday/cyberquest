import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import api from '../api/client';

export default function ChallengeDetail() {
  const { id } = useParams();
  const [challenge, setChallenge] = useState(null);
  const [flag, setFlag] = useState('');
  const [result, setResult] = useState(null);
  const [hints, setHints] = useState([]);

  useEffect(() => {
    api.get(`/challenges/${id}`).then((r) => setChallenge(r.data));
    api.get(`/challenges/${id}/hints`).then((r) => setHints(r.data));
  }, [id]);

  const submitFlag = async () => {
    try {
      const res = await api.post(`/challenges/${id}/submit`, { flag });
      setResult(res.data);
    } catch {
      setResult({ correct: false, message: 'Submission error' });
    }
  };

  const unlockHint = async (hintId) => {
    if (!confirm('This will deduct points from your score. Continue?')) return;
    try {
      const res = await api.post(`/challenges/${id}/hints/${hintId}/unlock`);
      setHints((prev) =>
        prev.map((h) =>
          h.id === hintId ? { ...h, content: res.data.content, unlocked: true } : h
        )
      );
    } catch (err) {
      alert(err.response?.data?.detail || 'Error unlocking hint');
    }
  };

  if (!challenge) return <div className="loading">Loading...</div>;

  return (
    <div className="challenge-detail">
      <h2>{challenge.title}</h2>
      <p className="challenge-meta">
        {challenge.category} · {challenge.difficulty} · {challenge.points} pts
      </p>
      <p className="challenge-desc">{challenge.description}</p>

      <div className="flag-input">
        <input
          placeholder="FLAG{...}"
          value={flag}
          onChange={(e) => setFlag(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && submitFlag()}
        />
        <button onClick={submitFlag} className="btn-primary">Submit</button>
      </div>

      {result && (
        <p className={result.correct ? 'result-correct' : 'result-wrong'}>
          {result.correct
            ? `Correct! +${result.points_awarded} pts`
            : result.message || 'Wrong flag, try again.'}
        </p>
      )}

      {hints.length > 0 && (
        <div className="hints-section">
          <h3>Hints</h3>
          {hints.map((h) => (
            <div key={h.id} className="hint-card">
              {h.unlocked ? (
                <p>{h.content}</p>
              ) : (
                <button onClick={() => unlockHint(h.id)} className="btn-outline">
                  Unlock Hint #{h.order} (-{h.penalty} pts)
                </button>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
