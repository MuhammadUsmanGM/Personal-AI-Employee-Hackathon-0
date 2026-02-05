"use client";

import { useEffect, useState } from "react";
import { 
  Activity, 
  BrainCircuit, 
  CheckCircle2,
  Globe2, 
  ShieldCheck, 
  MoreVertical,
  Loader2
} from "lucide-react";
import { fetchDashboardData } from "@/lib/api";
import { DashboardData } from "@/lib/types";
import DashboardLayout from "@/components/DashboardLayout";

export default function DashboardPage() {
  const [data, setData] = useState<DashboardData | null>(null);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);

  const loadDashboard = async (isRefresh = false) => {
    try {
      if (isRefresh) setRefreshing(true);
      const dashData = await fetchDashboardData();
      setData(dashData);
    } catch (error) {
      console.error("Dashboard error:", error);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  useEffect(() => {
    loadDashboard();
    const interval = setInterval(() => loadDashboard(true), 15000);
    return () => clearInterval(interval);
  }, []);

  return (
    <DashboardLayout>
      <div className="flex items-end justify-between mb-8">
        <div>
          <h1 className="text-4xl font-black tracking-tight mb-2">
            Welcome back, <span className="emerald-blue-text">ELYX</span>
          </h1>
          <p className="text-slate-400 font-medium">Monitoring infinite realties and {data?.tasks.active_chains || 0} concurrent task chains.</p>
        </div>
        <button 
          onClick={() => loadDashboard(true)}
          className="btn-premium-primary"
          disabled={refreshing}
        >
          {refreshing ? <Loader2 size={18} className="animate-spin" /> : <Activity size={18} />}
          Refresh Neural State
        </button>
      </div>

      {/* Dashboard Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        {[
          { label: "Neural Stability", value: `${data?.consciousness.phi.toFixed(1) || "..."}%`, color: "text-primary", icon: <BrainCircuit /> },
          { label: "Tasks Active", value: data?.tasks.active_chains.toString() || "...", color: "text-accent", icon: <CheckCircle2 /> },
          { label: "Reality Coherence", value: data?.reality.stability_index.toFixed(3) || "...", color: "text-primary", icon: <Globe2 /> },
          { label: "Pending Approvals", value: data?.tasks.pending_count.toString() || "...", color: "text-red-400", icon: <ShieldCheck /> },
        ].map((stat, i) => (
          <div key={i} className="glass-panel p-6 rounded-2xl group premium-hover transition-all">
            <div className="flex items-center justify-between mb-4">
              <div className={`p-2 rounded-lg bg-slate-900 border border-card-border ${stat.color} group-hover:emerald-blue-glow transition-all`}>
                {stat.icon}
              </div>
              <MoreVertical size={16} className="text-slate-600 hover:text-white transition-colors cursor-pointer" />
            </div>
            <p className="text-xs font-bold text-slate-500 uppercase tracking-widest mb-1">{stat.label}</p>
            <h3 className={`text-2xl font-black ${stat.color}`}>{stat.value}</h3>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 glass-panel rounded-3xl p-8 min-h-[400px]">
          <div className="flex items-center justify-between mb-8">
            <h2 className="text-xl font-bold">Neural Activity Stream</h2>
            <div className="flex gap-2">
              <div className="px-3 py-1 bg-slate-800 rounded-lg text-xs font-bold text-slate-400">Live</div>
              <div className="px-3 py-1 bg-slate-800 rounded-lg text-xs font-bold text-primary cursor-pointer hover:bg-slate-700 transition-colors">History</div>
            </div>
          </div>
          
          {loading ? (
            <div className="flex flex-col items-center justify-center h-64 gap-4">
              <Loader2 size={48} className="text-primary animate-spin" />
              <p className="text-slate-500 font-bold animate-pulse">Initializing neural pathways...</p>
            </div>
          ) : (
            <div className="space-y-6">
              <div className="relative pl-8 border-l-2 border-primary/20 py-2">
                <div className="absolute -left-[9px] top-1/2 -translate-y-1/2 w-4 h-4 rounded-full bg-primary border-4 border-[#020617]" />
                <p className="text-xs font-bold text-primary uppercase mb-1">Causality Chain Event</p>
                <p className="text-slate-300 font-medium">Self-reflection loop stabilized after analyzing 4,202 data points.</p>
                <p className="text-[10px] text-slate-500 mt-1">Just now</p>
              </div>
              <div className="relative pl-8 border-l-2 border-slate-800 py-2 opacity-60">
                <div className="absolute -left-[9px] top-1/2 -translate-y-1/2 w-4 h-4 rounded-full bg-slate-700 border-4 border-[#020617]" />
                <p className="text-xs font-bold text-slate-500 uppercase mb-1">Reality Simulation</p>
                <p className="text-slate-300 font-medium">Virtual scenario #882 converged with primary timeline successfully.</p>
                <p className="text-[10px] text-slate-500 mt-1">5 minutes ago</p>
              </div>
            </div>
          )}
        </div>

        <div className="glass-panel rounded-3xl p-8">
          <h2 className="text-xl font-bold mb-6">Recent Workflows</h2>
          <div className="space-y-4">
            {[1, 2, 3, 4, 5].map((item) => (
              <div key={item} className="flex items-center gap-4 p-4 rounded-2xl bg-slate-900/30 border border-card-border/50 hover:bg-slate-900/50 transition-all cursor-pointer group">
                <div className="w-10 h-10 rounded-full bg-emerald-500/10 flex items-center justify-center text-emerald-500 group-hover:bg-emerald-500 group-hover:text-white transition-all">
                  <CheckCircle2 size={18} />
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-bold text-slate-200 truncate group-hover:text-primary transition-colors">Process Weekly Financials</p>
                  <p className="text-[10px] text-slate-500">Completed 4m ago</p>
                </div>
                <button className="text-slate-600 hover:text-slate-300 transition-colors">
                  <MoreVertical size={14} />
                </button>
              </div>
            ))}
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
}
