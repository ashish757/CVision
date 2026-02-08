import {Home, BarChart3, FileText, LucideSettings2, LogOut} from "lucide-react";
import {useNavigate, useParams} from "react-router-dom";
import { useLogoutMutation } from "../redux/auth/authApi";
import {Link} from "react-router-dom";

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

    const isActive = (path: string) => location.pathname === path;



    return (
        <aside className="fixed left-0 top-0 h-full w-64 bg-card border-r border-border p-6">
            <div className="flex items-center space-x-2 mb-10">
                <div className="w-10 h-10 bg-primary rounded-lg flex items-center justify-center">
                    <span className="text-background font-bold text-xl">CV</span>
                </div>
                <span className="text-text text-xl font-bold">CVision</span>
            </div>

            <nav className="space-y-2">
                <Link
                    to="/dashboard"
                    className={"flex items-center space-x-3 px-4 py-3 rounded-lg transition-colors " + (isActive("/dashboard") ? "bg-primary/30 text-primary" : "hover:bg-muted/10 hover:text-text") }
                >
                    <Home className="w-5 h-5" />
                    <span>Dashboard</span>
                </Link>
                <Link
                    to="/analyse"
                    className={"flex items-center space-x-3 px-4 py-3 text-muted rounded-lg transition-colors " + (isActive("/analyse") ? "bg-primary/30 text-primary" : "hover:bg-muted/10 hover:text-text") }
                >
                    <FileText className="w-5 h-5" />
                    <span>Analyse</span>
                </Link>
                <Link
                    to="/analytics"
                    className={"flex items-center space-x-3 px-4 py-3 text-muted rounded-lg transition-colors " + (isActive("/analytics") ? "bg-primary/30 text-primary" : "hover:bg-muted/10 hover:text-text") }
                >
                    <BarChart3 className="w-5 h-5" />
                    <span>Analytics</span>
                </Link>

            </nav>

            <div className="absolute bottom-6 left-6 right-6">
                <Link
                    to="/settings"
                    className={"flex items-center space-x-3 px-4 py-3 text-muted  rounded-lg transition-colors " + (isActive("/settings") ? "bg-primary/30 text-primary" : "hover:bg-muted/10 hover:text-text")}
                >
                    <LucideSettings2 className="w-5 h-5" />
                    <span>Settings</span>
                </Link>
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