import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import { Navbar } from './components/common/Navbar';
import { Home } from './pages/Home';
import { Catalogue } from './pages/Catalogue';
import { ComponentDetail } from './pages/ComponentDetail';
import { Login } from './pages/Login';
import { AdminDashboard } from './pages/AdminDashboard';
import './styles/tokens.css';

export const App: React.FC = () => {
  return (
    <AuthProvider>
      <Router>
        <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
          <Navbar />
          <main style={{ flex: 1 }}>
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/components" element={<Catalogue />} />
              <Route path="/components/:slug" element={<ComponentDetail />} />
              <Route path="/login" element={<Login />} />
              <Route path="/admin" element={<AdminDashboard />} />
            </Routes>
          </main>
        </div>
      </Router>
    </AuthProvider>
  );
};

export default App;
