import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { AgentType } from '../types/api';
import './Sidebar.css';

interface SidebarProps {
  className?: string;
}

const Sidebar: React.FC<SidebarProps> = ({ className }) => {
  const location = useLocation();

  const getAgentType = (pathname: string): AgentType => {
    if (pathname.startsWith('/sports')) return 'sports';
    if (pathname.startsWith('/finance')) return 'finance';
    return 'general';
  };

  const currentAgent = getAgentType(location.pathname);

  const navItems = [
    { path: '/', label: 'General', type: 'general' as AgentType },
    { path: '/sports', label: 'Sports', type: 'sports' as AgentType },
    { path: '/finance', label: 'Finance', type: 'finance' as AgentType },
  ];

  return (
    <div className={`sidebar ${className || ''}`}>
      <div className="sidebar-header">
        <h2>Query Bot</h2>
      </div>
      <nav className="sidebar-nav">
        {navItems.map((item) => (
          <Link
            key={item.type}
            to={item.path}
            className={`nav-item ${currentAgent === item.type ? 'active' : ''}`}
          >
            <span className="nav-icon">
              {item.type === 'general' && '🤖'}
              {item.type === 'sports' && '⚽'}
              {item.type === 'finance' && '📈'}
            </span>
            {item.label}
          </Link>
        ))}
      </nav>
    </div>
  );
};

export default Sidebar; 