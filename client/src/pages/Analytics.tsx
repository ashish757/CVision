import React from 'react';
import SideBar from "../components/SideBar.tsx";

const Analytics = () => {
    return (
        <div className="min-h-screen bg-background">
            {/* Sidebar */}
            <SideBar />

            {/*    Main Content */}
            <main className="ml-64 p-8">
                <h1 className="text-3xl font-bold text-text mb-4">Analytics</h1>
                <p className="text-muted mb-8">Here you can view detailed analytics of your CV analyses.</p>

                {/* Placeholder for analytics content */}
                <div className="bg-card/80 backdrop-blur-lg rounded-2xl p-8 border border-primary/20">
                    <h2 className="text-xl font-semibold text-text mb-4">Coming Soon!</h2>
                    <p className="text-muted">We're working hard to bring you insightful analytics. Stay tuned!</p>
                </div>
            </main>
        </div>
    );
};

export default Analytics;