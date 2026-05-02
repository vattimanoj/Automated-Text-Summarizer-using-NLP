import React, { useState, useEffect, forwardRef, useImperativeHandle, useCallback } from 'react';
import { useAuth } from '../context/AuthContext';
import axios from '../utils/axios';
import './UserStats.css';

const UserStats = forwardRef(({ sidebar }, ref) => {
  const { user, token } = useAuth();
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  const fetchStats = useCallback(async () => {
    try {
      const response = await axios.get('/api/user/stats', {
        headers: { Authorization: `Bearer ${token}` },
      });
      setStats(response.data);
    } catch (error) {
      console.error('Error fetching stats:', error);
    } finally {
      setLoading(false);
    }
  }, [token]);

  useEffect(() => {
    if (user && token) {
      fetchStats();
    } else {
      setLoading(false);
    }
  }, [user, token, fetchStats]);

  // Expose refresh function to parent components
  useImperativeHandle(ref, () => ({
    refresh: () => {
      console.log('📊 UserStats: Refresh called, fetching stats...');
      fetchStats();
    }
  }));

  if (loading) return null;

  if (sidebar) {
    return (
      <div className="sidebar-stats">
        <div className="sidebar-stat-row">
          <span>Docs: {stats?.documents_count || 0}</span>
          <span>Summ: {stats?.summaries_count || 0}</span>
        </div>
        <div className="sidebar-stat-row">
          <span>Feedb: {stats?.feedback_count || 0}</span>
          <span>Rating: {stats?.average_rating ? stats.average_rating.toFixed(1) : '0.0'}</span>
        </div>
      </div>
    );
  }

  return (
    <div className="user-stats-card">
      <h3>📊 Your Statistics</h3>
      <div className="stats-grid">
        <div className="stat-item">
          <div className="stat-value">{stats?.documents_count || 0}</div>
          <div className="stat-label">Documents</div>
        </div>
        <div className="stat-item">
          <div className="stat-value">{stats?.summaries_count || 0}</div>
          <div className="stat-label">Summaries</div>
        </div>
        <div className="stat-item">
          <div className="stat-value">{stats?.feedback_count || 0}</div>
          <div className="stat-label">Feedback</div>
        </div>
        <div className="stat-item">
          <div className="stat-value">
            {stats?.average_rating
              ? stats.average_rating.toFixed(1)
              : '0.0'}
          </div>
          <div className="stat-label">Avg Rating</div>
        </div>
      </div>
    </div>
  );
});

export default UserStats;
