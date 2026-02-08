import {Home, BarChart3, FileText, LucideSettings2, LogOut, type LucideIcon} from "lucide-react";
import {useNavigate} from "react-router-dom";
import { useLogoutMutation } from "../redux/auth/authApi";
import {Link} from "react-router-dom";
import ThemeToggle from "./ThemeToggle.tsx";

const Item = ({ to, icon: Icon, label }: { to: string; icon: LucideIcon; label: string }) => {
    const isActive = location.pathname === to;

    return (
        <Link
            to={to}
            className={`flex items-center space-x-3 px-4 py-3 rounded-lg transition-colors  ${isActive ? "bg-primary text-white" : "hover:bg-primary/10 text-b"} `}
        >
            <Icon className="w-5 h-5" />
            <span>{label}</span>
        </Link>
    );
}

const SideBar = () => {
    const navigate = useNavigate();
    const [logout, { isLoading: isLoggingOut }] = useLogoutMutation();


    const handleLogout = async () => {
        try {
            await logout().unwrap();
            navigate("/signin");
        } catch (error) {
            console.error("Logout failed:", error);
            // Still navigate to signin even if logout fails
            navigate("/signin");
        }
    };


    return (
        <aside className="fixed left-0 top-0 h-full w-64 bg-card border-r border-border p-6">
            <div className="flex items-center space-x-2 mb-10">
                <div className="w-10 h-10 bg-primary rounded-lg flex items-center justify-center">
                    <span className="text-background font-bold text-xl">CV</span>
                </div>
                <span className="text-text text-xl font-bold">CVision</span>
            </div>

            <nav className="space-y-2">
                <Item icon={Home} label={"Dashboard"} to="/dashboard" />
                <Item icon={FileText} label={"Analyse"} to="/analyse" />
                <Item icon={BarChart3} label={"Analytics"} to="/analytics" />
            </nav>

            <div className="absolute bottom-6 left-6 right-6">
                <Item icon={LucideSettings2} label={"Settings"} to="/settings" />
                <ThemeToggle icon={false}/>
                <button
                    onClick={handleLogout}
                    disabled={isLoggingOut}
                    className="w-full flex items-center space-x-3 px-4 py-3 text-muted hover:bg-error/10 hover:text-error rounded-lg transition-colors disabled:opacity-50"
                >
                    <LogOut className="w-5 h-5" />
                    <span>{isLoggingOut ? "Signing out..." : "Sign Out"}</span>
                </button>
            </div>
        </aside>

    );
};

export default SideBar;