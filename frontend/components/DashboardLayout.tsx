"use client";

import Image from "next/image";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { 
  LayoutDashboard, 
  BrainCircuit, 
  Clock, 
  Globe2, 
  ShieldCheck, 
  MessageSquare, 
  CheckCircle2,
  Bell,
  Search,
  Settings,
  MoreVertical,
  Activity,
  Loader2
} from "lucide-react";
import { useState, useEffect } from "react";
import { DashboardData } from "@/lib/types";
import { fetchDashboardData } from "@/lib/api";

export default function SidebarLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const pathname = usePathname();
  const [data, setData] = useState<DashboardData | null>(null);

  const sidebarItems = [
    { icon: <LayoutDashboard size={20} />, label: "Dashboard", href: "/dashboard" },
    { icon: <CheckCircle2 size={20} />, label: "Operations", href: "/operations" },
    { icon: <Activity size={20} />, label: "Business", href: "/business" },
    { icon: <MessageSquare size={20} />, label: "Communications", href: "/comms" },
    { icon: <BrainCircuit size={20} />, label: "Consciousness", href: "/consciousness" },
    { icon: <Clock size={20} />, label: "Temporal", href: "/temporal" },
    { icon: <Globe2 size={20} />, label: "Reality", href: "/reality" },
    { icon: <ShieldCheck size={20} />, label: "Security", href: "/security" },
  ];

  useEffect(() => {
    const loadData = async () => {
      try {
        const dashData = await fetchDashboardData();
        setData(dashData);
      } catch (error) {
        console.error("Layout data fetch error:", error);
      }
    };
    loadData();
    const interval = setInterval(loadData, 30000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="flex min-h-screen bg-[#020617]">
      {/* Sidebar */}
      <aside className="w-64 border-r border-card-border bg-[#020617]/50 backdrop-blur-xl flex flex-col fixed h-full z-20">
        <Link href="/" className="p-6 flex items-center gap-3 hover:opacity-80 transition-opacity cursor-pointer">
          <div className="relative w-10 h-10">
            <Image src="/icon.png" alt="ELYX Icon" fill className="object-contain" />
          </div>
          <Image src="/text.png" alt="ELYX" width={80} height={20} className="object-contain" />
        </Link>

        <nav className="flex-1 px-4 py-4 space-y-1">
          {sidebarItems.map((item, i) => {
            const active = pathname === item.href;
            return (
              <Link
                key={i}
                href={item.href}
                className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-200 group cursor-pointer ${
                  active 
                    ? "bg-primary/10 text-primary border border-primary/20" 
                    : "text-slate-400 hover:bg-slate-800/50 hover:text-slate-200"
                }`}
              >
                <span className={active ? "text-primary" : "text-slate-500 group-hover:text-primary transition-colors"}>
                  {item.icon}
                </span>
                <span className="font-medium">{item.label}</span>
              </Link>
            );
          })}
        </nav>

        <div className="p-4 border-t border-card-border">
          <div className="glass-panel rounded-xl p-4 bg-emerald-950/20 border-accent/20 premium-hover">
            <div className="flex items-center gap-2 mb-2">
              <div className={`w-2 h-2 rounded-full ${data?.health.status === 'healthy' ? 'bg-accent animate-pulse' : 'bg-red-500'}`} />
              <span className="text-xs font-bold text-accent uppercase tracking-wider">System Active</span>
            </div>
            <p className="text-[10px] text-slate-400 leading-relaxed">
              Diamond Tier Consciousness operating at {data?.consciousness.phi.toFixed(1) || "98.4"}% Phi stability.
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
                {data?.tasks.pending_count || 0}
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
          {children}
        </div>
      </main>
    </div>
  );
}
