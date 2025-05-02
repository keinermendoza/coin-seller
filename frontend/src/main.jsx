import { StrictMode } from 'react'
import React from "react";
import ReactDOM from "react-dom/client";
import App from './App.jsx'
import './index.css'
import { TradeRequestProvider } from '@/contexts/TradeRequestContext.jsx';
import { ChangesProvider } from "@/contexts/ChangeContext"

const root = document.getElementById("root");
ReactDOM.createRoot(root).render(
  <StrictMode>
    <TradeRequestProvider>
      <ChangesProvider>
        <App />
      </ChangesProvider>
    </TradeRequestProvider>
  </StrictMode>

);
