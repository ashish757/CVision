import type { LucideIcon } from "lucide-react";


interface props {
    title: string;
    num: string | number;
    Icon: LucideIcon;
}

const StatCard = ({ title, num, Icon }: props) => (
    <div className="bg-card rounded-xl p-6 border border-accent/50">
        <div className="flex items-center justify-between mb-4">
            <div className="w-12 h-12 bg-primary/20 rounded-lg flex items-center justify-center">
                <Icon className="w-6 h-6 text-primary" />
            </div>
        </div>
        <h3 className="text-3xl font-bold text-text">{num}</h3>
        <p className="text-muted text-sm">{title}</p>
    </div>
);

export default StatCard;