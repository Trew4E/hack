import { useState, useEffect, useRef, useCallback } from 'react';
import LightRays from './components/LightRays/LightRays';
import MagicBento, { ParticleCard } from './components/MagicBento/MagicBento';
import './index.css';

const API = 'http://localhost:8000';

function esc(s) {
  const d = document.createElement('div');
  d.textContent = s || '';
  return d.innerHTML;
}

// ═══════════════════════════════════════════
// HEADER
// ═══════════════════════════════════════════
function Header() {
  return (
    <header className="header">
      <div className="header__badge"><span>Agentic AI</span></div>
      <h1 className="header__title">Career Navigator</h1>
      <p className="header__subtitle">
        AI-powered career co-pilot that analyzes your skills, identifies gaps,
        and builds a personalized 30-day learning roadmap.
      </p>
    </header>
  );
}

// ═══════════════════════════════════════════
// ERROR BOX
// ═══════════════════════════════════════════
function ErrorBox({ message, onDismiss }) {
  if (!message) return null;
  return (
    <div className="error-box">
      <p style={{ color: 'var(--accent-rose)', fontWeight: 500 }}>⚠ {message}</p>
      <button className="btn btn--secondary" onClick={onDismiss}
        style={{ marginTop: '0.5rem', fontSize: '0.82rem' }}>Dismiss</button>
    </div>
  );
}

// ═══════════════════════════════════════════
// INPUT STAGE
// ═══════════════════════════════════════════
function InputStage({ onGenerate, roles }) {
  const [resumeText, setResumeText] = useState('');
  const [githubUsername, setGithubUsername] = useState('');
  const [dreamRole, setDreamRole] = useState('');
  const [customRole, setCustomRole] = useState('');
  const [pdfStatus, setPdfStatus] = useState(null);

  const loadSample = async () => {
    try {
      const r = await fetch(API + '/sample-resume');
      const d = await r.json();
      setResumeText(d.resume_text || '');
    } catch {
      setResumeText('Backend not running. Start it with: python -m uvicorn main:app --reload');
    }
  };

  const handlePdfUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;
    setPdfStatus({ text: '⏳ Extracting text...', color: 'var(--text-muted)' });
    try {
      const formData = new FormData();
      formData.append('file', file);
      const res = await fetch(API + '/upload-resume', { method: 'POST', body: formData });
      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.detail || 'Upload failed');
      }
      const data = await res.json();
      setResumeText(data.resume_text || '');
      setPdfStatus({ text: `✓ PDF loaded (${file.name})`, color: 'var(--accent-emerald)' });
    } catch (err) {
      setPdfStatus({ text: `✗ ${err.message}`, color: 'var(--accent-rose)' });
    }
  };

  const handleSubmit = () => {
    const role = dreamRole === '__custom__' ? customRole : dreamRole;
    onGenerate(resumeText, role, githubUsername);
  };

  return (
    <div className="fade-in">
      <ParticleCard
        className="magic-bento-card magic-bento-card--border-glow"
        style={{ backgroundColor: 'rgba(6, 0, 16, 0.4)', backdropFilter: 'blur(24px)', WebkitBackdropFilter: 'blur(24px)', '--glow-color': '132, 0, 255', padding: '2rem', borderRadius: '20px', minHeight: 'auto' }}
        particleCount={12}
        glowColor="132, 0, 255"
        enableTilt={true}
        clickEffect={true}
        enableMagnetism={true}
      >
        <div className="bento-card-inner">
          <h2 className="card__title">🎯 Your Profile</h2>
          <div className="form-group">
            <label>Resume / Profile Text</label>
            <textarea className="textarea" value={resumeText} onChange={e => setResumeText(e.target.value)}
              placeholder="Paste your resume, LinkedIn bio, or project descriptions here..." />
            <div className="btn-row">
              <button className="btn btn--secondary" onClick={loadSample}>📄 Load Sample Resume</button>
              <label className="btn btn--secondary" style={{ cursor: 'pointer' }}>
                📎 Upload PDF
                <input type="file" accept=".pdf" style={{ display: 'none' }} onChange={handlePdfUpload} />
              </label>
              {pdfStatus && (
                <span style={{ fontSize: '0.82rem', color: pdfStatus.color, alignSelf: 'center' }}>{pdfStatus.text}</span>
              )}
            </div>
          </div>
          <div className="form-group">
            <label>GitHub Username <span style={{ fontWeight: 400, textTransform: 'none', color: 'var(--text-muted)' }}>(optional — enriches analysis)</span></label>
            <input className="input" type="text" value={githubUsername}
              onChange={e => setGithubUsername(e.target.value)}
              placeholder="e.g. octocat" autoComplete="off" spellCheck="false" />
          </div>
          <div className="form-group">
            <label>Dream Role</label>
            <select className="select" value={dreamRole} onChange={e => { setDreamRole(e.target.value); if (e.target.value !== '__custom__') setCustomRole(''); }}>
              <option value="">— Select your dream role —</option>
              {roles.map(r => <option key={r} value={r}>{r}</option>)}
              <option value="__custom__">✨ Custom (type your own)</option>
            </select>
            {dreamRole === '__custom__' && (
              <input className="input" type="text" value={customRole}
                onChange={e => setCustomRole(e.target.value)}
                placeholder="Type your dream role, e.g. Blockchain Developer, Game Designer..."
                style={{ marginTop: '0.5rem' }} />
            )}
          </div>
          <button className="btn btn--primary btn--full" onClick={handleSubmit}>🚀 Generate Career Roadmap</button>
        </div>
      </ParticleCard>
    </div>
  );
}

