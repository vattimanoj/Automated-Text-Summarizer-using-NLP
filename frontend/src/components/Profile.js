import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import axios from '../utils/axios';
import './Profile.css';

const Profile = ({ onClose }) => {
    const { user, updateUser, logout } = useAuth();
    const [name, setName] = useState(user?.name || '');
    const [currentPassword, setCurrentPassword] = useState('');
    const [newPassword, setNewPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');

    const [profileMsg, setProfileMsg] = useState({ type: '', text: '' });
    const [passwordMsg, setPasswordMsg] = useState({ type: '', text: '' });
    const [isLoading, setIsLoading] = useState(false);
    const [uploading, setUploading] = useState(false);

    // Validation state for profile form
    const [nameError, setNameError] = useState('');
    const [nameTouched, setNameTouched] = useState(false);

    // Validation state for password form
    const [pwdErrors, setPwdErrors] = useState({ current: '', newPwd: '', confirm: '' });
    const [pwdTouched, setPwdTouched] = useState({ current: false, newPwd: false, confirm: false });

    // ---- Validators ----
    const validateName = (val) => {
        if (!val.trim()) return 'Full name is required';
        if (val.trim().length < 2) return 'Name must be at least 2 characters';
        if (!/^[a-zA-Z\s]+$/.test(val.trim())) return 'Name can only contain letters and spaces';
        return '';
    };

    const validateCurrentPassword = (val) => {
        if (!val) return 'Current password is required';
        return '';
    };

    const validateNewPassword = (val) => {
        if (!val) return 'New password is required';
        if (val.length < 8) return 'Must be at least 8 characters';
        if (!/[A-Z]/.test(val)) return 'Must contain at least one uppercase letter';
        if (!/\d/.test(val)) return 'Must contain at least one number';
        if (!/[!@#$%^&*(),.?":{}|<>]/.test(val)) return 'Must contain at least one special character';
        return '';
    };

    const validateConfirmPassword = (val, pwd = newPassword) => {
        if (!val) return 'Please confirm your new password';
        if (val !== pwd) return 'Passwords do not match';
        return '';
    };

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

    // ---- Profile form handlers ----
    const handleNameChange = (val) => {
        setName(val);
        if (nameTouched) setNameError(validateName(val));
    };

    const handleUpdateProfile = async (e) => {
        e.preventDefault();
        setProfileMsg({ type: '', text: '' });
        setNameTouched(true);
        const err = validateName(name);
        setNameError(err);
        if (err) return;

        setIsLoading(true);
        try {
            const response = await axios.put('/api/user/profile', { name });
            updateUser(response.data);
            setProfileMsg({ type: 'success', text: 'Profile updated successfully!' });
            setTimeout(() => { onClose(); }, 1500);
        } catch (error) {
            console.error('Error updating profile:', error);
            setProfileMsg({ type: 'error', text: error.response?.data?.detail || 'Failed to update profile' });
        } finally {
            setIsLoading(false);
        }
    };

    const handlePhotoUpload = async (e) => {
        const file = e.target.files[0];
        if (!file) return;

        // Validate file type and size
        const allowedTypes = ['image/jpeg', 'image/png', 'image/gif', 'image/webp'];
        if (!allowedTypes.includes(file.type)) {
            setProfileMsg({ type: 'error', text: 'Only JPG, PNG, GIF, or WEBP images are allowed' });
            return;
        }
        if (file.size > 5 * 1024 * 1024) {
            setProfileMsg({ type: 'error', text: 'Image must be less than 5MB' });
            return;
        }

        const formData = new FormData();
        formData.append('file', file);
        setUploading(true);
        setProfileMsg({ type: '', text: '' });
        try {
            const response = await axios.post('/api/user/upload-photo', formData, {
                headers: { 'Content-Type': 'multipart/form-data' },
            });
            updateUser(response.data);
            setProfileMsg({ type: 'success', text: 'Photo uploaded successfully!' });
            setTimeout(() => { onClose(); }, 1000);
        } catch (error) {
            console.error('Error uploading photo:', error);
            setProfileMsg({ type: 'error', text: error.response?.data?.detail || 'Failed to upload photo' });
        } finally {
            setUploading(false);
        }
    };

    // ---- Password form handlers ----
    const handlePwdChange = (field, value) => {
        const setters = { current: setCurrentPassword, newPwd: setNewPassword, confirm: setConfirmPassword };
        setters[field](value);

        if (pwdTouched[field]) {
            const errors = { ...pwdErrors };
            if (field === 'current') errors.current = validateCurrentPassword(value);
            if (field === 'newPwd') {
                errors.newPwd = validateNewPassword(value);
                if (pwdTouched.confirm) errors.confirm = validateConfirmPassword(confirmPassword, value);
            }
            if (field === 'confirm') errors.confirm = validateConfirmPassword(value);
            setPwdErrors(errors);
        }
    };

    const handlePwdBlur = (field) => {
        setPwdTouched((prev) => ({ ...prev, [field]: true }));
        const errors = { ...pwdErrors };
        if (field === 'current') errors.current = validateCurrentPassword(currentPassword);
        if (field === 'newPwd') errors.newPwd = validateNewPassword(newPassword);
        if (field === 'confirm') errors.confirm = validateConfirmPassword(confirmPassword);
        setPwdErrors(errors);
    };

    const handleChangePassword = async (e) => {
        e.preventDefault();
        setPasswordMsg({ type: '', text: '' });

        const currentErr = validateCurrentPassword(currentPassword);
        const newErr = validateNewPassword(newPassword);
        const confirmErr = validateConfirmPassword(confirmPassword);

        setPwdErrors({ current: currentErr, newPwd: newErr, confirm: confirmErr });
        setPwdTouched({ current: true, newPwd: true, confirm: true });

        if (currentErr || newErr || confirmErr) return;

        setIsLoading(true);
        try {
            await axios.put('/api/user/change-password',
                { current_password: currentPassword, new_password: newPassword }
            );
            setPasswordMsg({ type: 'success', text: 'Password changed successfully! Please log in again.' });
            setCurrentPassword('');
            setNewPassword('');
            setConfirmPassword('');
            setPwdTouched({ current: false, newPwd: false, confirm: false });
            setTimeout(() => { logout(); }, 2000);
        } catch (error) {
            console.error('Error changing password:', error);
            setPasswordMsg({ type: 'error', text: error.response?.data?.detail || 'Failed to change password' });
        } finally {
            setIsLoading(false);
        }
    };

    const strength = getPasswordStrength(newPassword);

    const inputClass = (hasError, isTouched) =>
        `form-input ${isTouched && hasError ? 'input-error' : isTouched && !hasError ? 'input-success' : ''}`;

    return (
        <div className="profile-overlay" onClick={onClose}>
            <div className="profile-modal" onClick={(e) => e.stopPropagation()}>
                <div className="profile-header">
                    <h2>User Profile Settings</h2>
                    <button className="close-btn" onClick={onClose}>&times;</button>
                </div>

                <div className="profile-body">
                    <div className="profile-layout">
                        <div className="profile-left">
                            <div
                                className={`large-avatar ${uploading ? 'uploading' : ''}`}
                                onClick={() => document.getElementById('photo-input').click()}
                                title="Click to upload photo"
                            >
                                {user?.profile_photo ? (
                                    <img src={user.profile_photo.startsWith('http') ? user.profile_photo : `http://localhost:8000${user.profile_photo}`} alt="Profile" className="avatar-img" />
                                ) : (
                                    user?.name?.charAt(0).toUpperCase() || 'U'
                                )}
                                <div className="upload-overlay">
                                    <span>{uploading ? '...' : 'Upload'}</span>
                                </div>
                            </div>
                            <input
                                type="file"
                                id="photo-input"
                                hidden
                                accept="image/jpeg,image/png,image/gif,image/webp"
                                onChange={handlePhotoUpload}
                            />
                            <div className="profile-badge">Active User</div>
                            <p className="profile-joined">Member since {user?.created_at ? new Date(user.created_at).getFullYear() : 'N/A'}</p>
                        </div>

                        <div className="profile-right">
                            {/* Update Profile Section */}
                            <section className="profile-section">
                                <h3>Update Information</h3>
                                <form onSubmit={handleUpdateProfile} noValidate>
                                    <div className="form-group">
                                        <label>Email Address</label>
                                        <input type="text" value={user?.email} disabled className="form-input" />
                                    </div>
                                    <div className="form-group">
                                        <label>Full Name</label>
                                        <input
                                            type="text"
                                            value={name}
                                            onChange={(e) => handleNameChange(e.target.value)}
                                            onBlur={() => { setNameTouched(true); setNameError(validateName(name)); }}
                                            className={inputClass(nameError, nameTouched)}
                                            placeholder="Enter your full name"
                                        />
                                        {nameTouched && nameError && (
                                            <span className="field-error-text">⚠ {nameError}</span>
                                        )}
                                        {nameTouched && !nameError && name && (
                                            <span className="field-success-text">✓ Looks good!</span>
                                        )}
                                    </div>
                                    {profileMsg.text && (
                                        <div className={`alert alert-${profileMsg.type}`}>{profileMsg.text}</div>
                                    )}
                                    <button type="submit" className="btn btn-primary" disabled={isLoading || uploading}>
                                        Update Profile
                                    </button>
                                </form>
                            </section>

                            <hr />

                            {/* Change Password Section */}
                            <section className="profile-section">
                                <h3>Security Settings</h3>
                                <form onSubmit={handleChangePassword} noValidate>
                                    <div className="form-group">
                                        <label>Current Password</label>
                                        <input
                                            type="password"
                                            value={currentPassword}
                                            onChange={(e) => handlePwdChange('current', e.target.value)}
                                            onBlur={() => handlePwdBlur('current')}
                                            className={inputClass(pwdErrors.current, pwdTouched.current)}
                                            placeholder="Enter current password"
                                        />
                                        {pwdTouched.current && pwdErrors.current && (
                                            <span className="field-error-text">⚠ {pwdErrors.current}</span>
                                        )}
                                    </div>
                                    <div className="form-group">
                                        <label>New Password</label>
                                        <input
                                            type="password"
                                            value={newPassword}
                                            onChange={(e) => handlePwdChange('newPwd', e.target.value)}
                                            onBlur={() => handlePwdBlur('newPwd')}
                                            className={inputClass(pwdErrors.newPwd, pwdTouched.newPwd)}
                                            placeholder="Enter new password"
                                            minLength={8}
                                        />
                                        {/* Strength bar */}
                                        {newPassword && (
                                            <div style={{ marginTop: '6px' }}>
                                                <div style={{ display: 'flex', gap: '4px', marginBottom: '4px' }}>
                                                    {[1, 2, 3, 4].map((i) => (
                                                        <div key={i} style={{
                                                            flex: 1, height: '4px', borderRadius: '2px',
                                                            backgroundColor: i <= strength.level ? strength.color : '#e0e0e0',
                                                            transition: 'background-color 0.3s',
                                                        }} />
                                                    ))}
                                                </div>
                                                <span style={{ fontSize: '12px', color: strength.color, fontWeight: '600' }}>
                                                    {strength.label} password
                                                </span>
                                            </div>
                                        )}
                                        {pwdTouched.newPwd && pwdErrors.newPwd && (
                                            <span className="field-error-text">⚠ {pwdErrors.newPwd}</span>
                                        )}
                                        {/* Password hints */}
                                        {newPassword && (
                                            <ul className="password-hints">
                                                <li style={{ color: newPassword.length >= 8 ? '#27ae60' : '#999' }}>
                                                    {newPassword.length >= 8 ? '✓' : '○'} At least 8 characters
                                                </li>
                                                <li style={{ color: /[A-Z]/.test(newPassword) ? '#27ae60' : '#999' }}>
                                                    {/[A-Z]/.test(newPassword) ? '✓' : '○'} One uppercase letter
                                                </li>
                                                <li style={{ color: /\d/.test(newPassword) ? '#27ae60' : '#999' }}>
                                                    {/\d/.test(newPassword) ? '✓' : '○'} One number
                                                </li>
                                                <li style={{ color: /[!@#$%^&*(),.?":{}|<>]/.test(newPassword) ? '#27ae60' : '#999' }}>
                                                    {/[!@#$%^&*(),.?":{}|<>]/.test(newPassword) ? '✓' : '○'} One special character
                                                </li>
                                            </ul>
                                        )}
                                    </div>
                                    <div className="form-group">
                                        <label>Confirm Password</label>
                                        <input
                                            type="password"
                                            value={confirmPassword}
                                            onChange={(e) => handlePwdChange('confirm', e.target.value)}
                                            onBlur={() => handlePwdBlur('confirm')}
                                            className={inputClass(pwdErrors.confirm, pwdTouched.confirm)}
                                            placeholder="Confirm new password"
                                        />
                                        {pwdTouched.confirm && pwdErrors.confirm && (
                                            <span className="field-error-text">⚠ {pwdErrors.confirm}</span>
                                        )}
                                        {pwdTouched.confirm && !pwdErrors.confirm && confirmPassword && (
                                            <span className="field-success-text">✓ Passwords match!</span>
                                        )}
                                    </div>
                                    {passwordMsg.text && (
                                        <div className={`alert alert-${passwordMsg.type}`}>{passwordMsg.text}</div>
                                    )}
                                    <button type="submit" className="btn btn-secondary" disabled={isLoading || uploading}>
                                        Change Password
                                    </button>
                                </form>
                            </section>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Profile;
