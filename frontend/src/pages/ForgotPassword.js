import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import axios from '../utils/axios';
import './Login.css';

const ForgotPassword = () => {
    const navigate = useNavigate();
    const [step, setStep] = useState(1); // 1: Email, 2: Captcha, 3: New Password, 4: Success
    const [email, setEmail] = useState('');
    const [captcha, setCaptcha] = useState('');
    const [userCaptcha, setUserCaptcha] = useState('');
    const [newPassword, setNewPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [token, setToken] = useState('');
    const [error, setError] = useState('');
    const [captchaVerified, setCaptchaVerified] = useState(false);
    const [loading, setLoading] = useState(false);

    // Generate random CAPTCHA
    const generateCaptcha = () => {
        const chars = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ';
        let result = '';
        for (let i = 0; i < 6; i++) {
            result += chars.charAt(Math.floor(Math.random() * chars.length));
        }
        setCaptcha(result);
        setUserCaptcha('');
        setCaptchaVerified(false);
    };

    useEffect(() => {
        if (step === 2) {
            generateCaptcha();
        }
    }, [step]);

    const handleEmailSubmit = async (e) => {
        e.preventDefault();
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(email)) {
            setError('Please enter a valid email address.');
            return;
        }
        setError('');
        setLoading(true);
        try {
            const response = await axios.post('/api/auth/forgot-password', { email });
            setToken(response.data.reset_token);
            setStep(2);
        } catch (err) {
            setError(err.response?.data?.detail || 'User with this email not found.');
        } finally {
            setLoading(false);
        }
    };

    const handleCaptchaSubmit = (e) => {
        e.preventDefault();
        if (userCaptcha === captcha) {
            setCaptchaVerified(true);
            setError('');
            setTimeout(() => {
                setStep(3);
            }, 1000); // 1 second delay to show the success mark
        } else {
            setError('Invalid Captcha. Please try again.');
            generateCaptcha();
        }
    };

    const handlePasswordSubmit = async (e) => {
        e.preventDefault();
        if (newPassword.length < 8) {
            setError('Password must be at least 8 characters long.');
            return;
        }
        if (!/[A-Z]/.test(newPassword)) {
            setError('Password must contain at least one uppercase letter.');
            return;
        }
        if (!/\d/.test(newPassword)) {
            setError('Password must contain at least one number.');
            return;
        }
        if (!/[!@#$%^&*(),.?":{}|<>]/.test(newPassword)) {
            setError('Password must contain at least one special character.');
            return;
        }
        if (newPassword !== confirmPassword) {
            setError('Passwords do not match.');
            return;
        }
        setError('');
        setLoading(true);
        try {
            await axios.post('/api/auth/reset-password', {
                token: token,
                new_password: newPassword
            });
            setStep(4);
            setTimeout(() => {
                navigate('/login');
            }, 3000);
        } catch (err) {
            setError(err.response?.data?.detail || 'Failed to reset password.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="login-container">
            <div className="login-card">
                <div className="login-header">
                    <h1>Forgot Password</h1>
                    {step === 1 && <p>Enter your email to proceed</p>}
                    {step === 2 && <p>Please verify you are not a robot</p>}
                    {step === 3 && <p>Set your new password</p>}
                    {step === 4 && <p>Success!</p>}
                </div>

                {error && <div className="alert alert-error">{error}</div>}
                {step === 4 && (
                    <div className="alert alert-success">
                        Password reset successfully! Redirecting to login...
                    </div>
                )}

                {step === 1 && (
                    <form onSubmit={handleEmailSubmit} className="login-form">
                        <div className="form-group">
                            <label className="form-label">Email</label>
                            <input
                                type="email"
                                className="form-input"
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                                placeholder="Enter your email"
                                required
                            />
                        </div>
                        <button type="submit" className="btn btn-primary" disabled={loading} style={{ width: '100%' }}>
                            {loading ? 'Processing...' : 'Proceed'}
                        </button>
                    </form>
                )}

                {step === 2 && (
                    <form onSubmit={handleCaptchaSubmit} className="login-form">
                        <div className="form-group" style={{ textAlign: 'center' }}>
                            <div style={{
                                background: captchaVerified ? '#e6fffa' : '#f0f2f5',
                                padding: '10px',
                                fontSize: '24px',
                                fontWeight: 'bold',
                                letterSpacing: '5px',
                                fontStyle: 'italic',
                                textDecoration: captchaVerified ? 'none' : 'line-through',
                                marginBottom: '15px',
                                borderRadius: '5px',
                                userSelect: 'none',
                                color: captchaVerified ? '#38a169' : '#4a5568',
                                transition: 'all 0.3s ease'
                            }}>
                                {captchaVerified ? '✓ Verified' : captcha}
                            </div>
                            {!captchaVerified && (
                                <button type="button" onClick={generateCaptcha} style={{ fontSize: '0.8rem', color: '#667eea', border: 'none', background: 'none', cursor: 'pointer', marginBottom: '10px' }}>
                                    Refresh Captcha
                                </button>
                            )}
                            <input
                                type="text"
                                className="form-input"
                                value={userCaptcha}
                                onChange={(e) => setUserCaptcha(e.target.value)}
                                placeholder="Enter Captcha"
                                required
                                disabled={captchaVerified}
                                style={{ borderColor: captchaVerified ? '#38a169' : '' }}
                            />
                        </div>
                        <button
                            type="submit"
                            className="btn btn-primary"
                            style={{
                                width: '100%',
                                background: captchaVerified ? '#38a169' : '',
                                borderColor: captchaVerified ? '#38a169' : ''
                            }}
                            disabled={captchaVerified}
                        >
                            {captchaVerified ? 'Success!' : 'Verify Captcha'}
                        </button>
                    </form>
                )}

                {step === 3 && (
                    <form onSubmit={handlePasswordSubmit} className="login-form">
                        <div className="form-group">
                            <label className="form-label">New Password</label>
                            <input
                                type="password"
                                className={`form-input ${newPassword && (newPassword.length < 8 || !/[A-Z]/.test(newPassword) || !/\d/.test(newPassword) || !/[!@#$%^&*(),.?":{}|<>]/.test(newPassword)) ? 'input-error' : newPassword ? 'input-success' : ''}`}
                                value={newPassword}
                                onChange={(e) => setNewPassword(e.target.value)}
                                placeholder="Enter new password"
                                required
                            />
                            {/* Password hints */}
                            {newPassword && (
                                <ul className="password-hints">
                                    <li style={{ color: newPassword.length >= 8 ? '#27ae60' : '#e74c3c' }}>
                                        {newPassword.length >= 8 ? '✓' : '○'} At least 8 characters
                                    </li>
                                    <li style={{ color: /[A-Z]/.test(newPassword) ? '#27ae60' : '#e74c3c' }}>
                                        {/[A-Z]/.test(newPassword) ? '✓' : '○'} One uppercase letter
                                    </li>
                                    <li style={{ color: /\d/.test(newPassword) ? '#27ae60' : '#e74c3c' }}>
                                        {/\d/.test(newPassword) ? '✓' : '○'} One number
                                    </li>
                                    <li style={{ color: /[!@#$%^&*(),.?":{}|<>]/.test(newPassword) ? '#27ae60' : '#e74c3c' }}>
                                        {/[!@#$%^&*(),.?":{}|<>]/.test(newPassword) ? '✓' : '○'} One special character
                                    </li>
                                </ul>
                            )}
                        </div>
                        <div className="form-group">
                            <label className="form-label">Confirm Password</label>
                            <input
                                type="password"
                                className="form-input"
                                value={confirmPassword}
                                onChange={(e) => setConfirmPassword(e.target.value)}
                                placeholder="Confirm new password"
                                required
                            />
                        </div>
                        <button type="submit" className="btn btn-primary" disabled={loading} style={{ width: '100%' }}>
                            {loading ? 'Updating...' : 'Reset Password'}
                        </button>
                    </form>
                )}

                <div className="login-footer">
                    <p>
                        Back to <Link to="/login" style={{ color: '#667eea', fontWeight: '600' }}>Login</Link>
                    </p>
                </div>
            </div>
        </div>
    );
};

export default ForgotPassword;
