import React, { useRef } from 'react';
import './InputArea.css';

const InputArea = ({ inputText, setInputText, onSend, onFileUpload, onImageUpload, isLoading }) => {
  const textareaRef = useRef(null);
  const fileInputRef = useRef(null);
  const imageInputRef = useRef(null);

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      onSend();
    }
  };

  const handleFileClick = () => {
    fileInputRef.current?.click();
  };

  const handleImageClick = () => {
    imageInputRef.current?.click();
  };

  return (
    <div className="input-area">
      <div className="input-toolbar">
        <button
          type="button"
          className="toolbar-button"
          onClick={handleFileClick}
          title="Upload .txt file"
        >
          📁 Upload File
        </button>
        <input
          ref={fileInputRef}
          type="file"
          accept=".txt,text/plain"
          onChange={onFileUpload}
          style={{ display: 'none' }}
        />

        <div className="image-upload-group">
          <button
            type="button"
            className="toolbar-button toolbar-button-image"
            onClick={handleImageClick}
            title="Upload image to extract & summarize text"
            disabled={isLoading}
          >
            📷 Upload Image
          </button>
        </div>
        <input
          ref={imageInputRef}
          type="file"
          accept="image/*"
          onChange={(e) => {
            const file = e.target.files[0];
            if (file && onImageUpload) {
              onImageUpload(file);
            }
            // reset so same file can be selected again
            e.target.value = '';
          }}
          style={{ display: 'none' }}
        />

        <span className="toolbar-hint">Shift+Enter for new line</span>
      </div>
      <div className="input-wrapper">
        <textarea
          ref={textareaRef}
          className="input-textarea"
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          onKeyDown={handleKeyPress}
          placeholder="Paste or type your text here... (Press Enter to summarize)"
          rows={4}
          readOnly={isLoading}
        />
        <button
          type="button"
          className="send-button"
          onClick={onSend}
          disabled={!inputText.trim() || isLoading}
        >
          {isLoading ? '⏳' : '📤'}
        </button>
      </div>
      <div className="input-footer">
        <span className="char-count">{inputText.length} characters</span>
        <span className="input-hint">
          Powered by T5/BART Transformer Models
        </span>
      </div>
    </div>
  );
};

export default InputArea;
