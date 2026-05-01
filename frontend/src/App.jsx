import { useState } from 'react'
import AnalysisDashboard from './components/AnalysisDashboard'
import PostGenerator from './components/PostGenerator'
import { api } from './services/api'

function App() {
  const [topic, setTopic] = useState('')
  const [analysisData, setAnalysisData] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleAnalyze = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError('')
    try {
      const result = await api.analyze(topic)
      setAnalysisData(result)
    } catch (err) {
      setError(err.message || 'Failed to analyze data')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app-container">
      <header className="header">
        <h1>YouTube AI Insights</h1>
        <p>Analyze discourse and automate social media engagement for any topic dynamically</p>
      </header>

      <div className="card">
        <form onSubmit={handleAnalyze} style={{ display: 'flex', gap: '1rem', alignItems: 'flex-end' }}>
          <div className="input-group" style={{ flex: 1, marginBottom: 0 }}>
            <label htmlFor="topic">Analysis Topic</label>
            <input
              type="text"
              id="topic"
              className="form-control"
              value={topic}
              onChange={(e) => setTopic(e.target.value)}
              placeholder="Enter a topic to analyze on YouTube..."
              required
            />
          </div>
          <button type="submit" className="btn btn-primary" disabled={loading}>
            {loading ? <span className="loader"></span> : 'Analyze YouTube Data'}
          </button>
        </form>
        {error && <div className="alert alert-error" style={{ marginTop: '1rem' }}>{error}</div>}
      </div>

      {loading && (
        <div style={{ textAlign: 'center', padding: '4rem 0' }}>
          <div className="loader" style={{ width: '48px', height: '48px', borderWidth: '4px' }}></div>
          <p style={{ marginTop: '1rem', color: 'var(--text-secondary)' }}>Extracting and processing YouTube comments via NLP...</p>
        </div>
      )}

      {analysisData && !loading && (
        <>
          <AnalysisDashboard data={analysisData} />
          <PostGenerator topic={topic} analysisSummary={analysisData.summary} />
        </>
      )}
    </div>
  )
}

export default App
