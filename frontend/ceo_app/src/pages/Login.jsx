// CEO Dashboard Login
// Mock authentication for demo purposes

import React, { useState } from 'react';
import axiosInstance from '../api/client';

export default function Login(props) {
  const [email, setEmail] = useState('admin@demo.com');
  const [password, setPassword] = useState('AdminPass123!');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleLogin = async (e) => {
    e.preventDefault();
    setError('');
    if (!email || !password) {
      setError('Please enter email and password');
      return;
    }

    setLoading(true);
    try {
      setTimeout(() => {
        if (email.includes('@') && password.length >= 6) {
          localStorage.setItem('ceo_auth_token', 'demo-token-' + Date.now());
          localStorage.setItem('ceo_user_id', 'admin-1');
          localStorage.setItem('ceo_email', email);
          props.onLogin();
        } else {
          setError('Invalid email or password. Please try again.');
          setLoading(false);
        }
      }, 800);
    } catch (err) {
      setError('An error occurred.');
      setLoading(false);
    }
  };

  const S = {
    wrap: {
      display: 'flex', justifyContent: 'center', alignItems: 'center',
      minHeight: '100vh',
      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
      fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
    },
    card: {
      background: 'white', borderRadius: '16px',
      boxShadow: '0 20px 60px rgba(0,0,0,0.25)',
      padding: '40px', width: '100%', maxWidth: '420px',
    },
    logo: { fontSize: '48px', textAlign: 'center', marginBottom: '16px' },
    title: { fontSize: '28px', fontWeight: '700', color: '#1a1a2e', textAlign: 'center', margin: '0 0 8px' },
    subtitle: { fontSize: '14px', color: '#666', textAlign: 'center', margin: '0 0 28px' },
    group: { marginBottom: '18px' },
    label: { display: 'block', fontSize: '13px', fontWeight: '600', color: '#444', marginBottom: '6px' },
    input: {
      width: '100%', padding: '12px 14px', fontSize: '15px',
      border: '1.5px solid #ddd', borderRadius: '8px',
      boxSizing: 'border-box', outline: 'none', transition: 'border-color 0.2s',
      fontFamily: 'inherit',
    },
    btn: {
      width: '100%', padding: '13px', background: '#667eea', color: 'white',
      fontSize: '15px', fontWeight: '700', border: 'none', borderRadius: '8px',
      cursor: 'pointer', marginTop: '6px', transition: 'background 0.2s',
    },
    error: {
      color: '#dc3545', fontSize: '13px', padding: '10px 14px',
      background: '#f8d7da', borderRadius: '6px', marginBottom: '16px',
      border: '1px solid #f5c6cb',
    },
    hint: {
      marginTop: '20px', padding: '14px', background: '#f8f9ff',
      borderRadius: '8px', border: '1px solid #e0e7ff',
      fontSize: '12px', color: '#555', lineHeight: '1.6',
    },
  };

  return (
    <div style={S.wrap}>
      <div style={S.card}>
        <div style={S.logo}>📊</div>
        <h1 style={S.title}>CEO Dashboard</h1>
        <p style={S.subtitle}>Executive Business Intelligence Platform</p>

        {error && <div style={S.error}>⚠️ {error}</div>}

        <form onSubmit={handleLogin}>
          <div style={S.group}>
            <label style={S.label}>Email</label>
            <input
              type="email"
              style={S.input}
              placeholder="admin@demo.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              disabled={loading}
              required
              onFocus={(e) => (e.target.style.borderColor = '#667eea')}
              onBlur={(e) => (e.target.style.borderColor = '#ddd')}
            />
          </div>
          <div style={S.group}>
            <label style={S.label}>Password</label>
            <input
              type="password"
              style={S.input}
              placeholder="Enter password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              disabled={loading}
              required
              onFocus={(e) => (e.target.style.borderColor = '#667eea')}
              onBlur={(e) => (e.target.style.borderColor = '#ddd')}
            />
          </div>
          <button
            type="submit"
            style={{ ...S.btn, opacity: loading ? 0.7 : 1 }}
            disabled={loading}
            onMouseEnter={(e) => !loading && (e.target.style.background = '#5568d3')}
            onMouseLeave={(e) => (e.target.style.background = '#667eea')}
          >
            {loading ? 'Signing in...' : '→ Sign In'}
          </button>
          <div style={S.hint}>
            <strong>Demo Credentials:</strong><br />
            📧 admin@demo.com<br />
            🔑 AdminPass123!<br />
            <br />
            <em>Or login with any valid email</em>
          </div>
        </form>
      </div>
    </div>
  );
}
