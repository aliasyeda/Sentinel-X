import React from 'react';

const CyberTable = ({ headers, data, renderRow }) => {
    return (
        <div className="w-full overflow-x-auto">
            <table className="w-full text-left border-collapse">
                <thead>
                    <tr className="border-b border-[var(--border-color)]">
                        {headers.map((header, index) => (
                            <th
                                key={index}
                                className={`py-4 px-6 text-xs uppercase tracking-wider font-semibold text-[var(--text-secondary)] ${index === headers.length - 1 ? 'text-right' : ''
                                    }`}
                            >
                                {header}
                            </th>
                        ))}
                    </tr>
                </thead>
                <tbody className="divide-y divide-[var(--border-color)]">
                    {data.map((item, index) => (
                        <tr
                            key={item.id || index}
                            className="group hover:bg-[rgba(255,255,255,0.02)] transition-colors duration-150"
                        >
                            {renderRow(item)}
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default CyberTable;
