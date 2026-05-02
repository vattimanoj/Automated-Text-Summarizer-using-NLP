import React from 'react';
import './ExplanationPanel.css';

const ExplanationPanel = ({ explanation, onClose }) => {
  if (!explanation) return null;

  const sentenceImportance = explanation.sentence_importance || {};
  const highlightedWords = explanation.highlighted_words || [];

  return (
    <div className="explanation-overlay">
      <div className="explanation-panel">
        <div className="explanation-header">
          <h3>🤖 Explainable AI - Summary Explanation</h3>
          <button className="close-button" onClick={onClose}>
            ✕
          </button>
        </div>

        <div className="explanation-content">
          <div className="explanation-section">
            <h4>Overall Score</h4>
            <div className="score-display">
              <span className="score-value">
                {explanation.average_importance_score || 0}%
              </span>
              <span className="score-label">Average Relevance</span>
            </div>
            <p className="explanation-text">
              {explanation.explanation_text ||
                'This summary was generated using attention mechanisms and semantic similarity scoring.'}
            </p>
          </div>

          <div className="explanation-section">
            <h4>Sentence Importance Scores</h4>
            <div className="sentence-scores">
              {Object.entries(sentenceImportance).map(([key, data]) => (
                <div
                  key={key}
                  className={`sentence-item ${
                    data.included ? 'included' : 'excluded'
                  }`}
                >
                  <div className="sentence-header">
                    <span className="sentence-key">{key.replace('_', ' ')}</span>
                    <span
                      className={`importance-badge ${
                        data.importance_score > 50 ? 'high' : 'low'
                      }`}
                    >
                      {data.importance_score.toFixed(1)}%
                    </span>
                  </div>
                  <p className="sentence-text">{data.text}</p>
                </div>
              ))}
            </div>
          </div>

          {highlightedWords.length > 0 && (
            <div className="explanation-section">
              <h4>Key Terms Highlighted</h4>
              <div className="highlighted-words">
                {highlightedWords.slice(0, 20).map((word, index) => (
                  <span key={index} className="word-tag">
                    {word}
                  </span>
                ))}
              </div>
            </div>
          )}

          <div className="explanation-section">
            <h4>How It Works</h4>
            <ul className="explanation-list">
              <li>
                ✅ Attention mechanisms identify important parts of the text
              </li>
              <li>
                ✅ Sentence importance is calculated using semantic similarity
              </li>
              <li>
                ✅ Key terms are extracted and highlighted for transparency
              </li>
              <li>
                ✅ The model generates new sentences (abstractive) rather than
                copying
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ExplanationPanel;
