import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { LogIn, LogOut, Shield, Sparkles, User as UserIcon } from 'lucide-react';
import './Navbar.css';

export const Navbar: React.FC = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = async () => {
    await logout();
    navigate('/');
  };

  return (
    <header className="tech-navbar">
      <div className="tech-navbar__container">
        <Link to="/" className="tech-navbar__brand">
          <div className="tech-navbar__logo">
            <Sparkles size={16} />
          </div>
          <span className="tech-navbar__title">Tech Inject</span>
          <span className="tech-navbar__badge">Library</span>
        </Link>

        <nav className="tech-navbar__links">
          <Link to="/" className="tech-navbar__link">Get Started</Link>
          <Link to="/components" className="tech-navbar__link">Components</Link>
          {user?.role === 'admin' && (
            <Link to="/admin" className="tech-navbar__link tech-navbar__link--admin">
              <Shield size={14} />
              <span>Admin Dashboard</span>
            </Link>
          )}
        </nav>

        <div className="tech-navbar__auth">
          {user ? (
            <div className="tech-navbar__user-menu">
              <span className="tech-navbar__user-email">
                <UserIcon size={14} />
                {user.email}
              </span>
              {user.is_premium ? (
                <span className="tech-navbar__status-pill tech-navbar__status-pill--premium">
                  ★ Premium Access
                </span>
              ) : (
                <span className="tech-navbar__status-pill tech-navbar__status-pill--free">
                  Free Account
                </span>
              )}
              <button onClick={handleLogout} className="tech-navbar__btn-logout" title="Sign Out">
                <LogOut size={16} />
              </button>
            </div>
          ) : (
            <Link to="/login" className="tech-navbar__btn-login">
              <LogIn size={16} />
              <span>Sign In</span>
            </Link>
          )}
        </div>
      </div>
    </header>
  );
};
