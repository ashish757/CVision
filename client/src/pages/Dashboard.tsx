import { FileText, Upload, TrendingUp, Check, LucideScanEye} from "lucide-react";
import StatCard from "../components/StatCard.tsx";
import {useSelector} from "react-redux";
import type {RootState} from "../redux/store.ts";
import SideBar from "../components/SideBar.tsx";


const Dashboard = () => {

  const user = useSelector((state: RootState) => state.auth.user);


  return (
    <div className="min-h-screen bg-background">
      {/* Sidebar */}
      <SideBar />

      {/* Main Content */}
      <main className="ml-64 p-8">
        <h1 className="text-3xl font-bold text-text mb-4">Dashboard</h1>

        {/* Header */}
        <div className="flex items-center justify-between mb-8 bg-linear-to-r from-primary to-accent rounded-lg p-5">
          <div>
            <h1 className="text-3xl font-bold text-white">Good Morning,  {user?.name || "User"}!</h1>
            <p className="text-gray-100 mt-1">
              Welcome back,  What would you like to do today?
            </p>
          </div>

        </div>


        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <StatCard title={"Total Analysis"} num={"4"} Icon={Check} />
          <StatCard title={"CVs  Analysed"} num={"56"} Icon={FileText} />
          <StatCard title="Improvement" num="+12%" Icon={TrendingUp} />
        </div>


        {/* Action buttons*/}
        <h1 className="text-2xl text-text mb-4">Quick Actions</h1>
        <div className="flex items-center space-x-4 mb-8">
          <button className="bg-primary hover:bg-primary/90 text-white px-6 py-3 rounded-lg font-medium transition-colors flex items-center space-x-2">
            <Upload className="w-5 h-5" />
            <span>Start New Analysis</span>
          </button>

          <button className="bg-primary hover:bg-secondary/90 text-white px-6 py-3 rounded-lg font-medium transition-colors flex items-center space-x-2">
            <LucideScanEye className="w-5 h-5" />
            <span>View Last Analysis</span>
          </button>
        </div>

      </main>

    </div>
  );

};

export default Dashboard;

