import React from 'react';

const Card = ({ title, children, className = '', actions }) => {
    return (
        <div className={`glass-card rounded-xl p-6 flex flex-col ${className}`}>
            {(title || actions) && (
                <div className="flex items-center justify-between mb-6 pb-4 border-b border-[var(--border-color)]">
                    {title && (
                        <h3 className="text-lg font-semibold text-[var(--text-primary)] tracking-tight">
                            {title}
                        </h3>
                    )}
                    {actions && <div className="flex gap-2">{actions}</div>}
                </div>
            )}
            <div className="flex-1 relative">
                {children}
            </div>
        </div>
    );
};

export default Card;
