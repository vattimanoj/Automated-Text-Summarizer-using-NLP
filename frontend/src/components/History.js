import React, { useState, useEffect, forwardRef, useImperativeHandle, useCallback } from 'react';
import axios from '../utils/axios';
import './History.css';

const History = forwardRef(({ onSelect, onStatsUpdate }, ref) => {
    const [history, setHistory] = useState([]);
    const [loading, setLoading] = useState(true);
    const [isOpen, setIsOpen] = useState(true);
    const [activeId, setActiveId] = useState(null); // currently viewing item

    const fetchHistory = useCallback(async () => {
        try {
            const response = await axios.get('/api/summarize/history');
            setHistory(response.data);
        } catch (error) {
            console.error('Error fetching history:', error);
        } finally {
            setLoading(false);
        }
    }, []);

    useEffect(() => {
        fetchHistory();
    }, [fetchHistory]);

    useImperativeHandle(ref, () => ({
        refresh: () => {
            console.log('📜 History: Refresh called...');
            fetchHistory();
        }
    }));

    const handleSelect = (item) => {
        setActiveId(item ? item.doc_id : null);
        if (onSelect) {
            onSelect(item);
        }
    };

    const handleDelete = async (e, item) => {
        e.stopPropagation();

        if (!window.confirm('Are you sure you want to delete this history item?')) {
            return;
        }

        try {
            await axios.delete(`/api/summarize/document/${item.doc_id}`);
            fetchHistory();

            // Notify parent to refresh stats
            if (onStatsUpdate) {
                onStatsUpdate();
            }

            if (onSelect) {
                onSelect(null);
            }
        } catch (error) {
            console.error('Error deleting history item:', error);
            alert('Failed to delete history item. Please try again.');
        }
    };

    return (
        <div className="sidebar-history-container">
            <h3
                className="sidebar-section-title clickable-title"
                onClick={() => setIsOpen(prev => !prev)}
                title={isOpen ? 'Hide history' : 'Show history'}
            >
                <span>Recent History</span>
                <span className={`history-arrow ${isOpen ? 'open' : ''}`}>▾</span>
            </h3>

            {isOpen && (
                loading && history.length === 0 ? (
                    <p className="no-history-sidebar">Loading...</p>
                ) : history.length === 0 ? (
                    <p className="no-history-sidebar">No summaries yet.</p>
                ) : (
                    <div className="sidebar-history-list">
                        {history.map((item) => (
                            <div
                                key={item.doc_id}
                                className={`sidebar-history-item${activeId === item.doc_id ? ' active' : ''}`}
                                onClick={() => handleSelect(item)}
                                title={item.summary_text}
                            >
                                <span className={`history-icon ${item.domain === 'image' ? 'image-icon' : ''}`}>
                                    {item.domain === 'image' ? '📷' : '💬'}
                                </span>
                                <span className="history-text">
                                    {item.summary_text
                                        ? (item.summary_text.substring(0, 30) + (item.summary_text.length > 30 ? '...' : ''))
                                        : 'New Summary'}
                                </span>
                                <button
                                    className="delete-history-btn"
                                    onClick={(e) => handleDelete(e, item)}
                                    title="Delete History"
                                >
                                    &times;
                                </button>
                            </div>
                        ))}
                    </div>
                )
            )}
        </div>
    );
});

export default History;
