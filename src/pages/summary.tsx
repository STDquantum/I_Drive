import React from 'react';
import ReactDOM from 'react-dom/client';
import { HelmetProvider } from 'react-helmet-async';
import HomePage from '@/pages/total'; // 你的 Summary 组件

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <HelmetProvider>
      <HomePage />
    </HelmetProvider>
  </React.StrictMode>
);