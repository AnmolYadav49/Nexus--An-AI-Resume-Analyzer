import React, { useState, useEffect, useRef } from 'react';
import { FLASK_BASE } from './config.js';
import './index.css';

// ── State machine constants ────────────────────────────────────────────────
const STATE = {
  IDLE: 'idle',
  LOADING: 'loading',
  SUCCESS: 'success',
  ERROR_BACKEND: 'error_backend',
  ERROR_INVALID_FILE: 'error_invalid_file',
  ERROR_ANALYSIS: 'error_analysis',
};

// ── Sub-components ─────────────────────────────────────────────────────────

function ErrorCard({ state, onRetry }) {
  const messages = {
    [STATE.ERROR_BACKEND]: {
      icon: '🔌',
      title: 'Backend Offline',
      body: 'Cannot reach the Flask server on port 5000. Please make sure it is running.',
    },
    [STATE.ERROR_INVALID_FILE]: {
      icon: '📄',
      title: 'Invalid File',
      body: 'Only PDF and DOCX files are supported. Please upload a valid resume.',
    },
    [STATE.ERROR_ANALYSIS]: {
      icon: '⚠️',
      title: 'Analysis Failed',
      body: 'Something went wrong during processing. Please try again.',
    },
  };
  const msg = messages[state] || messages[STATE.ERROR_ANALYSIS];
  return (
    <div className="glass-panel" style={{ padding: '40px', textAlign: 'center', maxWidth: '500px', margin: '0 auto' }}>
      <div style={{ fontSize: '3rem', marginBottom: '16px' }}>{msg.icon}</div>
      <h3 style={{ color: 'var(--text-main)', marginBottom: '10px' }}>{msg.title}</h3>
      <p style={{ color: 'var(--text-muted)', marginBottom: '24px', fontSize: '0.95rem' }}>{msg.body}</p>
      <button className="btn-primary" onClick={onRetry}>Try Again</button>
    </div>
  );
}

function LoadingState() {
  const steps = ['Extracting text…', 'Predicting role…', 'Matching skills…', 'Generating insights…'];
  const [step, setStep] = useState(0);
  useEffect(() => {
    const t = setInterval(() => setStep(s => (s + 1) % steps.length), 1200);
    return () => clearInterval(t);
  }, []);
  return (
    <div style={{ textAlign: 'center', padding: '60px 20px' }}>
      <div className="loading-ring" style={{ margin: '0 auto 28px' }} />
      <h3 style={{ color: 'var(--text-main)', marginBottom: '8px' }}>Analysing Resume</h3>
      <p style={{ color: 'var(--text-muted)', fontSize: '0.95rem', minHeight: '24px' }}>{steps[step]}</p>
    </div>
  );
}

