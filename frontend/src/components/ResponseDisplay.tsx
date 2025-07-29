import React, { useState } from 'react';
import { PerplexityResponse } from '../types/api';
import './ResponseDisplay.css';

interface ResponseDisplayProps {
  response: PerplexityResponse;
}

const ResponseDisplay: React.FC<ResponseDisplayProps> = ({ response }) => {
  const [showAllSources, setShowAllSources] = useState(false);

  const displayedSources = showAllSources 
    ? response.explore_more 
    : response.explore_more.slice(0, 3);

  return (
    <div className="response-display">
      <div className="summary-section">
        <div className="summary-content">
          {response.summary.split('\n').map((paragraph, index) => (
            <p key={index}>{paragraph}</p>
          ))}
        </div>
      </div>

      {response.explore_more.length > 0 && (
        <div className="explore-more-section">
          <h3 className="explore-more-title">Explore More</h3>
          <div className="sources-list">
            {displayedSources.map((source, index) => (
              <a
                key={index}
                href={source.url}
                target="_blank"
                rel="noopener noreferrer"
                className="source-link"
              >
                <div className="source-item">
                  <div className="source-title">{source.title}</div>
                  <div className="source-url">{new URL(source.url).hostname}</div>
                </div>
                <div className="source-arrow">↗</div>
              </a>
            ))}
          </div>
          
          {response.explore_more.length > 3 && (
            <button
              onClick={() => setShowAllSources(!showAllSources)}
              className="show-more-button"
            >
              {showAllSources 
                ? `Show Less` 
                : `Show ${response.explore_more.length - 3} More Sources`
              }
            </button>
          )}
        </div>
      )}
    </div>
  );
};

export default ResponseDisplay; 