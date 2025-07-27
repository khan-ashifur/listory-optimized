import React, { useState } from 'react';
import './QualityValidationReport.css';

const QualityValidationReport = ({ validationReport }) => {
  const [activeSection, setActiveSection] = useState(null);

  if (!validationReport) {
    return (
      <div className="quality-validation-report">
        <div className="no-report">
          <h3>Quality Validation</h3>
          <p>Generate a listing to see quality analysis</p>
        </div>
      </div>
    );
  }

  const getGradeColor = (grade) => {
    const gradeColors = {
      'A+': '#4CAF50', 'A': '#4CAF50',
      'B+': '#8BC34A', 'B': '#8BC34A',
      'C+': '#FFC107', 'C': '#FFC107',
      'D': '#FF9800', 'F': '#F44336'
    };
    return gradeColors[grade] || '#9E9E9E';
  };

  const getScoreColor = (score) => {
    if (score >= 8) return '#4CAF50';
    if (score >= 6) return '#8BC34A';
    if (score >= 4) return '#FFC107';
    return '#F44336';
  };

  const getIssueIcon = (type) => {
    const icons = {
      'critical': '🚨',
      'major': '⚠️',
      'minor': 'ℹ️',
      'enhancement': '💡'
    };
    return icons[type] || 'ℹ️';
  };

  return (
    <div className="quality-validation-report">
      <div className="report-header">
        <h3>Quality Validation Report</h3>
        <div className="overall-grade" style={{ backgroundColor: getGradeColor(validationReport.grade) }}>
          <span className="grade">{validationReport.grade}</span>
          <span className="score">{validationReport.overall_score}/10</span>
        </div>
      </div>

      <div className="score-summary">
        <div className="score-item">
          <span className="score-label">Emotion</span>
          <div className="score-bar">
            <div 
              className="score-fill" 
              style={{ 
                width: `${(validationReport.emotion_score / 10) * 100}%`,
                backgroundColor: getScoreColor(validationReport.emotion_score)
              }}
            ></div>
          </div>
          <span className="score-value">{validationReport.emotion_score}/10</span>
        </div>

        <div className="score-item">
          <span className="score-label">Conversion</span>
          <div className="score-bar">
            <div 
              className="score-fill" 
              style={{ 
                width: `${(validationReport.conversion_score / 10) * 100}%`,
                backgroundColor: getScoreColor(validationReport.conversion_score)
              }}
            ></div>
          </div>
          <span className="score-value">{validationReport.conversion_score}/10</span>
        </div>

        <div className="score-item">
          <span className="score-label">Trust</span>
          <div className="score-bar">
            <div 
              className="score-fill" 
              style={{ 
                width: `${(validationReport.trust_score / 10) * 100}%`,
                backgroundColor: getScoreColor(validationReport.trust_score)
              }}
            ></div>
          </div>
          <span className="score-value">{validationReport.trust_score}/10</span>
        </div>
      </div>

      <div className="report-summary">
        <p>{validationReport.summary}</p>
      </div>

      <div className="section-scores">
        <h4>Section Analysis</h4>
        {validationReport.section_scores.map((section, index) => (
          <div 
            key={index} 
            className={`section-item ${activeSection === index ? 'active' : ''}`}
            onClick={() => setActiveSection(activeSection === index ? null : index)}
          >
            <div className="section-header">
              <span className="section-name">{section.section}</span>
              <div className="section-score">
                <span className="score">{section.score}/{section.max_score}</span>
                <span className="percentage">({section.percentage}%)</span>
              </div>
            </div>
            
            {activeSection === index && (
              <div className="section-details">
                <p className="section-feedback">{section.feedback}</p>
                
                {section.strengths && section.strengths.length > 0 && (
                  <div className="strengths">
                    <h5>✅ Strengths:</h5>
                    <ul>
                      {section.strengths.map((strength, i) => (
                        <li key={i}>{strength}</li>
                      ))}
                    </ul>
                  </div>
                )}

                {section.improvements && section.improvements.length > 0 && (
                  <div className="improvements">
                    <h5>🎯 Improvements:</h5>
                    <ul>
                      {section.improvements.map((improvement, i) => (
                        <li key={i}>{improvement}</li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            )}
          </div>
        ))}
      </div>

      {validationReport.issues && validationReport.issues.length > 0 && (
        <div className="issues-section">
          <h4>Issues to Address</h4>
          {validationReport.issues.slice(0, 5).map((issue, index) => (
            <div key={index} className={`issue-item ${issue.type}`}>
              <div className="issue-header">
                <span className="issue-icon">{getIssueIcon(issue.type)}</span>
                <span className="issue-type">{issue.type.toUpperCase()}</span>
                <span className="issue-section">({issue.section})</span>
              </div>
              <div className="issue-content">
                <p className="issue-message">{issue.message}</p>
                <p className="issue-suggestion">
                  <strong>Solution:</strong> {issue.suggestion}
                </p>
                {issue.example && (
                  <p className="issue-example">
                    <strong>Example:</strong> {issue.example}
                  </p>
                )}
              </div>
            </div>
          ))}
        </div>
      )}

      {validationReport.action_items && validationReport.action_items.length > 0 && (
        <div className="action-items">
          <h4>Priority Action Items</h4>
          <ol>
            {validationReport.action_items.slice(0, 5).map((action, index) => (
              <li key={index} className="action-item">{action}</li>
            ))}
          </ol>
        </div>
      )}

      <div className="validation-footer">
        <p className="pro-tip">
          💡 <strong>Pro Tip:</strong> Focus on addressing critical and major issues first for maximum impact on conversion rates.
        </p>
      </div>
    </div>
  );
};

export default QualityValidationReport;