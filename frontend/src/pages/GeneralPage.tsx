import React from 'react';
import ChatInterface from '../components/ChatInterface';

const GeneralPage: React.FC = () => {
  return (
    <ChatInterface
      agentType="general"
      welcomeMessage="Hi, welcome to Brennan's Query Bot"
      initialResponse={null}
    />
  );
};

export default GeneralPage; 