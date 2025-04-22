import { StrictMode } from 'react'
import React from "react";
import ReactDOM from "react-dom/client";
import App from './App.jsx'
import './index.css'

const root = document.getElementById("root");
ReactDOM.createRoot(root).render(
  <StrictMode>
      <App />
  </StrictMode>

);
