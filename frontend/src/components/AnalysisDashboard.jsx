import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';

const COLORS = ['#3b82f6', '#10b981', '#ef4444', '#f59e0b', '#8b5cf6'];

export default function AnalysisDashboard({ data }) {
  const { analysis, summary } = data;

  const orgData = Object.entries(analysis.organizations || {}).map(([name, count]) => ({ name, count }));
  const personData = Object.entries(analysis.persons || {}).map(([name, count]) => ({ name, count }));
  const sentimentData = Object.entries(analysis.sentiments || {}).map(([name, value]) => ({ name, value }));

  return (
    <div className="card">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
        <h2>Data Analysis Results</h2>
        <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
          <button 
            className="btn" 
            style={{ padding: '0.4rem 0.8rem', fontSize: '0.9rem', background: 'var(--bg-secondary)', border: '1px solid var(--border-color)', cursor: 'pointer' }}
            onClick={() => import('../services/api').then(m => m.api.exportAnalysis(data, 'pdf'))}
          >
            Export PDF
          </button>
          <button 
            className="btn" 
            style={{ padding: '0.4rem 0.8rem', fontSize: '0.9rem', background: 'var(--bg-secondary)', border: '1px solid var(--border-color)', cursor: 'pointer' }}
            onClick={() => import('../services/api').then(m => m.api.exportAnalysis(data, 'word'))}
          >
            Export Word
          </button>
          <div style={{ background: 'var(--bg-secondary)', padding: '0.5rem 1rem', borderRadius: '8px', fontSize: '0.9rem' }}>
            Extracted from <strong>{summary.total_videos}</strong> videos & <strong>{summary.total_comments_analyzed}</strong> comments
          </div>
        </div>
      </div>

      <div className="grid-2">
        <div style={{ height: '300px', background: 'var(--bg-secondary)', padding: '1rem', borderRadius: '12px' }}>
          <h3 style={{ textAlign: 'center', marginBottom: '1rem', color: 'var(--text-secondary)' }}>Sentiment Analysis</h3>
          <ResponsiveContainer width="100%" height="90%">
            <PieChart>
              <Pie
                data={sentimentData}
                cx="50%"
                cy="50%"
                innerRadius={60}
                outerRadius={80}
                paddingAngle={5}
                dataKey="value"
              >
                {sentimentData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip theme="dark" contentStyle={{ backgroundColor: 'var(--bg-card)', border: 'none', borderRadius: '8px' }} />
              <Legend verticalAlign="bottom" height={36}/>
            </PieChart>
          </ResponsiveContainer>
        </div>

        <div style={{ height: '300px', background: 'var(--bg-secondary)', padding: '1rem', borderRadius: '12px' }}>
          <h3 style={{ textAlign: 'center', marginBottom: '1rem', color: 'var(--text-secondary)' }}>Top Organizations</h3>
          <ResponsiveContainer width="100%" height="90%">
            <BarChart data={orgData}>
              <CartesianGrid strokeDasharray="3 3" stroke="var(--border-color)" />
              <XAxis dataKey="name" stroke="var(--text-secondary)" />
              <YAxis stroke="var(--text-secondary)" />
              <Tooltip cursor={{fill: 'rgba(255,255,255,0.05)'}} contentStyle={{ backgroundColor: 'var(--bg-card)', border: 'none', borderRadius: '8px' }} />
              <Bar dataKey="count" fill="var(--accent-color)" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
      
      <div className="grid-2" style={{ marginTop: '2rem' }}>
        <div style={{ height: '300px', background: 'var(--bg-secondary)', padding: '1rem', borderRadius: '12px' }}>
          <h3 style={{ textAlign: 'center', marginBottom: '1rem', color: 'var(--text-secondary)' }}>Top People Mentioned</h3>
          <ResponsiveContainer width="100%" height="90%">
            <BarChart data={personData}>
              <CartesianGrid strokeDasharray="3 3" stroke="var(--border-color)" />
              <XAxis dataKey="name" stroke="var(--text-secondary)" />
              <YAxis stroke="var(--text-secondary)" />
              <Tooltip cursor={{fill: 'rgba(255,255,255,0.05)'}} contentStyle={{ backgroundColor: 'var(--bg-card)', border: 'none', borderRadius: '8px' }} />
              <Bar dataKey="count" fill="#10b981" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      
        <div style={{ height: '300px', background: 'var(--bg-secondary)', padding: '1rem', borderRadius: '12px' }}>
          <h3 style={{ textAlign: 'center', marginBottom: '1rem', color: 'var(--text-secondary)' }}>Top Topics</h3>
          <ResponsiveContainer width="100%" height="90%">
            <BarChart data={analysis.topics}>
              <CartesianGrid strokeDasharray="3 3" stroke="var(--border-color)" />
              <XAxis dataKey="topic" stroke="var(--text-secondary)" />
              <YAxis stroke="var(--text-secondary)" />
              <Tooltip cursor={{fill: 'rgba(255,255,255,0.05)'}} contentStyle={{ backgroundColor: 'var(--bg-card)', border: 'none', borderRadius: '8px' }} />
              <Bar dataKey="count" fill="#8b5cf6" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}
