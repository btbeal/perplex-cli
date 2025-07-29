import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import GeneralPage from './pages/GeneralPage';
import SportsPage from './pages/SportsPage';
import FinancePage from './pages/FinancePage';
import './App.css';

function App() {
  return (
    <Router>
      <div className="App">
        <Layout>
          <Routes>
            <Route path="/" element={<GeneralPage />} />
            <Route path="/sports" element={<SportsPage />} />
            <Route path="/finance" element={<FinancePage />} />
          </Routes>
        </Layout>
      </div>
    </Router>
  );
}

export default App;
