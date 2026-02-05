"use client";

import { useEffect, useState } from "react";
import { 
  Globe2, 
  Orbit, 
  GitBranch, 
  Zap, 
  Anchor, 
  AlertTriangle, 
  ChevronRight, 
  History,
  Target,
  RefreshCcw,
  Plus,
  ArrowUpRight,
  Loader2
} from "lucide-react";
import DashboardLayout from "@/components/DashboardLayout";
import { fetchRealityStatus, fetchRealityScenarios } from "@/lib/api";
import { RealityStatus, RealityScenario } from "@/lib/types";

export default function RealityPage() {
  const [status, setStatus] = useState<RealityStatus | null>(null);
  const [scenarios, setScenarios] = useState<RealityScenario[]>([]);
  const [loading, setLoading] = useState(true);
  const [simulating, setSimulating] = useState(false);

  const loadData = async () => {
    try {
      setLoading(true);
      const [resStatus, resScenarios] = await Promise.all([
        fetchRealityStatus(),
        fetchRealityScenarios()
      ]);
      setStatus(resStatus);
      setScenarios(resScenarios);
    } catch (error) {
      console.error("Reality fetch error:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const runSimulation = () => {
    setSimulating(true);
    setTimeout(() => {
      setSimulating(false);
      loadData();
    }, 3000);
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'anchored': return 'text-emerald-500 border-emerald-500/20 bg-emerald-500/5';
      case 'simulating': return 'text-primary border-primary/20 bg-primary/5';
      case 'diverged': return 'text-red-500 border-red-500/20 bg-red-500/5';
      case 'stable': return 'text-accent border-accent/20 bg-accent/5';
      default: return 'text-slate-500 border-slate-500/20 bg-slate-500/5';
    }
  };

  return (
    <DashboardLayout>
      <div className="space-y-8 animate-in fade-in duration-700">
        <div className="flex items-end justify-between">
          <div>
            <h1 className="text-4xl font-black tracking-tight mb-2">Reality Management</h1>
            <p className="text-slate-400 font-medium">Control primary timelines and manage simulated causal projections.</p>
          </div>
          <div className="flex gap-3">
             <button 
               onClick={runSimulation}
               disabled={simulating}
               className="px-6 py-3 bg-emerald-blue-gradient rounded-xl font-bold text-slate-950 flex items-center gap-2 hover:scale-105 transition-all active:scale-95 disabled:opacity-50"
             >
               {simulating ? <Loader2 size={18} className="animate-spin" /> : <Orbit size={18} />}
               New Reality Prophecy
             </button>
          </div>
        </div>

        {loading ? (
          <div className="flex flex-col items-center justify-center p-40 gap-4">
            <Loader2 size={48} className="text-primary animate-spin" />
            <p className="text-slate-500 font-bold">Anchoring temporal data...</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
            
            {/* Left Column: Continuity Status */}
            <div className="lg:col-span-1 space-y-6">
               <div className="glass-panel p-8 rounded-3xl border-primary/20 relative overflow-hidden">
                  <div className="absolute top-0 right-0 p-4 opacity-5">
                     <Globe2 size={120} />
                  </div>
                  <h3 className="text-xs font-bold text-slate-500 uppercase tracking-widest mb-6 border-b border-card-border pb-4">Timeline Integrity</h3>
                  
                  <div className="space-y-8">
                     <div>
                        <p className="text-[10px] font-black text-slate-500 uppercase mb-2">Stability Index</p>
                        <div className="flex items-center gap-4">
                           <h2 className="text-4xl font-black text-primary">{(status?.stability_index || 0).toFixed(3)}</h2>
                           <div className="flex items-center text-[10px] font-bold text-emerald-500">
                              <ArrowUpRight size={14} />
                              Stable
                           </div>
                        </div>
                     </div>

                     <div>
                        <p className="text-[10px] font-black text-slate-500 uppercase mb-2">Anchoring Strength</p>
                        <div className="w-full bg-slate-900 h-2 rounded-full overflow-hidden border border-card-border mb-2">
                           <div className="bg-primary h-full" style={{ width: `${(status?.anchoring_strength || 0) * 100}%` }} />
                        </div>
                        <p className="text-[10px] font-bold text-slate-400">{(status?.anchoring_strength || 0 * 100).toFixed(1)}% Bound</p>
                     </div>

                     <div className="p-4 rounded-2xl bg-slate-900/50 border border-card-border">
                        <div className="flex items-center gap-2 text-emerald-500 mb-2">
                           <Zap size={14} />
                           <span className="text-[10px] font-black uppercase">Primary Core</span>
                        </div>
                        <p className="text-xs text-slate-400">The primary reality is currently synchronized with all business vectors.</p>
                     </div>
                  </div>
               </div>

               <div className="glass-panel p-6 rounded-2xl border-accent/10">
                  <h4 className="text-[10px] font-black text-slate-500 uppercase mb-4">Boundary Metrics</h4>
                  <div className="space-y-4">
                     {[
                       { label: "Temporal Leak", value: "0.002%", status: "safe" },
                       { label: "Causal Loop", value: "Detected (2)", status: "warn" },
                       { label: "Entropic Decay", value: "Minimal", status: "safe" },
                     ].map((m, i) => (
                       <div key={i} className="flex items-center justify-between">
                         <span className="text-[10px] font-bold text-slate-400">{m.label}</span>
                         <span className={`text-[10px] font-black uppercase ${m.status === 'warn' ? 'text-amber-500' : 'text-emerald-500'}`}>
                           {m.value}
                         </span>
                       </div>
                     ))}
                  </div>
               </div>
            </div>

            {/* Main Center: Scenarios */}
            <div className="lg:col-span-3 space-y-6">
               <div className="flex items-center justify-between mb-4 px-2">
                  <h3 className="text-lg font-bold flex items-center gap-2">
                     <GitBranch size={20} className="text-primary" />
                     Forecasted Timelines
                  </h3>
                  <div className="flex gap-2">
                    <button className="p-2 bg-slate-900 border border-card-border rounded-lg text-slate-500 hover:text-white transition-colors">
                       <RefreshCcw size={16} />
                    </button>
                    <button className="p-2 bg-slate-900 border border-card-border rounded-lg text-slate-500 hover:text-white transition-colors">
                       <Plus size={16} />
                    </button>
                  </div>
               </div>

               <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  {scenarios.map((s) => (
                    <div key={s.id} className="glass-panel p-6 rounded-3xl hover:border-primary/40 transition-all cursor-pointer group relative overflow-hidden">
                       <div className="absolute top-0 right-0 w-32 h-32 bg-primary/5 blur-3xl pointer-events-none" />
                       
                       <div className="flex items-start justify-between mb-4">
                          <span className={`px-3 py-1 rounded-full text-[10px] font-black uppercase border ${getStatusColor(s.status)}`}>
                             {s.status}
                          </span>
                          <p className="text-[10px] font-bold text-slate-600 uppercase">
                             ID: {s.id}
                          </p>
                       </div>

                       <h4 className="text-lg font-bold text-slate-200 mb-2 group-hover:text-primary transition-colors">{s.name}</h4>
                       <p className="text-xs text-slate-500 leading-relaxed mb-6 line-clamp-2">{s.description}</p>

                       <div className="grid grid-cols-2 gap-4 mb-6">
                          <div className="p-3 rounded-2xl bg-slate-900/50 border border-card-border">
                             <p className="text-[9px] font-black text-slate-500 uppercase mb-1">Impact Score</p>
                             <p className="text-sm font-black text-slate-200">{s.impact_score}/100</p>
                          </div>
                          <div className="p-3 rounded-2xl bg-slate-900/50 border border-card-border">
                             <p className="text-[9px] font-black text-slate-500 uppercase mb-1">Probability</p>
                             <p className="text-sm font-black text-slate-200">{(s.probability * 100).toFixed(0)}%</p>
                          </div>
                       </div>

                       <div className="flex items-center justify-between border-t border-card-border pt-4">
                          <div className="flex items-center gap-2">
                             <Target size={14} className="text-primary" />
                             <span className="text-[10px] font-bold text-slate-400 capitalize">{s.type} Path</span>
                          </div>
                          <button className="flex items-center gap-1 text-[10px] font-black text-primary uppercase hover:underline">
                             Propagate Scenario
                             <ChevronRight size={14} />
                          </button>
                       </div>
                    </div>
                  ))}
               </div>

               {/* Causal Graph Placeholder */}
               <div className="glass-panel rounded-3xl p-8 relative overflow-hidden min-h-[300px]">
                  <div className="flex items-center justify-between mb-8">
                     <h3 className="text-lg font-bold flex items-center gap-2">
                        <GitBranch size={20} className="text-accent" />
                        Causal Link Projections
                     </h3>
                     <span className="text-[10px] font-black text-slate-500 uppercase">4,288 Active Connections</span>
                  </div>

                  <div className="flex flex-col items-center justify-center h-48 opacity-30 select-none">
                     <Orbit size={64} className="text-accent mb-4 animate-spin-slow" />
                     <p className="text-xs font-bold text-slate-500">Visualizing causal impact on primary timeline...</p>
                  </div>

                  <div className="absolute bottom-0 left-0 w-full p-8 bg-gradient-to-t from-[#020617] to-transparent">
                     <div className="flex items-center justify-between p-4 rounded-2xl bg-slate-900/80 border border-card-border backdrop-blur-md">
                        <div className="flex items-center gap-4">
                           <div className="w-10 h-10 rounded-full bg-accent/20 flex items-center justify-center text-accent">
                              <AlertTriangle size={20} />
                           </div>
                           <div>
                              <p className="text-xs font-bold text-slate-200">Critical Anomaly Detected</p>
                              <p className="text-[10px] text-slate-500">Divergence detected in "Competitor Hostile Takeover" scenario.</p>
                           </div>
                        </div>
                        <button className="px-4 py-2 bg-accent text-white rounded-xl text-[10px] font-black uppercase hover:bg-white hover:text-slate-950 transition-all">
                           Anchor Branch
                        </button>
                     </div>
                  </div>
               </div>

            </div>
          </div>
        )}
      </div>
    </DashboardLayout>
  );
}
