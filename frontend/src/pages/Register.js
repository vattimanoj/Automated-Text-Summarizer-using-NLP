import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import './Register.css';

const Register = () => {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [loading, setLoading] = useState(false);
  const { register } = useAuth();
  const navigate = useNavigate();

  const [fieldErrors, setFieldErrors] = useState({ name: '', email: '', password: '', confirmPassword: '' });
  const [touched, setTouched] = useState({ name: false, email: false, password: false, confirmPassword: false });

  // Password strength
  const getPasswordStrength = (pwd) => {
    if (!pwd) return { level: 0, label: '', color: '' };
    let score = 0;
    if (pwd.length >= 8) score++;
    if (/[A-Z]/.test(pwd)) score++;
    if (/\d/.test(pwd)) score++;
    if (/[!@#$%^&*(),.?":{}|<>]/.test(pwd)) score++;
    if (score === 1) return { level: 1, label: 'Weak', color: '#e74c3c' };
    if (score === 2) return { level: 2, label: 'Fair', color: '#f39c12' };
    if (score === 3) return { level: 3, label: 'Good', color: '#3498db' };
    if (score === 4) return { level: 4, label: 'Strong', color: '#27ae60' };
    return { level: 0, label: '', color: '' };
  };

  const validateName = (val) => {
    if (!val.trim()) return 'Full name is required';
    if (val.trim().length < 2) return 'Name must be at least 2 characters';
    if (!/^[a-zA-Z\s]+$/.test(val.trim())) return 'Name can only contain letters and spaces';
    return '';
  };

  const validateEmail = (val) => {
    if (!val) return 'Email is required';
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(val)) return 'Enter a valid email address';
    return '';
  };

  const validatePassword = (val) => {
    if (!val) return 'Password is required';
    if (val.length < 8) return 'Password must be at least 8 characters';
    if (!/[A-Z]/.test(val)) return 'Must contain at least one uppercase letter';
    if (!/\d/.test(val)) return 'Must contain at least one number';
    if (!/[!@#$%^&*(),.?":{}|<>]/.test(val)) return 'Must contain at least one special character';
    return '';
  };

  const validateConfirmPassword = (val, pwd = password) => {
    if (!val) return 'Please confirm your password';
    if (val !== pwd) return 'Passwords do not match';
    return '';
  };

  const handleBlur = (field) => {
    setTouched((prev) => ({ ...prev, [field]: true }));
    const validators = {
      name: () => validateName(name),
      email: () => validateEmail(email),
      password: () => validatePassword(password),
      confirmPassword: () => validateConfirmPassword(confirmPassword),
    };
    setFieldErrors((prev) => ({ ...prev, [field]: validators[field]() }));
  };

  const handleChange = (field, value, setter) => {
    setter(value);
    if (touched[field]) {
      const errors = { ...fieldErrors };
      if (field === 'name') errors.name = validateName(value);
      if (field === 'email') errors.email = validateEmail(value);
      if (field === 'password') {
        errors.password = validatePassword(value);
        if (touched.confirmPassword) errors.confirmPassword = validateConfirmPassword(confirmPassword, value);
      }
      if (field === 'confirmPassword') errors.confirmPassword = validateConfirmPassword(value);
      setFieldErrors(errors);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    const nameErr = validateName(name);
    const emailErr = validateEmail(email);
    const passwordErr = validatePassword(password);
    const confirmErr = validateConfirmPassword(confirmPassword);

    setFieldErrors({ name: nameErr, email: emailErr, password: passwordErr, confirmPassword: confirmErr });
    setTouched({ name: true, email: true, password: true, confirmPassword: true });

    if (nameErr || emailErr || passwordErr || confirmErr) return;

    setLoading(true);
    try {
      await register(name, email, password);
      setSuccess('Registration successful! Please sign in with your new account.');
      setTimeout(() => {
        navigate('/login');
      }, 2000);
    } catch (err) {
      const detail = err.response?.data?.detail;
      let message = 'Registration failed. Please try again.';
      if (typeof detail === 'string') {
        message = detail;
      } else if (Array.isArray(detail) && detail.length > 0) {
        message = detail.map((e) => e.msg || JSON.stringify(e)).join('. ');
      } else if (err.message) {
        message = err.response?.status === 500
          ? 'Server error. Please try again later.'
          : err.message;
      }
      setError(message);
    } finally {
      setLoading(false);
    }
  };

  const strength = getPasswordStrength(password);

  const inputClass = (field) =>
    `form-input ${touched[field] && fieldErrors[field] ? 'input-error' : touched[field] && !fieldErrors[field] ? 'input-success' : ''}`;

  return (
    <div className="register-container">
      <div className="register-card">
        <div className="register-header">
          <h1>Create Account</h1>
          <p>Join us to get started</p>
        </div>

        {error && <div className="alert alert-error">{error}</div>}
        {success && <div className="alert alert-success">{success}</div>}

        <form onSubmit={handleSubmit} className="register-form" noValidate>

          {/* Full Name */}
          <div className="form-group">
            <label className="form-label">Full Name</label>
            <input
              type="text"
              className={inputClass('name')}
              value={name}
              onChange={(e) => handleChange('name', e.target.value, setName)}
              onBlur={() => handleBlur('name')}
              placeholder="Enter your full name"
            />
            {touched.name && fieldErrors.name && (
              <span className="field-error-text">⚠ {fieldErrors.name}</span>
            )}
            {touched.name && !fieldErrors.name && name && (
              <span className="field-success-text">✓ Looks good!</span>
            )}
          </div>

          {/* Email */}
          <div className="form-group">
            <label className="form-label">Email</label>
            <input
              type="email"
              className={inputClass('email')}
              value={email}
              onChange={(e) => handleChange('email', e.target.value, setEmail)}
              onBlur={() => handleBlur('email')}
              placeholder="Enter your email"
            />
            {touched.email && fieldErrors.email && (
              <span className="field-error-text">⚠ {fieldErrors.email}</span>
            )}
            {touched.email && !fieldErrors.email && email && (
              <span className="field-success-text">✓ Valid email</span>
            )}
          </div>

          {/* Password */}
          <div className="form-group">
            <label className="form-label">Password</label>
            <input
              type="password"
              className={inputClass('password')}
              value={password}
              onChange={(e) => handleChange('password', e.target.value, setPassword)}
              onBlur={() => handleBlur('password')}
              placeholder="Enter your password"
              maxLength={72}
            />
            {/* Password strength bar */}
            {password && (
              <div style={{ marginTop: '6px' }}>
                <div style={{ display: 'flex', gap: '4px', marginBottom: '4px' }}>
                  {[1, 2, 3, 4].map((i) => (
                    <div
                      key={i}
                      style={{
                        flex: 1,
                        height: '4px',
                        borderRadius: '2px',
                        backgroundColor: i <= strength.level ? strength.color : '#e0e0e0',
                        transition: 'background-color 0.3s',
                      }}
                    />
                  ))}
                </div>
                <span style={{ fontSize: '12px', color: strength.color, fontWeight: '600' }}>
                  {strength.label} password
                </span>
              </div>
            )}
            {touched.password && fieldErrors.password && (
              <span className="field-error-text">⚠ {fieldErrors.password}</span>
            )}
            {/* Password hints */}
            {password && (
              <ul className="password-hints">
                <li style={{ color: password.length >= 8 ? '#27ae60' : '#999' }}>
                  {password.length >= 8 ? '✓' : '○'} At least 8 characters
                </li>
                <li style={{ color: /[A-Z]/.test(password) ? '#27ae60' : '#999' }}>
                  {/[A-Z]/.test(password) ? '✓' : '○'} One uppercase letter
                </li>
                <li style={{ color: /\d/.test(password) ? '#27ae60' : '#999' }}>
                  {/\d/.test(password) ? '✓' : '○'} One number
                </li>
                <li style={{ color: /[!@#$%^&*(),.?":{}|<>]/.test(password) ? '#27ae60' : '#999' }}>
                  {/[!@#$%^&*(),.?":{}|<>]/.test(password) ? '✓' : '○'} One special character
                </li>
              </ul>
            )}
          </div>

          {/* Confirm Password */}
          <div className="form-group">
            <label className="form-label">Confirm Password</label>
            <input
              type="password"
              className={inputClass('confirmPassword')}
              value={confirmPassword}
              onChange={(e) => handleChange('confirmPassword', e.target.value, setConfirmPassword)}
              onBlur={() => handleBlur('confirmPassword')}
              placeholder="Confirm your password"
              maxLength={72}
            />
            {touched.confirmPassword && fieldErrors.confirmPassword && (
              <span className="field-error-text">⚠ {fieldErrors.confirmPassword}</span>
            )}
            {touched.confirmPassword && !fieldErrors.confirmPassword && confirmPassword && (
              <span className="field-success-text">✓ Passwords match!</span>
            )}
          </div>

          <button
            type="submit"
            className="btn btn-primary"
            disabled={loading}
            style={{ width: '100%', marginTop: '10px' }}
          >
            {loading ? 'Creating account...' : 'Create Account'}
          </button>
        </form>

        <div className="register-footer">
          <p>
            Already have an account?{' '}
            <Link to="/login" style={{ color: '#667eea', fontWeight: '600' }}>
              Sign in
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
};

export default Register;
