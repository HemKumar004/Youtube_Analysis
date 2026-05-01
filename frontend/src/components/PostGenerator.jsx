import React, { useState } from 'react';
import { api } from '../services/api';

export default function PostGenerator({ topic }) {
  const [postDraft, setPostDraft] = useState('');
  const [imagePrompt, setImagePrompt] = useState('');
  const [imageUrl, setImageUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [publishing, setPublishing] = useState(false);
  const [publishResult, setPublishResult] = useState(null);
  const [publishError, setPublishError] = useState('');

  const handleGenerate = async () => {
    setLoading(true);
    setImageUrl(''); // 🔥 reset image before loading

    try {
      const data = await api.generatePost(topic);

      console.log("API RESPONSE:", data);

      setPostDraft(data.post_content);
      setImagePrompt(data.image_prompt);
      setImageUrl(data.image_url);

    } catch (e) {
      console.error(e);
      alert("Failed to generate post");
    } finally {
      setLoading(false);
    }
  };

  const handlePublish = async () => {
    setPublishing(true);
    setPublishError('');
    setPublishResult(null);

    try {
      const result = await api.publish(postDraft);
      setPublishResult(result);
    } catch (e) {
      console.error(e);
      setPublishError(e.message || "Failed to publish");
    } finally {
      setPublishing(false);
    }
  };

  return (
    <div className="card">
      <h2 style={{ marginBottom: '1.5rem' }}>AI Social Media Automation</h2>

      {/* GENERATE BUTTON */}
      <button className="btn btn-primary" onClick={handleGenerate} disabled={loading}>
        {loading ? <span className="loader"></span> : 'Generate Viral Post'}
      </button>

      {postDraft && (
        <div style={{ marginTop: '1.5rem' }}>

          {/* TEXT OUTPUT */}
          <div className="input-group">
            <label>Draft</label>
            <textarea
              className="form-control"
              value={postDraft}
              onChange={(e) => setPostDraft(e.target.value)}
              rows={4}
            />
          </div>

          {/* IMAGE PROMPT */}
          {imagePrompt && (
            <div className="input-group" style={{ marginTop: '1rem' }}>
              <label>AI Image Prompt</label>
              <textarea
                className="form-control"
                value={imagePrompt}
                onChange={(e) => setImagePrompt(e.target.value)}
                rows={3}
                style={{ background: 'var(--bg-secondary)' }}
              />
            </div>
          )}

          {/* IMAGE LOADING */}
          {loading && (
            <div style={{ marginTop: '1rem' }}>
              <p>🎨 Generating AI image...</p>
            </div>
          )}

          {/* IMAGE DISPLAY */}
          {!loading && imageUrl && (
            <div
              style={{
                marginTop: '1rem',
                borderRadius: '12px',
                overflow: 'hidden',
                border: '1px solid var(--border-color)',
                width: '100%',
                maxWidth: '500px'
              }}
            >
              <img
                src={imageUrl}
                alt="AI Generated"
                style={{
                  width: '100%',
                  height: '300px',
                  objectFit: 'cover',
                  display: 'block'
                }}
              />

              {/* DOWNLOAD BUTTON */}
              <div style={{ padding: '10px', textAlign: 'center' }}>
                <a href={imageUrl} download="ai-image.png">
                  <button className="btn">Download Image</button>
                </a>
              </div>
            </div>
          )}

          {/* PUBLISH BUTTON */}
          <button
            className="btn"
            style={{ background: '#1da1f2', color: 'white', marginTop: '1rem' }}
            onClick={handlePublish}
            disabled={publishing}
          >
            {publishing ? <span className="loader"></span> : 'Publish to Twitter (X)'}
          </button>

          {/* ERROR */}
          {publishError && (
            <div className="alert" style={{
              marginTop: '1rem',
              background: 'rgba(239, 68, 68, 0.1)',
              color: '#ef4444',
              border: '1px solid rgba(239, 68, 68, 0.2)'
            }}>
              {publishError}
            </div>
          )}

          {/* SUCCESS */}
          {publishResult && (
            <div className="alert" style={{
              marginTop: '1rem',
              background: 'rgba(16, 185, 129, 0.1)',
              color: '#10b981',
              border: '1px solid rgba(16, 185, 129, 0.2)'
            }}>
              Successfully published!

              {(() => {
                const tweetId = publishResult?.data?.tweet_id || publishResult?.tweet_id;
                if (tweetId) {
                  const postUrl = `https://twitter.com/user/status/${tweetId}`;
                  return (
                    <div style={{ marginTop: '0.5rem', fontWeight: 'bold' }}>
                      <p>Tweet ID: {tweetId}</p>
                      <a href={postUrl} target="_blank" rel="noreferrer">
                        View Tweet
                      </a>
                    </div>
                  );
                }
                return null;
              })()}
            </div>
          )}

        </div>
      )}
    </div>
  );
}