// ═══════════════════════════════════════════
// THINKING STAGE
// ═══════════════════════════════════════════
function ThinkingStage({ mode }) {
  const [visibleIdx, setVisibleIdx] = useState(0);
  const steps = mode === 'adapt'
    ? ['Analyzing progress vs. original plan...', 'Identifying missed critical content...', 'Compressing remaining curriculum...', 'Adjusting flagship project scope...', 'Generating motivation and new milestones...']
    : ['Parsing resume and extracting skills...', 'Analyzing dream role requirements...', 'Computing skill gap analysis...', 'Designing 30-day adaptive roadmap...', 'Building flagship project plan...', 'Finalizing personalized recommendations...'];

  useEffect(() => {
    setVisibleIdx(0);
    const iv = setInterval(() => {
      setVisibleIdx(prev => {
        if (prev < steps.length) return prev + 1;
        clearInterval(iv);
        return prev;
      });
    }, 1200);
    return () => clearInterval(iv);
  }, [mode, steps.length]);

  return (
    <div className="card">
      <div className="thinking">
        <div className="thinking__dots">
          <div className="thinking__dot" />
          <div className="thinking__dot" />
          <div className="thinking__dot" />
        </div>
        <h3 style={{ marginBottom: '0.5rem', fontSize: '1.1rem', fontWeight: 700 }}>
          {mode === 'adapt' ? '🔄 Career Brain is re-planning...' : '🧠 Career Brain is analyzing...'}
        </h3>
        <p style={{ color: 'var(--text-muted)', fontSize: '0.82rem', marginBottom: '1.5rem' }}>
          {mode === 'adapt' ? 'Adapting your roadmap based on progress update' : 'Processing your profile and generating a personalized career plan'}
        </p>
        <ul className="thinking__steps">
          {steps.map((step, i) => (
            <li key={i} className={`thinking__step${i < visibleIdx ? ' thinking__step--visible' : ''}${i === visibleIdx - 1 && visibleIdx <= steps.length ? ' thinking__step--active' : ''}${i < visibleIdx - 1 ? ' thinking__step--done' : ''}`}>
              <span style={{ flexShrink: 0, fontSize: '0.82rem' }}>
                {i < visibleIdx - 1 ? '✓' : i === visibleIdx - 1 ? '◉' : '○'}
              </span>
              {step}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}

// ═══════════════════════════════════════════
// RESULT TABS
// ═══════════════════════════════════════════
function SkillsTab({ data }) {
  const d = data;
  return (
    <MagicBento
      textAutoHide={true}
      enableStars
      enableSpotlight
      enableBorderGlow={true}
      enableTilt
      enableMagnetism
      clickEffect
      spotlightRadius={400}
      particleCount={12}
      glowColor="132, 0, 255"
      disableAnimations={false}
      autoLayout={true}
    >
      {/* Card 1: Extracted Skills */}
      <>
        <h3>🧠 Extracted Skills</h3>
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.3rem' }}>
          {(d.skill_map?.skills || []).map((s, i) => {
            const st = s.level === 'advanced' ? '★★★' : s.level === 'intermediate' ? '★★' : '★';
            return <span key={i} className={`skill-tag skill-tag--${s.level}`}>{s.name} <span style={{ opacity: 0.6, fontSize: '0.7rem' }}>{st}</span></span>;
          })}
        </div>
      </>

      {/* Card 2: Strengths */}
      <>
        <h3 style={{ color: 'var(--accent-emerald)' }}>✦ Strengths</h3>
        <ul className="list list--strength">
          {(d.skill_map?.strengths || []).map((s, i) => <li key={i}>{s}</li>)}
        </ul>
      </>

      {/* Card 3: Weaknesses */}
      <>
        <h3 style={{ color: 'var(--accent-amber)' }}>△ Weaknesses</h3>
        <ul className="list list--weakness">
          {(d.skill_map?.weaknesses || []).map((w, i) => <li key={i}>{w}</li>)}
        </ul>
      </>

      {/* Card 4: Role Requirements */}
      <>
        <h3>🎯 Role Requirements</h3>
        {Object.entries(d.role_requirements || {}).map(([cat, skills]) => (
          <div key={cat} style={{ marginBottom: '0.75rem' }}>
            <div className="section-label">{cat.replace(/_/g, ' ')}</div>
            {(skills || []).map((s, i) => <span key={i} className="skill-tag skill-tag--role">{s}</span>)}
          </div>
        ))}
      </>
    </MagicBento>
  );
}

function GapsTab({ data }) {
  const levels = [
    ['critical', '🔴 Critical', '--critical'],
    ['important', '🟡 Important', '--important'],
    ['nice_to_have', '🔵 Nice to Have', '--nice']
  ];
  return (
    <MagicBento
      textAutoHide={false}
      enableStars
      enableSpotlight
      enableBorderGlow={true}
      enableTilt
      enableMagnetism
      clickEffect
      spotlightRadius={400}
      particleCount={8}
      glowColor="244, 63, 94"
      disableAnimations={false}
      autoLayout={true}
    >
      {levels.map(([key, label, cls]) => {
        const items = (data.gap_analysis || {})[key] || [];
        return (
          <div key={key}>
            <h3 className={`gap-section__title gap-section__title${cls}`} style={{ borderBottom: 'none', marginBottom: '0.5rem' }}>{label} ({items.length})</h3>
            {items.map((g, i) => (
              <div key={i} className={`gap-item gap-item${cls}`}>
                <div className="gap-item__skill">{g.skill}</div>
                <div className="gap-item__reason">{g.reason}</div>
              </div>
            ))}
          </div>
        );
      })}
    </MagicBento>
  );
}

function RoadmapTab({ data, adaptData }) {
  const rm = (adaptData ? adaptData.adapted_roadmap : data.roadmap) || {};
  return (
    <>
      {adaptData && (
        <div className="motivation-banner">🔄 <strong>Adapted Roadmap</strong> — Re-generated after missing 7 days. Content compressed and priorities re-ordered.</div>
      )}
      <div className="card">
        <h3 className="card__title">{adaptData ? '📅 Adapted Roadmap' : '📅 30-Day Learning Roadmap'}</h3>
        {(rm.weekly_milestones || []).map((ms, mi) => {
          let wd = (rm.days || []).filter(d => Math.ceil(d.day / 7) === ms.week);
          if (!wd.length) wd = ms.week === (rm.weekly_milestones || [])[0]?.week ? (rm.days || []) : [];
          return (
            <div key={mi} className="week-block">
              <div className="week-header">
                <span className="week-header__number">Week {ms.week}</span>
                <span className="week-header__milestone">{ms.milestone}</span>
              </div>
              {wd.map((day, di) => (
                <div key={di} className="day-row">
                  <div className="day-row__number">D{day.day}</div>
                  <div>
                    <div className="day-row__objective">{day.objective}</div>
                    <div className="day-row__details">
                      <span>📖 {day.resource}</span>
                      <span>✏️ {day.task}</span>
                      <span>⏱ {day.hours}h</span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          );
        })}
      </div>
    </>
  );
}

function ProjectTab({ data, adaptData }) {
  const p = data.flagship_project || {};
  const pf = adaptData ? (adaptData.adapted_project?.weekly_features || []) : (p.weekly_features || []);
  return (
    <>
      {adaptData?.adapted_project && (
        <div className="motivation-banner">🔧 <strong>Project Scope Adjusted:</strong> {adaptData.adapted_project.changes || ''}</div>
      )}
      <div className="card project-card">
        <div className="project-card__title">{p.title || ''}</div>
        <p className="project-card__problem">{p.problem_statement || ''}</p>
        <div className="section-label">Tech Stack</div>
        <div className="tech-stack">
          {(p.tech_stack || []).map((t, i) => <span key={i} className="tech-tag">{t}</span>)}
        </div>
        <div className="section-label">Weekly Feature Plan</div>
        {pf.map((f, i) => (
          <div key={i} className="weekly-feature">
            <div className="weekly-feature__week">Week {f.week}</div>
            <div className="weekly-feature__name">{f.feature}</div>
            <div className="weekly-feature__desc">{f.description}</div>
          </div>
        ))}
        {p.portfolio_quality && (
          <div className="pq-box">
            <div className="section-label" style={{ color: 'var(--accent-emerald)' }}>Portfolio Quality</div>
            <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)' }}>{p.portfolio_quality}</p>
          </div>
        )}
      </div>
    </>
  );
}

function ResultsStage({ data, adaptData, onAdapt, onReset }) {
  const [activeTab, setActiveTab] = useState('skills');
  const tabs = [
    { key: 'skills', label: '🧠 Skills' },
    { key: 'gaps', label: '⚡ Gaps' },
    { key: 'roadmap', label: '📅 Roadmap' },
    { key: 'project', label: '🚀 Project' }
  ];

  return (
    <div className="fade-in">
      <div className="reasoning-box">
        💡 <strong>Agent Reasoning:</strong> {adaptData ? adaptData.adaptation_reasoning : data.reasoning}
      </div>

      <div className="tabs">
        {tabs.map(t => (
          <button key={t.key} className={`tab${activeTab === t.key ? ' tab--active' : ''}`}
            onClick={() => setActiveTab(t.key)}>
            {t.label}
          </button>
        ))}
      </div>

      {activeTab === 'skills' && <SkillsTab data={data} />}
      {activeTab === 'gaps' && <GapsTab data={data} />}
      {activeTab === 'roadmap' && <RoadmapTab data={data} adaptData={adaptData} />}
      {activeTab === 'project' && <ProjectTab data={data} adaptData={adaptData} />}

      {!adaptData && (
        <div className="adapt-panel">
          <h3 className="adapt-panel__title">⚡ Adaptation Simulator</h3>
          <p className="adapt-panel__desc">
            Simulate a real-world scenario: you completed the first 7 days, then missed the
            next 7 days due to exams. Watch the AI re-plan your entire remaining roadmap in real-time.
          </p>
          <button className="btn btn--danger" onClick={onAdapt}>🔄 Simulate: Missed 7 Days → Re-Plan</button>
        </div>
      )}

      {adaptData && (
        <div className="motivation-banner">💪 {adaptData.motivation || 'Keep going!'}</div>
      )}

      <div style={{ textAlign: 'center', marginTop: '1.5rem' }}>
        <button className="btn btn--secondary" onClick={onReset}>← Start Over</button>
      </div>
    </div>
  );
}

// ═══════════════════════════════════════════
// MAIN APP
// ═══════════════════════════════════════════
export default function App() {
  const [stage, setStage] = useState('input'); // input | thinking | results
  const [thinkingMode, setThinkingMode] = useState('generate');
  const [error, setError] = useState('');
  const [roles, setRoles] = useState([]);
  const [roadmapData, setRoadmapData] = useState(null);
  const [adaptData, setAdaptData] = useState(null);

  // Load roles on startup
  useEffect(() => {
    (async () => {
      try {
        const r = await fetch(API + '/roles');
        const d = await r.json();
        setRoles(d.roles || []);
      } catch {
        setRoles(['ML Engineer', 'Frontend Developer', 'Data Analyst', 'Backend Developer', 'DevOps Engineer', 'AI/NLP Engineer', 'Full Stack Developer', 'Cybersecurity Analyst']);
      }
    })();
  }, []);

  const generateRoadmap = useCallback(async (resumeText, dreamRole, githubUsername) => {
    if (!resumeText.trim()) { setError('Please paste your resume or upload a PDF.'); return; }
    if (!dreamRole.trim()) { setError('Please select a dream role or type a custom one.'); return; }
    setError('');
    setThinkingMode('generate');
    setStage('thinking');
    try {
      const body = { resume_text: resumeText, dream_role: dreamRole };
      if (githubUsername) body.github_username = githubUsername;
      const res = await fetch(API + '/generate-roadmap', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
      });
      if (!res.ok) throw new Error('Server error: ' + res.status);
      const data = await res.json();
      setRoadmapData(data);
      setTimeout(() => setStage('results'), 2500);
    } catch (err) {
      setError(err.message + '. Run: python -m uvicorn main:app --reload');
      setStage('input');
    }
  }, []);

  const adaptRoadmap = useCallback(async () => {
    setThinkingMode('adapt');
    setStage('thinking');
    try {
      const res = await fetch(API + '/adapt-roadmap', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          days_completed: 7,
          days_missed: 7,
          reason: 'Fell behind due to exams and personal commitments',
          confidence: 4
        })
      });
      if (!res.ok) throw new Error('Server error: ' + res.status);
      const data = await res.json();
      setAdaptData(data);
      setTimeout(() => setStage('results'), 2500);
    } catch (err) {
      setError(err.message);
      setStage('results');
    }
  }, []);

  const resetAll = useCallback(() => {
    setRoadmapData(null);
    setAdaptData(null);
    setError('');
    setStage('input');
  }, []);

  return (
    <>
      {/* Light Rays Background */}
      <div className="background-layer">
        <LightRays
          raysOrigin="top-center"
          raysColor="#ffffff"
          raysSpeed={1}
          lightSpread={0.5}
          rayLength={3}
          followMouse={true}
          mouseInfluence={0.1}
          noiseAmount={0}
          distortion={0}
          pulsating={false}
          fadeDistance={1}
          saturation={1}
        />
      </div>

      <div className="app">
        <Header />
        <ErrorBox message={error} onDismiss={() => setError('')} />

        {stage === 'input' && (
          <InputStage onGenerate={generateRoadmap} roles={roles} />
        )}

        {stage === 'thinking' && (
          <ThinkingStage mode={thinkingMode} />
        )}

        {stage === 'results' && roadmapData && (
          <ResultsStage
            data={roadmapData}
            adaptData={adaptData}
            onAdapt={adaptRoadmap}
            onReset={resetAll}
          />
        )}
      </div>
    </>
  );
}
