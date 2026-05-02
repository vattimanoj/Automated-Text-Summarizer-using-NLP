import React, { useState } from 'react';
import './Message.css';

const Message = ({ message, onExplain, onRate, onImageClick }) => {
  const [selectedRating, setSelectedRating] = useState(null);

  const handleRatingClick = (rating) => {
    setSelectedRating(rating);
    if (onRate && message.summaryId) {
      onRate(message.summaryId, rating);
    }
  };

  if (message.isLoading) {
    return (
      <div className="message bot">
        <div className="message-avatar">AI</div>
        <div className="message-content message-loading">
          <div className="loading-dot"></div>
          <div className="loading-dot"></div>
          <div className="loading-dot"></div>
        </div>
      </div>
    );
  }

  return (
    <div className={`message ${message.type}`}>
      <div className="message-avatar">
        {message.type === 'user' ? 'U' : 'AI'}
      </div>
      <div className="message-wrapper">
        <div
          className={`message-content ${message.isSummary ? 'message-summary' : ''
            } ${message.isError ? 'message-error' : ''} ${message.imageUrl ? 'message-has-image' : ''}`}
        >
          {/* Show image preview if this message has an image */}
          {message.imageUrl && (
            <div className="message-image-wrapper">
              <img
                src={message.imageUrl}
                alt="Uploaded"
                className="message-image"
                onClick={() => onImageClick ? onImageClick(message.imageUrl) : window.open(message.imageUrl, '_blank')}
                title="Click to view full size"
              />
            </div>
          )}
          {/* Message text below image */}
          {message.text && (
            <span className="message-text">{message.text}</span>
          )}
        </div>

        {message.isAction && (
          <div className="message-actions">
            <button
              className="action-button"
              onClick={() => onExplain?.(message.summaryId)}
            >
              🔍 Explain Summary
            </button>
            <div className="rating-section">
              <span style={{ fontSize: '12px', color: '#666', marginRight: '8px' }}>
                Rate:
              </span>
              <div className="rating-buttons">
                {[1, 2, 3, 4, 5].map((rating) => (
                  <button
                    key={rating}
                    className={`rating-button ${selectedRating === rating ? 'active' : ''
                      }`}
                    onClick={() => handleRatingClick(rating)}
                  >
                    {rating}
                  </button>
                ))}
              </div>
            </div>
          </div>
        )}

        {message.timestamp && (
          <div className="message-timestamp">
            {new Date(message.timestamp).toLocaleTimeString([], {
              hour: '2-digit',
              minute: '2-digit',
            })}
          </div>
        )}
      </div>
    </div>
  );
};

export default Message;
