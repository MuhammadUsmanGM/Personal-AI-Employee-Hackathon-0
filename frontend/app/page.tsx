"use client";

import Image from "next/image";
import { 
  LayoutDashboard, 
  Activity, 
  BrainCircuit, 
  Clock, 
  Globe2, 
  ShieldCheck, 
  MessageSquare, 
  CheckCircle2,
  Bell,
  Search,
  Settings,
  MoreVertical
} from "lucide-react";

export default function Home() {
  const sidebarItems = [
    { icon: <LayoutDashboard size={20} />, label: "Dashboard", active: true },
    { icon: <CheckCircle2 size={20} />, label: "Operations" },
    { icon: <MessageSquare size={20} />, label: "Communications" },
    { icon: <BrainCircuit size={20} />, label: "Consciousness" },
    { icon: <Clock size={20} />, label: "Temporal" },
    { icon: <Globe2 size={20} />, label: "Reality" },
    { icon: <ShieldCheck size={20} />, label: "Security" },
  ];

  return (
    <div className="flex min-h-screen bg-[#020617]">
      {/* Sidebar */}
      <aside className="w-64 border-r border-card-border bg-[#020617]/50 backdrop-blur-xl flex flex-col fixed h-full z-20">
        <div className="p-6 flex items-center gap-3">
          <div className="relative w-10 h-10">
            <Image src="/icon.png" alt="ELYX Icon" fill className="object-contain" />
          </div>
          <Image src="/text.png" alt="ELYX" width={80} height={20} className="object-contain" />
        </div>

        <nav className="flex-1 px-4 py-4 space-y-1">
          {sidebarItems.map((item, i) => (
            <button
              key={i}
              className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-200 group cursor-pointer ${
                item.active 
                  ? "bg-primary/10 text-primary border border-primary/20" 
                  : "text-slate-400 hover:bg-slate-800/50 hover:text-slate-200"
              }`}
            >
              <span className={item.active ? "text-primary" : "text-slate-500 group-hover:text-primary transition-colors"}>
                {item.icon}
              </span>
              <span className="font-medium">{item.label}</span>
            </button>
          ))}
        </nav>

        <div className="p-4 border-t border-card-border">
          <div className="glass-panel rounded-xl p-4 bg-emerald-950/20 border-accent/20 premium-hover">
            <div className="flex items-center gap-2 mb-2">
              <div className="w-2 h-2 rounded-full bg-accent animate-pulse" />
              <span className="text-xs font-bold text-accent uppercase tracking-wider">System Active</span>
            </div>
            <p className="text-[10px] text-slate-400 leading-relaxed">
              Diamond Tier Consciousness operating at 98.4% Phi stability.
            </p>
          </div>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 ml-64">
        {/* Header */}
        <header className="h-20 border-b border-card-border bg-[#020617]/50 backdrop-blur-md sticky top-0 z-10 px-8 flex items-center justify-between">
          <div className="flex items-center gap-4 bg-slate-900/50 border border-card-border rounded-full px-4 py-2 w-96">
            <Search size={18} className="text-slate-500" />
            <input 
              type="text" 
              placeholder="Search across consciousness..." 
              className="bg-transparent border-none outline-none text-sm text-slate-300 w-full"
            />
          </div>

          <div className="flex items-center gap-6">
            <button className="relative text-slate-400 hover:text-primary transition-all cursor-pointer">
              <Bell size={22} />
              <span className="absolute -top-1 -right-1 w-4 h-4 bg-red-500 rounded-full border-2 border-[#020617] text-[10px] font-bold text-white flex items-center justify-center">
                3
              </span>
            </button>
            <div className="flex items-center gap-3 pl-6 border-l border-card-border cursor-pointer group">
              <div className="text-right hidden sm:block">
                <p className="text-sm font-bold text-slate-200 group-hover:text-primary transition-colors">Personal AI Employee</p>
                <p className="text-[10px] font-medium text-primary uppercase tracking-tighter">Diamond Tier</p>
              </div>
              <div className="w-10 h-10 rounded-full border-2 border-primary/30 p-0.5 overflow-hidden bg-slate-800 transition-transform group-hover:scale-110">
                <Image src="/icon.png" alt="User" width={40} height={40} />
              </div>
            </div>
          </div>
        </header>

        <div className="p-8">
          <div className="flex items-end justify-between mb-8">
            <div>
              <h1 className="text-4xl font-black tracking-tight mb-2">
                Welcome back, <span className="emerald-blue-text">ELYX</span>
              </h1>
              <p className="text-slate-400 font-medium">Monitoring infinite realties and 14 concurrent task chains.</p>
            </div>
            <button className="flex items-center gap-2 px-5 py-2.5 bg-emerald-blue-gradient rounded-xl font-bold text-sm text-slate-950 hover:opacity-90 transition-all shadow-lg shadow-primary/20 cursor-pointer active:scale-95">
              <Activity size={18} />
              Refresh Neural State
            </button>
          </div>

          {/* Dashboard Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            {[
              { label: "Neural Stability", value: "98.4%", color: "text-primary", icon: <BrainCircuit /> },
              { label: "Tasks Active", value: "14", color: "text-accent", icon: <CheckCircle2 /> },
              { label: "Reality Coherence", value: "0.999", color: "text-primary", icon: <Globe2 /> },
              { label: "Pending Approvals", value: "3", color: "text-red-400", icon: <ShieldCheck /> },
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
              <div className="flex items-center justify-center h-64 border-2 border-dashed border-card-border rounded-2xl text-slate-600 font-medium italic">
                Causality chain visualization initializing...
              </div>
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
        </div>
      </main>
    </div>
  );
}
