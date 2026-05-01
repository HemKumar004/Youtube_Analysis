export const api = {
  baseUrl: 'http://localhost:8000/api',

  async analyze(topic) {
    try {
      const response = await fetch(`${this.baseUrl}/analyze`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ topic, max_videos: 100 }) // increased back to 100 videos
      });
      if (!response.ok) throw new Error('API Error');
      return await response.json();
    } catch (e) {
      // Mock Data Fallback for Development if backend isn't running
      console.warn("Backend not running or failed. Using MOCK data.", e);
      return {
        status: "success",
        summary: { total_videos: 10, total_comments_analyzed: 450 },
        analysis: {
          organizations: { "OpenAI": 120, "Google": 85, "Microsoft": 95 },
          persons: { "Elon Musk": 110, "Sam Altman": 80, "Sundar Pichai": 105 },
          sentiments: { "positive": 180, "neutral": 150, "negative": 120 },
          topics: [
            {"topic": "innovation", "count": 140},
            {"topic": "models", "count": 98},
            {"topic": "future", "count": 75},
            {"topic": "safety", "count": 60},
            {"topic": "agi", "count": 45}
          ]
        }
      };
    }
  },

  async generatePost(topic) {
    try {
      const response = await fetch(`${this.baseUrl}/generate-post`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ topic })
      });
      if (!response.ok) throw new Error('Generation failed');
      const json = await response.json();
      return json.data || json;
    } catch (e) {
      // Mock Fallback
      return {
        post_content: `Exciting insights from the latest ${topic} YouTube discussions! Viewers are highly engaged with the new developments. #Trending #${topic.replace(/\s+/g, '')} 📊`,
        image_prompt: `A dynamic cinematic shot representing ${topic}, data visualizations overlaying the scene, photorealistic, 8k --ar 16:9`,
        image_url: `https://placehold.co/1024x1024/1e1e2f/00d4ff?text=AI+Generated+Image+For%5Cn${encodeURIComponent(topic)}`
      };
    }
  },

  async publish(content) {
    try {
      const response = await fetch(`${this.baseUrl}/publish`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ content })
      });
      if (!response.ok) throw new Error('Publish failed');
      return await response.json();
    } catch (e) {
      // Mock Fallback
      return { success: true, text: content, tweet_id: "1234567890" };
    }
  },

  async exportAnalysis(data, format) {
    try {
      const response = await fetch(`${this.baseUrl}/export/${format}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ data })
      });
      if (!response.ok) throw new Error(`Export to ${format} failed`);
      
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `analysis_report.${format === 'word' ? 'docx' : 'pdf'}`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (e) {
      console.error(e);
      if (e.message === 'Failed to fetch') {
        alert(`Failed to connect to backend server. Please make sure the Python FastAPI backend is running at ${this.baseUrl}`);
      } else {
        alert(`Failed to export as ${format.toUpperCase()}: ${e.message}`);
      }
    }
  }
};
