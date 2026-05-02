import React, { useState, useRef } from 'react';
import { useAuth } from '../context/AuthContext';
import Chatbot from '../components/Chatbot';
import UserStats from '../components/UserStats';
import History from '../components/History';
import Profile from '../components/Profile';
import './Dashboard.css';

const Dashboard = () => {
  const { user, logout } = useAuth();
  const [showProfile, setShowProfile] = useState(false);
  const [selectedHistory, setSelectedHistory] = useState(null);
  const [sidebarOpen, setSidebarOpen] = useState(true); // sidebar open by default
  const statsRef = useRef();
  const historyRef = useRef();

  const handleStatsUpdate = () => {
    console.log('🔄 Dashboard: Triggering refresh...');
    statsRef.current?.refresh();
    historyRef.current?.refresh();
  };

  const handleHistorySelect = (item) => {
    console.log('🖱️ Dashboard: History item selected:', item?.doc_id);
    setSelectedHistory(item);
  };

  return (
    <div className="dashboard-wrapper">

      {/* Hamburger toggle button */}
      <button
        type="button"
        className="sidebar-toggle-btn"
        onClick={() => setSidebarOpen(prev => !prev)}
        title={sidebarOpen ? 'Close sidebar' : 'Open sidebar'}
      >
        <span></span>
        <span></span>
        <span></span>
      </button>

      {/* Overlay when sidebar is open */}
      {sidebarOpen && (
        <div className="sidebar-overlay" onClick={() => setSidebarOpen(false)} />
      )}

      <aside className={`dashboard-sidebar ${sidebarOpen ? 'open' : ''}`}>
        <div className="sidebar-header">
          <button type="button" className="new-chat-btn" onClick={() => { setSelectedHistory(null); setSidebarOpen(false); }}>
            <span>+</span> New Summary
          </button>
        </div>

        <div className="sidebar-content">
          <UserStats ref={statsRef} sidebar={true} />
          <History
            ref={historyRef}
            onSelect={(item) => { handleHistorySelect(item); setSidebarOpen(false); }}
            onStatsUpdate={handleStatsUpdate}
          />
        </div>

        <div className="sidebar-footer">
          <div
            className="profile-trigger"
            onClick={() => setShowProfile(true)}
            title="View Profile"
          >
            <div className="avatar-circle">
              {user?.profile_photo ? (
                <img
                  src={user.profile_photo.startsWith('http') ? user.profile_photo : `http://localhost:8000${user.profile_photo}?t=${new Date().getTime()}`}
                  alt="Profile"
                  className="avatar-mini"
                />
              ) : (
                user?.name?.charAt(0).toUpperCase() || 'U'
              )}
            </div>
            <div className="user-info">
              <span className="user-name">{user?.name}</span>
            </div>
          </div>
          <button type="button" onClick={logout} className="logout-icon-btn" title="Logout">
            <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4" />
              <polyline points="16 17 21 12 16 7" />
              <line x1="21" y1="12" x2="9" y2="12" />
            </svg>
          </button>
        </div>
      </aside>

      <main className="dashboard-main-area">
        <header className="main-header">
          <div className="header-brand">
            <h1>Automated Text Summarizer</h1>
            <p>AI-Powered Abstractive Summarization</p>
          </div>
        </header>

        <div className="chat-content">
          <Chatbot
            onStatsUpdate={handleStatsUpdate}
            historyItem={selectedHistory}
          />
        </div>
      </main>

      {showProfile && <Profile onClose={() => setShowProfile(false)} />}
    </div>
  );
};

export default Dashboard;
