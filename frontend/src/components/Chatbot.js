import React, { useState, useEffect, useRef } from 'react';
import axios from '../utils/axios';
import Message from './Message';
import InputArea from './InputArea';
import ExplanationPanel from './ExplanationPanel';
import './Chatbot.css';



const Chatbot = ({ onExplanationRequest, onStatsUpdate, historyItem }) => {
  const [messages, setMessages] = useState([
    {
      id: 1,
      type: 'bot',
      text: "Hello! I'm your AI Text Summarizer. 👋\n\nI can help you summarize long texts using advanced NLP techniques. Just paste your text or type it here, and I'll create a concise summary for you!\n\n📷 You can also upload an image — I'll extract the text and summarize it in the same language!",
      timestamp: new Date(),
    },
  ]);
  const [inputText, setInputText] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [currentSummary, setCurrentSummary] = useState(null);
  const [currentExplanation, setCurrentExplanation] = useState(null);
  const [showExplanation, setShowExplanation] = useState(false);
  const [fullScreenImage, setFullScreenImage] = useState(null);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    if (historyItem) {
      console.log('📖 Chatbot: Loading history item...', historyItem.doc_id);

      let extractedImageUrl = null;
      let textToShow = historyItem.original_text;
      let extractedTextNote = null;

      if (historyItem.domain === 'image' && typeof textToShow === 'string') {
        const matchUrl = textToShow.match(/^\[ImageURL:\s*([^\]]+)\]\n\n([\s\S]*)$/);
        if (matchUrl) {
          extractedImageUrl = axios.defaults.baseURL + matchUrl[1];
          textToShow = null;
          extractedTextNote = `✅ Text extracted from image. Here's the summary:`;
        } else {
          const oldMatch = textToShow.match(/^\[Image:\s*([^\]]+)\]\n\n([\s\S]*)$/);
          if (oldMatch) {
            textToShow = `📷 ${oldMatch[1]}\n\n(Image not available)\n\n${oldMatch[2]}`;
          }
        }
      }

      const historyMessages = [
        {
          id: 'user-h-' + historyItem.doc_id,
          type: 'user',
          text: textToShow,
          imageUrl: extractedImageUrl,
          timestamp: new Date(historyItem.created_at),
        }
      ];

      if (extractedTextNote && historyItem.summary_text) {
        historyMessages.push({
          id: 'bot-extracted-' + historyItem.doc_id,
          type: 'bot',
          text: extractedTextNote,
          timestamp: new Date(historyItem.created_at),
        });
      }

      if (historyItem.summary_text) {
        historyMessages.push({
          id: 'bot-h-' + historyItem.doc_id,
          type: 'bot',
          text: historyItem.summary_text,
          timestamp: new Date(historyItem.created_at),
          isSummary: true,
          summaryId: historyItem.doc_id,
        });

        historyMessages.push({
          id: 'action-h-' + historyItem.doc_id,
          type: 'bot',
          text: 'Loaded from history. What would you like to do?',
          timestamp: new Date(historyItem.created_at),
          isAction: true,
          summaryId: historyItem.doc_id,
        });
      } else {
        historyMessages.push({
          id: 'bot-h-none-' + historyItem.doc_id,
          type: 'bot',
          text: 'No summary generated yet for this document.',
          timestamp: new Date(historyItem.created_at),
        });
      }

      setMessages(historyMessages);
      setCurrentSummary({ text: historyItem.summary_text, id: historyItem.summary_id, docId: historyItem.doc_id });
      setCurrentExplanation(historyItem.explanation);
    } else {
      // Revert to welcome message when historyItem is cleared (New Summary)
      setMessages([
        {
          id: 1,
          type: 'bot',
          text: "Hello! I'm your AI Text Summarizer. 👋\n\nI can help you summarize long texts using advanced NLP techniques. Just paste your text or type it here, and I'll create a concise summary for you!\n\n📷 You can also upload an image — I'll extract the text and summarize it in the same language!",
          timestamp: new Date(),
        },
      ]);
      setCurrentSummary(null);
      setCurrentExplanation(null);
    }
  }, [historyItem]);

  const handleSummarize = async (textOverride) => {
    // If textOverride is an event or not a string, use inputText
    const textToSummarize = typeof textOverride === 'string' ? textOverride : inputText;

    if (!textToSummarize || !textToSummarize.trim() || isLoading) return;

    const userMessage = {
      id: Date.now(),
      type: 'user',
      text: textToSummarize,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);

    // Only clear input if we're using the standard input (no string override)
    if (typeof textOverride !== 'string') {
      setInputText('');
    }

    setIsLoading(true);

    // Add loading message
    const loadingMessage = {
      id: Date.now() + 1,
      type: 'bot',
      text: 'Generating summary...',
      isLoading: true,
      timestamp: new Date(),
    };
    setMessages((prev) => [...prev, loadingMessage]);

    try {
      const response = await axios.post('/api/summarize/text', {
        text: textToSummarize,
        domain: 'general',
        max_length: 256,
        min_length: 50,
      });

      const { summary, explanation, summary_id, document_id } = response.data;

      // Remove loading message
      setMessages((prev) => prev.filter((msg) => !msg.isLoading));

      // Add summary message
      const summaryMessage = {
        id: messages.length + 2,
        type: 'bot',
        text: summary,
        timestamp: new Date(),
        isSummary: true,
        summaryId: summary_id,
      };

      // Add action buttons message
      const actionMessage = {
        id: messages.length + 3,
        type: 'bot',
        text: 'What would you like to do?',
        timestamp: new Date(),
        isAction: true,
        summaryId: summary_id,
      };

      setMessages((prev) => [...prev, summaryMessage, actionMessage]);
      setCurrentSummary({ text: summary, id: summary_id, docId: document_id });
      setCurrentExplanation(explanation);

      // Trigger stats refresh (documents + summaries count)
      console.log('✅ Chatbot: Summary generated, calling onStatsUpdate...');
      onStatsUpdate?.();

      // Auto-scroll
      setTimeout(scrollToBottom, 100);
    } catch (error) {
      console.error('Error summarizing:', error);
      setMessages((prev) => {
        const updated = prev.filter((msg) => !msg.isLoading);
        return [
          ...updated,
          {
            id: updated.length + 1,
            type: 'bot',
            text: `Sorry, I encountered an error: ${error.response?.data?.detail || 'Unknown error'}. Please try again.`,
            timestamp: new Date(),
            isError: true,
          },
        ];
      });
    } finally {
      setIsLoading(false);
    }
  };

  // ── Image upload handler ─────────────────────────────────────────────────
  const handleImageUpload = async (file) => {
    if (!file || isLoading) return;

    // Smart Redirect: If user picks a .txt file in the image slot, handle it as a text file
    if (file.type === 'text/plain' || file.name.endsWith('.txt')) {
      console.log('📄 Chatbot: .txt file detected in image upload, redirecting to handleFileUpload...');
      handleFileUpload(file); // Manual summarize (default)
      return;
    }

    // Create a local object URL for instant preview in chat
    const localPreviewUrl = URL.createObjectURL(file);

    // Add image bubble to chat immediately (user side)
    const imageUserMsg = {
      id: Date.now(),
      type: 'user',
      text: null,
      imageUrl: localPreviewUrl,
      timestamp: new Date(),
    };
    setMessages((prev) => [...prev, imageUserMsg]);
    setIsLoading(true);

    // Add loading bubble
    const loadingMsg = {
      id: Date.now() + 1,
      type: 'bot',
      text: 'Extracting text from image and generating summary...',
      isLoading: true,
      timestamp: new Date(),
    };
    setMessages((prev) => [...prev, loadingMsg]);
    setTimeout(scrollToBottom, 100);

    try {
      const formData = new FormData();
      formData.append('file', file);

      const response = await axios.post('/api/summarize/image', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });

      const { summary, detected_language, explanation, summary_id, document_id } = response.data;

      // Remove loading message
      setMessages((prev) => prev.filter((msg) => !msg.isLoading));

      // Language label
      const langLabel = detected_language && detected_language !== 'en'
        ? ` (${detected_language.toUpperCase()} detected)`
        : '';

      // Show extracted text note
      const extractedNoteMsg = {
        id: Date.now() + 2,
        type: 'bot',
        text: `✅ Text extracted from image${langLabel}. Here's the summary:`,
        timestamp: new Date(),
      };

      // Summary message
      const summaryMsg = {
        id: Date.now() + 3,
        type: 'bot',
        text: summary,
        timestamp: new Date(),
        isSummary: true,
        summaryId: summary_id,
      };

      // Action message
      const actionMsg = {
        id: Date.now() + 4,
        type: 'bot',
        text: 'What would you like to do?',
        timestamp: new Date(),
        isAction: true,
        summaryId: summary_id,
      };

      setMessages((prev) => [...prev, extractedNoteMsg, summaryMsg, actionMsg]);
      setCurrentSummary({ text: summary, id: summary_id, docId: document_id });
      setCurrentExplanation(explanation);
      onStatsUpdate?.();
      setTimeout(scrollToBottom, 100);
    } catch (error) {
      console.error('Image upload error:', error);
      setMessages((prev) => {
        const updated = prev.filter((msg) => !msg.isLoading);
        return [
          ...updated,
          {
            id: Date.now() + 5,
            type: 'bot',
            text: `❌ Could not process image: ${error.response?.data?.detail || error.message || 'Unknown error'}. Make sure the image has readable text.`,
            timestamp: new Date(),
            isError: true,
          },
        ];
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleExplain = async (summaryId) => {
    // If explanation is already in memory, just show it
    if (currentExplanation && currentSummary?.id === summaryId) {
      setShowExplanation(true);
      return;
    }

    // Fetch explanation from backend using summary_id
    try {
      // We need doc_id too — find it from current messages or historyItem
      const docId = historyItem?.doc_id || currentSummary?.docId;

      if (!docId || !summaryId) {
        alert('Explanation not available. Please generate a new summary.');
        return;
      }

      const response = await axios.get(
        `/api/summarize/document/${docId}/explanation`,
        { params: { summary_id: summaryId } }
      );

      setCurrentExplanation(response.data);
      setShowExplanation(true);
    } catch (error) {
      console.error('Error fetching explanation:', error);
      alert('Explanation not available. Please generate a new summary.');
    }
  };

  const handleRate = async (summaryId, rating) => {
    try {
      await axios.post('/api/feedback/', {
        summary_id: summaryId,
        rating: rating,
      });

      const feedbackMessage = {
        id: messages.length + 1,
        type: 'bot',
        text: `Thank you for your feedback! Your rating (${rating}/5) helps improve the model. 🎉`,
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, feedbackMessage]);

      // Trigger stats refresh (feedback count + average rating)
      onStatsUpdate?.();

      scrollToBottom();
    } catch (error) {
      console.error('Error submitting feedback:', error);
      alert('Could not submit feedback. Please try again.');
    }
  };

  const handleFileUpload = async (eventOrFile, autoSummarize = false) => {
    const file = eventOrFile.target ? eventOrFile.target.files[0] : eventOrFile;
    if (!file) return;

    if (file.type !== 'text/plain' && !file.name.endsWith('.txt')) {
      alert('Please upload a .txt file');
      return;
    }

    try {
      const buffer = await file.arrayBuffer();
      const uint8 = new Uint8Array(buffer);
      let text = '';

      // 1. Check for BOMs (Byte Order Marks)
      if (uint8[0] === 0xEF && uint8[1] === 0xBB && uint8[2] === 0xBF) {
        text = new TextDecoder('utf-8').decode(uint8.slice(3));
      } else if (uint8[0] === 0xFF && uint8[1] === 0xFE) {
        text = new TextDecoder('utf-16le').decode(uint8.slice(2));
      } else if (uint8[0] === 0xFE && uint8[1] === 0xFF) {
        text = new TextDecoder('utf-16be').decode(uint8.slice(2));
      } else {
        // 2. No BOM - try UTF-8 first (strict)
        try {
          const utf8Decoder = new TextDecoder('utf-8', { fatal: true });
          text = utf8Decoder.decode(uint8);
        } catch (err) {
          // 3. Fallback to Windows-1252 (Common ANSI)
          text = new TextDecoder('windows-1252').decode(uint8);
        }
      }

      // 4. Check for literal question marks (evidence of encoding loss)
      const qmarkCount = (text.match(/\?\?\?\?/g) || []).length;
      const indicMatch = text.match(/[\u0B80-\u0C7F\u0900-\u097F]/g); // Tamil/Telugu/Hindi
      const indicCount = indicMatch ? indicMatch.length : 0;

      if (qmarkCount > 0 && indicCount < 10) {
        console.warn('⚠️ Chatbot: Potential encoding loss detected (ANSI instead of UTF-8)');

        const warningMsg = {
          id: Date.now() - 1,
          type: 'bot',
          text: "⚠️ **Warning: Possible encoding issue detected.**\n\nIt looks like this file might have been saved in 'ANSI' format instead of 'UTF-8' (common in Notepad). This causes Tamil/Telugu/Hindi text to turn into question marks.\n\n**To fix this:**\n1. Open your file in Notepad. \n2. Go to **File > Save As**. \n3. Change **Encoding** (at the bottom) to **UTF-8**. \n4. Save and upload again!",
          timestamp: new Date(),
          isError: true,
        };
        setMessages((prev) => [...prev, warningMsg]);
      }

      setInputText(text);
      if (eventOrFile.target) eventOrFile.target.value = '';

      // Instead of auto-summarizing, add a small helper note
      const uploadNote = {
        id: Date.now() + 1,
        type: 'bot',
        text: `📄 **File uploaded:** "${file.name}"\n\nThe text is now in the input box below. You can review or edit it, then click the **Summarize** button to generate the summary.`,
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, uploadNote]);

    } catch (err) {
      console.error("File read error:", err);
      // Last resort fallback
      const text = await file.text();
      setInputText(text);
      if (eventOrFile.target) eventOrFile.target.value = '';
    }
  };

  return (
    <div className="chatbot-container">
      <div className="chatbot-header">
        <h2>Chat with AI Summarizer</h2>
        <p>Powered by Transformer-based NLP</p>
      </div>

      <div className="chatbot-messages">
        {messages.map((message) => (
          <Message
            key={message.id}
            message={message}
            onExplain={handleExplain}
            onRate={handleRate}
            onImageClick={(url) => setFullScreenImage(url)}
          />
        ))}
        <div ref={messagesEndRef} />
      </div>

      {fullScreenImage && (
        <div className="fullscreen-image-overlay">
          <div className="fullscreen-image-header">
            <button className="back-button" onClick={() => setFullScreenImage(null)}>
              &#8592; Back to Chat
            </button>
          </div>
          <img src={fullScreenImage} alt="Fullscreen preview" className="fullscreen-image" />
        </div>
      )}

      <InputArea
        inputText={inputText}
        setInputText={setInputText}
        onSend={handleSummarize}
        onFileUpload={handleFileUpload}
        onImageUpload={handleImageUpload}
        isLoading={isLoading}
      />

      {showExplanation && currentExplanation && (
        <ExplanationPanel
          explanation={currentExplanation}
          onClose={() => setShowExplanation(false)}
        />
      )}
    </div>
  );
};

export default Chatbot;