function ResultPanel({ result }) {
  if (!result || !result.success) return null;

  return (
    <section style={{ display: 'flex', flexDirection: 'column', gap: '30px' }}>
      
      {/* Overview Cards Grid */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '20px' }}>
        {/* Role & Score Card */}
        <div className="glass-panel" style={{ padding: '24px', textAlign: 'center' }}>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.75rem', textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: '8px' }}>
            Best Suitable Role
          </p>
          <h3 style={{ fontSize: '1.4rem', color: 'var(--text-main)', fontWeight: 700, marginBottom: '8px' }}>
            {result.predicted_role}
          </h3>
          <div style={{
            display: 'inline-block',
            padding: '4px 12px',
            borderRadius: '20px',
            fontSize: '0.85rem',
            fontWeight: 600,
            background: 'rgba(0, 206, 201, 0.12)',
            color: '#00cec9',
            border: '1px solid rgba(0, 206, 201, 0.25)'
          }}>
            ● {result.confidence}% confidence
          </div>
        </div>

        {/* ATS Score Card */}
        <div className="glass-panel" style={{ padding: '24px', textAlign: 'center', display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.75rem', textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: '8px' }}>
            ATS Match Rating
          </p>
          <div style={{ fontSize: '2.4rem', fontWeight: 800, color: 'var(--text-main)', marginBottom: '4px' }}>
            {result.ats_score}%
          </div>
          <div style={{
            height: '6px',
            width: '80%',
            background: 'rgba(255,255,255,0.08)',
            borderRadius: '3px',
            margin: '8px auto 0',
            overflow: 'hidden'
          }}>
            <div style={{
              height: '100%',
              width: `${result.ats_score}%`,
              background: 'var(--primary-gradient)',
              borderRadius: '3px'
            }} />
          </div>
        </div>
      </div>

      {/* DNA Matrix */}
      {result.resume_dna && (
        <div className="glass-panel" style={{ padding: '28px' }}>
          <h4 style={{ fontSize: '1.1rem', marginBottom: '20px', color: 'var(--text-main)', fontWeight: 600 }}>
            Resume DNA Profile
          </h4>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
            {Object.entries(result.resume_dna).map(([metric, val]) => (
              <div key={metric}>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '6px', fontSize: '0.85rem' }}>
                  <span style={{ color: 'var(--text-muted)', textTransform: 'capitalize' }}>
                    {metric.replace('_', ' ')}
                  </span>
                  <span style={{ fontWeight: 600, color: 'var(--text-main)' }}>
                    {val}%
                  </span>
                </div>
                <div style={{ height: '6px', background: 'rgba(255,255,255,0.05)', borderRadius: '3px', overflow: 'hidden' }}>
                  <div style={{
                    height: '100%',
                    width: `${val}%`,
                    background: 'var(--accent)',
                    borderRadius: '3px'
                  }} />
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Captured Competencies & Vulnerabilities */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '20px' }}>
        {/* Matched Skills */}
        <div className="glass-panel" style={{ padding: '24px' }}>
          <h4 style={{ fontSize: '1rem', color: 'var(--text-main)', marginBottom: '16px', display: 'flex', alignItems: 'center', gap: '8px', fontWeight: 600 }}>
            <span style={{ color: '#00cec9' }}>✔</span> Captured Competencies
          </h4>
          {result.matched_skills && result.matched_skills.length > 0 ? (
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
              {result.matched_skills.map((s, idx) => (
                <span key={idx} style={{
                  padding: '4px 10px',
                  borderRadius: '6px',
                  fontSize: '0.8rem',
                  fontWeight: 500,
                  background: 'rgba(0, 206, 201, 0.08)',
                  color: '#00cec9',
                  border: '1px solid rgba(0, 206, 201, 0.15)',
                  textTransform: 'capitalize'
                }}>
                  {s}
                </span>
              ))}
            </div>
          ) : (
            <p style={{ color: 'var(--text-muted)', fontSize: '0.85rem' }}>No technical entities captured.</p>
          )}
        </div>

        {/* Missing Skills */}
        <div className="glass-panel" style={{ padding: '24px' }}>
          <h4 style={{ fontSize: '1rem', color: 'var(--text-main)', marginBottom: '16px', display: 'flex', alignItems: 'center', gap: '8px', fontWeight: 600 }}>
            <span style={{ color: '#ff7675' }}>✖</span> Identified Vulnerabilities
          </h4>
          {result.missing_skills && result.missing_skills.length > 0 ? (
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
              {result.missing_skills.map((s, idx) => (
                <span key={idx} style={{
                  padding: '4px 10px',
                  borderRadius: '6px',
                  fontSize: '0.8rem',
                  fontWeight: 500,
                  background: 'rgba(255, 118, 117, 0.08)',
                  color: '#ff7675',
                  border: '1px solid rgba(255, 118, 117, 0.15)',
                  textTransform: 'capitalize'
                }}>
                  {s}
                </span>
              ))}
            </div>
          ) : (
            <p style={{ color: 'var(--text-muted)', fontSize: '0.85rem' }}>Complete keyword saturation.</p>
          )}
        </div>
      </div>

      {/* Dynamic Suggestions */}
      {result.suggestions && result.suggestions.length > 0 && (
        <div className="glass-panel" style={{ padding: '28px' }}>
          <h4 style={{ fontSize: '1.1rem', marginBottom: '16px', color: 'var(--text-main)', fontWeight: 600 }}>
            Improvement Directives
          </h4>
          <ul style={{ paddingLeft: '20px', display: 'flex', flexDirection: 'column', gap: '10px' }}>
            {result.suggestions.map((s, idx) => (
              <li key={idx} style={{ color: 'var(--text-muted)', fontSize: '0.9rem', lineHeight: 1.6 }}>
                {s}
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Enhanced Bullets */}
      {result.enhanced_bullets && result.enhanced_bullets.length > 0 && (
        <div className="glass-panel" style={{ padding: '28px' }}>
          <h4 style={{ fontSize: '1.1rem', marginBottom: '16px', color: 'var(--text-main)', fontWeight: 600 }}>
            Enhanced Bullets (AI Polish)
          </h4>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
            {result.enhanced_bullets.map((b, idx) => (
              <p key={idx} style={{
                color: 'var(--text-muted)',
                fontSize: '0.9rem',
                lineHeight: 1.6,
                margin: 0,
                paddingLeft: '12px',
                borderLeft: '2px solid var(--accent)'
              }}>
                {b}
              </p>
            ))}
          </div>
        </div>
      )}

    </section>
  );
}

// ── Main App ───────────────────────────────────────────────────────────────

export default function App() {
  const [file, setFile] = useState(null);
  const [isHovering, setIsHovering] = useState(false);
  const [appState, setAppState] = useState(STATE.IDLE);
  const [result, setResult] = useState(null);
  const fileInputRef = useRef(null);

  const handleDragOver = e => { e.preventDefault(); setIsHovering(true); };
  const handleDragLeave = () => setIsHovering(false);
  const handleDrop = e => {
    e.preventDefault();
    setIsHovering(false);
    const dropped = e.dataTransfer.files?.[0];
    if (dropped) setFile(dropped);
  };

  const handleAnalyze = async () => {
    if (!file) return;
    const fileExt = file.name.split('.').pop().toLowerCase();
    if (fileExt !== 'pdf' && fileExt !== 'docx') {
      setAppState(STATE.ERROR_INVALID_FILE);
      return;
    }

    setAppState(STATE.LOADING);

    try {
      const formData = new FormData();
      formData.append('resume', file);

      const res = await fetch(`${FLASK_BASE}/api/analyze`, {
        method: 'POST',
        body: formData,
      });

      if (!res.ok) {
        throw new Error('Flask backend returned an error');
      }

      const data = await res.json();
      if (!data.success) {
        throw new Error(data.error || 'Analysis failed');
      }

      setResult(data);
      setAppState(STATE.SUCCESS);

    } catch (err) {
      console.error(err);
      setAppState(STATE.ERROR_ANALYSIS);
    }
  };

  const handleReset = () => {
    setFile(null);
    setResult(null);
    setAppState(STATE.IDLE);
  };

  return (
    <div style={{ maxWidth: '900px', margin: '0 auto', padding: '48px 20px' }}>

      {/* Header */}
      <header style={{ textAlign: 'center', marginBottom: '48px' }}>
        <div style={{ display: 'inline-flex', alignItems: 'center', gap: '8px', background: 'rgba(108,92,231,0.12)', border: '1px solid rgba(108,92,231,0.25)', borderRadius: '20px', padding: '4px 14px', marginBottom: '20px', fontSize: '0.8rem', color: 'rgba(255,255,255,0.5)' }}>
          <span style={{ background: 'var(--primary-gradient)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent', fontWeight: 700 }}>Nexus Core v2</span>
          <span>·</span>
          <span>Resume Intelligence Engine</span>
        </div>
        <h1 style={{ fontSize: 'clamp(2rem, 5vw, 3.2rem)', fontWeight: 800, marginBottom: '14px', lineHeight: 1.1 }}>
          <span style={{ background: 'var(--primary-gradient)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>Elevate</span> Your Resume
        </h1>
        <p style={{ color: 'var(--text-muted)', fontSize: '1.05rem', maxWidth: '520px', margin: '0 auto', lineHeight: 1.6 }}>
          AI-powered analysis that rewrites, quantifies, and perfectly formats your experience.
        </p>
      </header>

      {/* State-driven content */}
      {appState === STATE.IDLE && (
        <main style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '24px' }}>
          {/* Drop zone */}
          <div
            className="glass-panel drop-zone"
            style={{
              width: '100%', maxWidth: '580px', padding: '60px 40px', textAlign: 'center',
              border: isHovering ? '2px dashed var(--accent)' : '1px solid var(--panel-border)',
              boxShadow: isHovering ? '0 0 40px rgba(108,92,231,0.2)' : 'none',
              transition: 'all 0.3s ease', cursor: 'pointer', position: 'relative'
            }}
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onDrop={handleDrop}
            onClick={() => fileInputRef.current?.click()}
          >
            <input ref={fileInputRef} type="file" accept=".pdf,.docx" style={{ display: 'none' }}
              onChange={e => setFile(e.target.files[0])} />
            <div style={{ fontSize: '3rem', marginBottom: '16px', transition: 'transform 0.3s', transform: isHovering ? 'scale(1.1)' : 'scale(1)' }}>📄</div>
            {file ? (
              <div>
                <h3 style={{ color: 'var(--text-main)', marginBottom: '6px', fontSize: '1.1rem' }}>{file.name}</h3>
                <p style={{ color: 'var(--text-muted)', fontSize: '0.85rem' }}>Ready to analyse · Click to change</p>
              </div>
            ) : (
              <div>
                <h3 style={{ color: 'var(--text-main)', marginBottom: '8px' }}>Drag & Drop your Resume</h3>
                <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem' }}>PDF or DOCX format · up to 5 MB</p>
              </div>
            )}
          </div>

          {/* Action */}
          <button
            id="analyze-btn"
            className="btn-primary"
            onClick={handleAnalyze}
            disabled={!file}
            style={{ width: '220px', fontSize: '1rem' }}
          >
            Enhance with AI ✨
          </button>

          {/* Go to full analyzer */}
          <p style={{ color: 'var(--text-muted)', fontSize: '0.85rem' }}>
            Want the full ATS analysis?{' '}
            <a href="http://127.0.0.1:5000/" style={{ color: 'var(--accent)', textDecoration: 'none' }}>
              Open full analyzer →
            </a>
          </p>
        </main>
      )}

      {appState === STATE.LOADING && <LoadingState />}

      {[STATE.ERROR_BACKEND, STATE.ERROR_INVALID_FILE, STATE.ERROR_ANALYSIS].includes(appState) && (
        <ErrorCard state={appState} onRetry={handleReset} />
      )}

      {appState === STATE.SUCCESS && (
        <div>
          <ResultPanel result={result} />
          <div style={{ textAlign: 'center', marginTop: '28px' }}>
            <button className="btn-primary" onClick={handleReset} style={{ background: 'rgba(255,255,255,0.06)', boxShadow: 'none', border: '1px solid var(--panel-border)' }}>
              ← Analyse Another Resume
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
