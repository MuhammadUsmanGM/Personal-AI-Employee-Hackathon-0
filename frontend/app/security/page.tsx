"use client";

import { useEffect, useState } from "react";
import { 
  ShieldCheck, 
  Lock, 
  Key, 
  Eye, 
  AlertOctagon, 
  ShieldAlert, 
  Binary, 
  Fingerprint, 
  Server,
  Zap,
  CheckCircle2,
  ChevronRight,
  MoreVertical,
  Loader2
} from "lucide-react";
import DashboardLayout from "@/components/DashboardLayout";

export default function SecurityPage() {
  const [loading, setLoading] = useState(true);
  const [scanning, setScanning] = useState(false);

  useEffect(() => {
    setTimeout(() => setLoading(false), 1000);
  }, []);

  const runScan = () => {
    setScanning(true);
    setTimeout(() => setScanning(false), 2000);
  };

  return (
    <DashboardLayout>
      <div className="space-y-8 animate-in fade-in duration-700">
        <div className="flex items-end justify-between">
          <div>
            <h1 className="text-4xl font-black tracking-tight mb-2">Security Perimeter</h1>
            <p className="text-slate-400 font-medium">End-to-end causal encryption and zero-trust neural access control.</p>
          </div>
          <button 
            onClick={runScan}
            disabled={scanning}
            className="px-6 py-3 bg-red-500/10 border border-red-500/20 rounded-xl font-bold text-red-500 flex items-center gap-2 hover:bg-red-500/20 transition-all active:scale-95 disabled:opacity-50"
          >
            {scanning ? <Loader2 size={18} className="animate-spin" /> : <Eye size={18} />}
            Scan for Reality Leaks
          </button>
        </div>

        {loading ? (
          <div className="flex flex-col items-center justify-center p-40 gap-4">
            <Loader2 size={48} className="text-primary animate-spin" />
            <p className="text-slate-500 font-bold">Initializing encryption layers...</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            
            {/* Status Panel */}
            <div className="lg:col-span-2 space-y-8">
               <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  {[
                    { label: "Encryption Depth", value: "8192-bit", icon: <Lock className="text-primary" />, status: "Optimal" },
                    { label: "Intrusion Attempts", value: "0", icon: <ShieldAlert className="text-emerald-500" />, status: "24h clean" },
                  ].map((stat, i) => (
                    <div key={i} className="glass-panel p-8 rounded-3xl group premium-hover">
                       <div className="flex items-center justify-between mb-4">
                          <div className="p-3 rounded-xl bg-slate-900 border border-card-border group-hover:emerald-blue-glow transition-all">
                             {stat.icon}
                          </div>
                          <span className="text-[10px] font-black text-emerald-500 uppercase tracking-widest">{stat.status}</span>
                       </div>
                       <p className="text-xs font-bold text-slate-500 uppercase tracking-widest mb-1">{stat.label}</p>
                       <h3 className="text-3xl font-black text-slate-200">{stat.value}</h3>
                    </div>
                  ))}
               </div>

               <div className="glass-panel p-8 rounded-3xl">
                  <h3 className="text-xl font-bold mb-8 flex items-center gap-2">
                    <Binary size={20} className="text-primary" />
                    Encrypted Causal Chains
                  </h3>
                  
                  <div className="space-y-4">
                     {[1, 2, 3, 4].map((i) => (
                       <div key={i} className="flex items-center gap-6 p-4 rounded-2xl bg-slate-900/30 border border-card-border/50 hover:bg-slate-900/50 transition-all group">
                          <div className="w-12 h-12 rounded-xl bg-slate-900 border border-card-border flex items-center justify-center text-slate-600 font-mono text-xs">
                             #{1000 + i}
                          </div>
                          <div className="flex-1 min-w-0">
                             <div className="flex items-center gap-2 mb-1">
                                <h4 className="text-sm font-bold text-slate-200 truncate">Decision Chain {i}x-Temporal</h4>
                                <CheckCircle2 size={12} className="text-emerald-500" />
                             </div>
                             <p className="text-[10px] font-mono text-slate-600 truncate">SHA3-512: 8f92b...{i}e4a</p>
                          </div>
                          <div className="text-right">
                             <p className="text-[10px] font-black text-slate-500 uppercase">Validated</p>
                             <p className="text-[10px] text-slate-600">2m ago</p>
                          </div>
                       </div>
                     ))}
                  </div>

                  <button className="w-full mt-8 py-3 bg-slate-900 border border-card-border rounded-xl text-xs font-bold text-slate-500 hover:text-primary transition-all flex items-center justify-center gap-2">
                     Audit All Historical Chains
                     <ChevronRight size={14} />
                  </button>
               </div>
            </div>

            {/* Right Side: Access Controls */}
            <div className="space-y-8">
               <div className="glass-panel p-8 rounded-3xl">
                  <h3 className="text-lg font-bold mb-6 flex items-center gap-2">
                    <Fingerprint size={18} className="text-primary" />
                    Access Auth
                  </h3>
                  <div className="space-y-4">
                     <div className="p-4 rounded-2xl bg-primary/5 border border-primary/20">
                        <div className="flex items-center justify-between mb-2">
                           <span className="text-xs font-bold text-slate-200">Owner Terminal</span>
                           <span className="px-2 py-0.5 rounded text-[8px] font-black bg-primary text-slate-950 uppercase tracking-tighter">Active</span>
                        </div>
                        <p className="text-[10px] text-slate-500">Biometric and temporal signature verified.</p>
                     </div>
                     <div className="p-4 rounded-2xl bg-slate-900 border border-card-border opacity-50">
                        <div className="flex items-center justify-between mb-2">
                           <span className="text-xs font-bold text-slate-400">Guest Delegate</span>
                           <span className="px-2 py-0.5 rounded text-[8px] font-black bg-slate-800 text-slate-500 uppercase tracking-tighter">Disabled</span>
                        </div>
                        <p className="text-[10px] text-slate-600">Cross-timeline delegation requires approval.</p>
                     </div>
                  </div>
               </div>

               <div className="glass-panel p-8 rounded-3xl border-red-500/20">
                  <h3 className="text-lg font-bold mb-6 flex items-center gap-2">
                    <AlertOctagon size={18} className="text-red-500" />
                    System Redline
                  </h3>
                  <div className="space-y-4">
                     <button className="w-full py-4 bg-red-500 text-white rounded-2xl font-black text-xs uppercase tracking-widest hover:bg-white hover:text-red-500 transition-all shadow-lg shadow-red-500/20 active:scale-95">
                        Initiate Neural Purge
                     </button>
                     <p className="text-[9px] text-slate-600 text-center px-4">
                        Warning: Purging the neural core will result in absolute memory loss across all timelines.
                     </p>
                  </div>
               </div>

               <div className="glass-panel p-8 rounded-3xl">
                  <div className="flex items-center gap-3 mb-6">
                     <div className="p-2 rounded-lg bg-slate-900 text-primary">
                        <Server size={18} />
                     </div>
                     <h3 className="text-lg font-bold">Node Integrity</h3>
                  </div>
                  <div className="space-y-2">
                     <div className="flex justify-between text-[10px] font-bold mb-1">
                        <span className="text-slate-500">Node α (Primary)</span>
                        <span className="text-emerald-500">100%</span>
                     </div>
                     <div className="w-full bg-slate-900 h-1 rounded-full overflow-hidden">
                        <div className="bg-emerald-500 h-full w-full" />
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
