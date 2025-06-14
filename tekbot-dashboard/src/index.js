import React from 'react';
import { createRoot } from 'react-dom/client';
import App from './App';        // agora App.js existe
import './index.css';          // agora index.css existe

const container = document.getElementById('root');
const root = createRoot(container);
root.render(<App />);
