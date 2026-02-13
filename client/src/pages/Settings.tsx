import SideBar from "../components/SideBar.tsx";

const Settings = () => {
    return (
        <div className="min-h-screen bg-background">
            {/* Sidebar */}
            <SideBar />

            {/*    Main Content */}
            <main className="ml-64 p-8">
                <h1 className="text-3xl font-bold text-text mb-4">Settings</h1>

                {/* Placeholder for Settings content */}
                <div className="bg-card/80 backdrop-blur-lg rounded-2xl p-8 border border-primary/20">
                    <h2 className="text-xl font-semibold text-text mb-4">Coming Soon!</h2>
                </div>
            </main>
        </div>
    );
};

export default Settings;