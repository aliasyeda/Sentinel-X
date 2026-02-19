import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate, Outlet } from 'react-router-dom';
import Layout from './components/Layout';
import Overview from './pages/Overview';
import Incidents from './pages/Incidents';
import Decisions from './pages/Decisions';
import Actions from './pages/Actions';
import Governance from './pages/Governance';
import Login from './pages/Login';
import { useAuth } from './context/AuthContext';

// Protected Route Wrapper
const ProtectedRoute = () => {
    const { user, loading } = useAuth();

    if (loading) return <div className="min-h-screen bg-[#050507] flex items-center justify-center text-[var(--neon-blue)]">Initializing Sentinel Core...</div>;

    return user ? <Outlet /> : <Navigate to="/login" replace />;
};

function App() {
    return (
        <Router>
            <Routes>
                <Route path="/login" element={<Login />} />

                <Route element={<ProtectedRoute />}>
                    <Route path="/" element={<Layout />}>
                        <Route index element={<Navigate to="/overview" replace />} />
                        <Route path="overview" element={<Overview />} />
                        <Route path="incidents" element={<Incidents />} />
                        <Route path="decisions" element={<Decisions />} />
                        <Route path="actions" element={<Actions />} />
                        <Route path="governance" element={<Governance />} />
                    </Route>
                </Route>
            </Routes>
        </Router>
    );
}

export default App;
