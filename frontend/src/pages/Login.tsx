import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { LogIn, UserPlus, Sparkles, Key, AlertCircle } from 'lucide-react';
import './Login.css';

export const Login: React.FC = () => {
  const { login, signup } = useAuth();
  const navigate = useNavigate();

  const [mode, setMode] = useState<'signin' | 'signup'>('signin');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setSubmitting(true);
    try {
      let u;
      if (mode === 'signup') {
        u = await signup(email, password);
      } else {
        u = await login(email, password);
      }

      if (u.role === 'admin') {
        navigate('/admin');
      } else {
        navigate('/components');
      }
    } catch (err: any) {
      setError(err.message || 'Authentication failed');
    } finally {
      setSubmitting(false);
    }
  };

  const fillDemo = (demoEmail: string, demoPass: string) => {
    setMode('signin');
    setEmail(demoEmail);
    setPassword(demoPass);
    setError(null);
  };

  return (
    <div className="tech-login">
      <div className="tech-login__card">
        <div className="tech-login__header">
          <div className="tech-login__logo">
            <Sparkles size={20} />
          </div>
          <h2>{mode === 'signup' ? 'Create an Account' : 'Sign In to Tech Inject'}</h2>
          <p>Access free & premium React component libraries</p>
        </div>

        {/* Mode Switcher Tabs */}
        <div className="tech-login__mode-tabs">
          <button
            type="button"
            className={`tech-login__mode-tab ${mode === 'signin' ? 'tech-login__mode-tab--active' : ''}`}
            onClick={() => { setMode('signin'); setError(null); }}
          >
            Sign In
          </button>
          <button
            type="button"
            className={`tech-login__mode-tab ${mode === 'signup' ? 'tech-login__mode-tab--active' : ''}`}
            onClick={() => { setMode('signup'); setError(null); }}
          >
            Create Account
          </button>
        </div>

        {error && (
          <div className="tech-login__error">
            <AlertCircle size={16} />
            <span>{error}</span>
          </div>
        )}

        <form onSubmit={handleSubmit} className="tech-login__form">
          <div className="tech-login__field">
            <label>Email Address</label>
            <input
              type="email"
              required
              placeholder="user@example.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
          </div>

          <div className="tech-login__field">
            <label>Password</label>
            <input
              type="password"
              required
              minLength={6}
              placeholder="••••••••"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>

          <button type="submit" disabled={submitting} className="tech-login__btn-submit">
            {mode === 'signup' ? <UserPlus size={16} /> : <LogIn size={16} />}
            <span>
              {submitting
                ? mode === 'signup' ? 'Creating Account...' : 'Signing In...'
                : mode === 'signup' ? 'Sign Up' : 'Sign In'}
            </span>
          </button>
        </form>

        {/* Quick Demo Test Credential Buttons */}
        <div className="tech-login__demo-box">
          <div className="tech-login__demo-title">
            <Key size={14} />
            <span>Quick Demo Test Accounts</span>
          </div>
          <div className="tech-login__demo-btns">
            <button
              type="button"
              className="tech-login__demo-btn"
              onClick={() => fillDemo('admin@techinject.com', 'admin123')}
            >
              Admin Demo (admin@techinject.com)
            </button>
            <button
              type="button"
              className="tech-login__demo-btn"
              onClick={() => fillDemo('free@example.com', 'customer123')}
            >
              Free Customer Demo (free@example.com)
            </button>
            <button
              type="button"
              className="tech-login__demo-btn"
              onClick={() => fillDemo('premium@example.com', 'customer123')}
            >
              Premium Customer 1 (premium@example.com)
            </button>
            <button
              type="button"
              className="tech-login__demo-btn"
              onClick={() => fillDemo('premium2@example.com', 'customer123')}
            >
              Premium Customer 2 (premium2@example.com)
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
