import { StrictMode } from 'react'
import React from "react";
import ReactDOM from "react-dom/client";
import App from './App.jsx'
import './index.css'
import { TradeRequestProvider } from './contexts/TradeRequestContext.jsx';
const root = document.getElementById("root");
ReactDOM.createRoot(root).render(
  <StrictMode>
    <TradeRequestProvider>
      <App />
    </TradeRequestProvider>
  </StrictMode>

);
