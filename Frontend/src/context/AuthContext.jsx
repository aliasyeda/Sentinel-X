import React, { createContext, useContext, useState, useEffect } from 'react';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);

    // Mock Users Database
    const USERS = [
        { username: 'Syed', role: 'Administrator', designation: 'Lead Architect' },
        { username: 'Alia', role: 'Security Analyst', designation: 'Threat Hunter' },
        { username: 'Samiya', role: 'SOC Operator', designation: 'L1 Responder' }
    ];

    useEffect(() => {
        // Check local storage for existing session
        const storedUser = localStorage.getItem('sentinel_user');
        if (storedUser) {
            setUser(JSON.parse(storedUser));
        }
        setLoading(false);
    }, []);

    const login = (username, password) => {
        return new Promise((resolve, reject) => {
            // Simulate network delay
            setTimeout(() => {
                const foundUser = USERS.find(u => u.username.toLowerCase() === username.toLowerCase());

                if (foundUser) {
                    setUser(foundUser);
                    localStorage.setItem('sentinel_user', JSON.stringify(foundUser));
                    resolve(foundUser);
                } else {
                    reject('Invalid credentials. Access Denied.');
                }
            }, 800);
        });
    };

    const logout = () => {
        setUser(null);
        localStorage.removeItem('sentinel_user');
    };

    return (
        <AuthContext.Provider value={{ user, login, logout, loading }}>
            {!loading && children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => useContext(AuthContext);
