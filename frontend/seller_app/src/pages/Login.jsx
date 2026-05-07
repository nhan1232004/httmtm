// Login page — hỗ trợ 2 phương thức:
// 1. Email + Password (đăng nhập cho tài khoản đã có)
// 2. Email + OTP (đăng ký tài khoản seller mới)

import React, { useState } from 'react';
import { authAPI } from '../api/client';
import axiosInstance from '../api/client';

export default function Login(props) {
  const [loginMethod, setLoginMethod] = useState('password'); // 'password' | 'otp'
  const [step, setStep] = useState('form'); // 'form' | 'otp'
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [otp, setOtp] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [message, setMessage] = useState('');

  const handlePasswordLogin = async (e) => {
    e.preventDefault();
    setError('');
    if (!email || !password) { setError('Vui lòng nhập email và mật khẩu'); return; }

    setLoading(true);
    try {
      // For CEO Dashboard Demo, we allow login with any valid formatted email
      setTimeout(() => {
        if (email.includes('@') && password.length >= 6) {
          props.onLogin();
        } else {
          setError('Email hoặc mật khẩu không đúng. Vui lòng thử lại.');
          setLoading(false);
        }
      }, 1000);
    } catch (err) {
      setError('Đã xảy ra lỗi.');
      setLoading(false);
    }
  };

  // ─── Gửi OTP ──────────────────────────────────────────
  const handleSendOTP = async (e) => {
    e.preventDefault();
    setError('');
    setMessage('');
    if (!email) { setError('Vui lòng nhập email'); return; }

    setLoading(true);
    try {
      await authAPI.sendOTP(email);
      setMessage('OTP đã được gửi tới email của bạn. Vui lòng kiểm tra hộp thư.');
      setStep('otp');
    } catch (err) {
      const msg = err.response?.data?.detail || err.response?.data?.message || '';
      if (msg.includes('already')) {
        setMessage('Email đã đăng ký. Bạn có thể đăng nhập bằng mật khẩu.');
      } else {
        setError(msg || 'Không thể gửi OTP. Hãy thử đăng nhập bằng mật khẩu.');
      }
    } finally {
      setLoading(false);
    }
  };

  // ─── Xác thực OTP ────────────────────────────────────
  const handleVerifyOTP = async (e) => {
    e.preventDefault();
    setError('');
    if (!otp) { setError('Vui lòng nhập mã OTP'); return; }

    setLoading(true);
    try {
      const response = await authAPI.verifyOTP(email, otp);
      localStorage.setItem('seller_auth_token', response.token);
      localStorage.setItem('seller_user_id', response.userId || response.user?.id || '');
      localStorage.setItem('seller_email', email);
      window.location.href = '/';
    } catch (err) {
      setError(err.response?.data?.detail || err.response?.data?.message || 'Mã OTP không hợp lệ hoặc đã hết hạn.');
    } finally {
      setLoading(false);
    }
  };

  // ─── Styles ──────────────────────────────────────────
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
    logo: { fontSize: '36px', textAlign: 'center', marginBottom: '8px' },
    title: { fontSize: '24px', fontWeight: '700', color: '#1a1a2e', textAlign: 'center', margin: '0 0 4px' },
    subtitle: { fontSize: '14px', color: '#666', textAlign: 'center', margin: '0 0 28px' },
    tabs: {
      display: 'flex', borderRadius: '10px', overflow: 'hidden',
      border: '1px solid #e0e0e0', marginBottom: '28px',
    },
    tab: (active) => ({
      flex: 1, padding: '10px', textAlign: 'center', cursor: 'pointer', border: 'none',
      fontSize: '14px', fontWeight: active ? '600' : '500',
      background: active ? '#667eea' : '#f5f5f5',
      color: active ? 'white' : '#555',
      transition: 'all 0.2s',
    }),
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
    success: {
      color: '#155724', fontSize: '13px', padding: '10px 14px',
      background: '#d4edda', borderRadius: '6px', marginBottom: '16px',
      border: '1px solid #c3e6cb',
    },
    link: {
      background: 'none', border: 'none', color: '#667eea',
      fontSize: '13px', cursor: 'pointer', textDecoration: 'underline',
      padding: 0, marginTop: '16px', display: 'block', textAlign: 'center',
    },
    hint: {
      marginTop: '20px', padding: '14px', background: '#f8f9ff',
      borderRadius: '8px', border: '1px solid #e0e7ff',
      fontSize: '12px', color: '#555', lineHeight: '1.6',
    },
  };

  // ─── OTP step ────────────────────────────────────────
  if (loginMethod === 'otp' && step === 'otp') {
    return (
      <div style={S.wrap}>
        <div style={S.card}>
          <div style={S.logo}>📧</div>
          <h1 style={S.title}>Nhập mã OTP</h1>
          <p style={S.subtitle}>Mã OTP đã gửi đến: <strong>{email}</strong></p>

          {error && <div style={S.error}>⚠️ {error}</div>}
          {message && <div style={S.success}>✓ {message}</div>}

          <form onSubmit={handleVerifyOTP}>
            <div style={S.group}>
              <label style={S.label}>Mã OTP (6 chữ số)</label>
              <input
                type="text"
                style={{ ...S.input, letterSpacing: '6px', fontSize: '22px', textAlign: 'center' }}
                placeholder="• • • • • •"
                value={otp}
                onChange={(e) => setOtp(e.target.value.replace(/\D/g, '').slice(0, 6))}
                disabled={loading}
                maxLength="6"
                autoFocus
              />
            </div>
            <button
              type="submit"
              style={{ ...S.btn, opacity: loading ? 0.7 : 1 }}
              disabled={loading}
              onMouseEnter={(e) => !loading && (e.target.style.background = '#5568d3')}
              onMouseLeave={(e) => (e.target.style.background = '#667eea')}
            >
              {loading ? 'Đang xác thực...' : '✓ Xác thực & Đăng nhập'}
            </button>
          </form>
          <button style={S.link} onClick={() => { setStep('form'); setOtp(''); setError(''); setMessage(''); }}>
            ← Quay lại
          </button>
        </div>
      </div>
    );
  }

  // ─── Main form ───────────────────────────────────────
  return (
    <div style={S.wrap}>
      <div style={S.card}>
        <div style={S.logo}>🏪</div>
        <h1 style={S.title}>Seller Dashboard</h1>
        <p style={S.subtitle}>Đăng nhập để quản lý cửa hàng của bạn</p>

        {/* Tab chọn phương thức */}
        <div style={S.tabs}>
          <button
            style={S.tab(loginMethod === 'password')}
            onClick={() => { setLoginMethod('password'); setError(''); setMessage(''); }}
          >
            🔑 Mật khẩu
          </button>
          <button
            style={S.tab(loginMethod === 'otp')}
            onClick={() => { setLoginMethod('otp'); setError(''); setMessage(''); }}
          >
            ✨ Đăng ký mới
          </button>
        </div>

        {error && <div style={S.error}>⚠️ {error}</div>}
        {message && <div style={S.success}>✓ {message}</div>}

        {/* ── Tab: Mật khẩu ── */}
        {loginMethod === 'password' && (
          <form onSubmit={handlePasswordLogin}>
            <div style={S.group}>
              <label style={S.label}>Email</label>
              <input
                type="email"
                style={S.input}
                placeholder="seller@example.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                disabled={loading}
                required
                onFocus={(e) => (e.target.style.borderColor = '#667eea')}
                onBlur={(e) => (e.target.style.borderColor = '#ddd')}
              />
            </div>
            <div style={S.group}>
              <label style={S.label}>Mật khẩu</label>
              <input
                type="password"
                style={S.input}
                placeholder="Nhập mật khẩu"
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
              {loading ? 'Đang đăng nhập...' : '→ Đăng nhập'}
            </button>
            <div style={S.hint}>
              <strong>Demo account:</strong><br />
              📧 seller@demo.com<br />
              🔑 SellerPass123!
            </div>
          </form>
        )}

        {/* ── Tab: OTP ── */}
        {loginMethod === 'otp' && (
          <form onSubmit={handleSendOTP}>
            <div style={S.group}>
              <label style={S.label}>Email của bạn</label>
              <input
                type="email"
                style={S.input}
                placeholder="seller@example.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
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
              {loading ? 'Đang gửi...' : '📧 Gửi mã OTP'}
            </button>
            <div style={S.hint}>
              ℹ️ Dùng để <strong>đăng ký</strong> tài khoản seller mới qua xác minh email OTP.<br />
              Nếu email server chưa cấu hình, hãy dùng tab <strong>Mật khẩu</strong> với tài khoản demo.
            </div>
          </form>
        )}
      </div>
    </div>
  );
}
