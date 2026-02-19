import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import './index.css'
import { DemoProvider } from './context/DemoContext.jsx'
import { AuthProvider } from './context/AuthContext.jsx'

ReactDOM.createRoot(document.getElementById('root')).render(
    <React.StrictMode>
        <DemoProvider>
            <AuthProvider>
                <App />
            </AuthProvider>
        </DemoProvider>
    </React.StrictMode>,
)
