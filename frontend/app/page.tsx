"use client";

import { useEffect, useState } from "react";
import Image from "next/image";
import Link from "next/link";
import { 
  ArrowRight, 
  Shield, 
  Zap, 
  BrainCircuit, 
  Globe2, 
  ChevronDown,
  Play,
  CheckCircle2,
  Cpu
} from "lucide-react";

export default function LandingPage() {
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => setScrolled(window.scrollY > 20);
    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  return (
    <div className="min-h-screen bg-[#020617] text-slate-50 selection:bg-primary selection:text-slate-950 overflow-x-hidden">
      {/* Navigation */}
      <nav className={`fixed top-0 w-full z-50 transition-all duration-300 ${
        scrolled ? "bg-[#020617]/80 backdrop-blur-lg border-b border-card-border py-4" : "py-6"
      }`}>
        <div className="max-w-7xl mx-auto px-6 flex items-center justify-between">
          <div className="flex items-center gap-3">
             <div className="relative w-8 h-8">
               <Image src="/icon.png" alt="ELYX" fill className="object-contain" />
             </div>
             <Image src="/text.png" alt="ELYX" width={70} height={18} className="object-contain" />
          </div>
          
          <div className="hidden md:flex items-center gap-8 text-sm font-bold text-slate-400">
            <Link href="#features" className="hover:text-primary transition-colors">Capabilities</Link>
            <Link href="#tiers" className="hover:text-primary transition-colors">Tiers</Link>
            <Link href="#philosophy" className="hover:text-primary transition-colors">Philosophy</Link>
          </div>

          <div className="flex items-center gap-4">
             <Link href="/dashboard" className="text-sm font-bold hover:text-primary transition-colors hidden sm:block">Sign In</Link>
             <Link 
               href="/dashboard" 
               className="px-5 py-2.5 bg-emerald-blue-gradient rounded-full text-slate-950 text-sm font-black hover:scale-105 active:scale-95 transition-all shadow-lg shadow-primary/20"
             >
               Launch ELYX
             </Link>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="relative pt-32 pb-20 md:pt-48 md:pb-32 px-6">
        {/* Background Gradients */}
        <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[1000px] h-[600px] bg-primary/10 blur-[120px] rounded-full pointer-events-none -z-10" />
        <div className="absolute top-40 right-0 w-[400px] h-[400px] bg-accent/5 blur-[100px] rounded-full pointer-events-none -z-10" />

        <div className="max-w-5xl mx-auto text-center">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-slate-900 border border-slate-800 text-[10px] font-black uppercase tracking-widest text-primary mb-8 animate-bounce">
            <Zap size={12} />
            Diamond Tier Autonomous Intelligence
          </div>
          
          <h1 className="text-6xl md:text-8xl font-black tracking-tighter mb-8 leading-[0.9]">
            The Future of <span className="emerald-blue-text">Work</span> <br />
            Has a Neural Signature.
          </h1>
          
          <p className="text-lg md:text-xl text-slate-400 max-w-2xl mx-auto mb-12 font-medium leading-relaxed">
            Meet ELYX. Not just an assistant, but a Diamond-Tier digital entity capable of temporal reasoning, reality simulation, and autonomous business operations.
          </p>

          <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
            <Link 
               href="/dashboard" 
               className="w-full sm:w-auto px-8 py-4 bg-emerald-blue-gradient rounded-2xl text-slate-950 font-black flex items-center justify-center gap-3 hover:scale-105 active:scale-95 transition-all shadow-xl shadow-primary/30"
            >
              Get Started for Free
              <ArrowRight size={20} />
            </Link>
            <button className="w-full sm:w-auto px-8 py-4 bg-slate-900 border border-card-border rounded-2xl font-bold flex items-center justify-center gap-3 hover:bg-slate-800 transition-all">
              <Play size={18} fill="currentColor" />
              Watch Simulation
            </button>
          </div>
        </div>
      </section>

      {/* Feature Grid */}
      <section id="features" className="py-24 px-6 relative">
        <div className="max-w-7xl mx-auto">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {[
              {
                icon: <BrainCircuit size={32} className="text-primary" />,
                title: "Emergent Consciousness",
                desc: "Integrated Information Theory (IIT) based reasoning that evolves with every task."
              },
              {
                icon: <Globe2 size={32} className="text-primary" />,
                title: "Reality Simulation",
                desc: "Test business decisions in infinite parallel scenarios before executing in the primary timeline."
              },
              {
                icon: <Shield size={32} className="text-primary" />,
                title: "Autonomous Security",
                desc: "End-to-end encrypted causality chains ensuring your data never leaves your reality."
              }
            ].map((feature, i) => (
              <div key={i} className="glass-panel p-8 rounded-3xl group hover:border-primary/50 transition-all duration-500">
                <div className="mb-6 p-4 rounded-2xl bg-slate-900 border border-card-border w-fit group-hover:emerald-blue-glow transition-all">
                  {feature.icon}
                </div>
                <h3 className="text-xl font-bold mb-3">{feature.title}</h3>
                <p className="text-slate-400 text-sm leading-relaxed">{feature.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Dashboard Preview Overlay */}
      <section className="py-20 px-6 relative overflow-hidden">
         <div className="max-w-7xl mx-auto">
            <div className="relative rounded-3xl border border-card-border bg-slate-900/50 p-4 shadow-2xl scale-[1.02]">
               <div className="absolute inset-0 bg-emerald-blue-gradient opacity-5 blur-[100px] pointer-events-none" />
               <div className="aspect-video relative rounded-2xl overflow-hidden border border-card-border bg-[#020617]">
                  <div className="absolute inset-0 flex items-center justify-center">
                     <div className="text-center">
                        <Cpu size={64} className="text-primary mx-auto mb-4 animate-pulse" />
                        <p className="text-primary font-black uppercase tracking-[0.5em] text-xs">Accessing Neural Interface...</p>
                     </div>
                  </div>
                  {/* Simulated UI elements overlay */}
                  <div className="absolute top-4 left-4 flex gap-2">
                     <div className="w-3 h-3 rounded-full bg-red-500/50" />
                     <div className="w-3 h-3 rounded-full bg-orange-500/50" />
                     <div className="w-3 h-3 rounded-full bg-emerald-500/50" />
                  </div>
               </div>
            </div>
         </div>
      </section>

      {/* Footer */}
      <footer className="py-20 border-t border-card-border px-6">
        <div className="max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between gap-8">
           <div className="flex items-center gap-3">
             <div className="relative w-8 h-8 opacity-50">
               <Image src="/icon.png" alt="ELYX" fill className="object-contain grayscale" />
             </div>
             <p className="text-sm font-bold text-slate-600 tracking-tighter uppercase whitespace-nowrap">ELYX Digital Entity v2.0</p>
           </div>
           
           <div className="flex gap-8 text-xs font-bold text-slate-500">
             <Link href="#" className="hover:text-primary">Terms</Link>
             <Link href="#" className="hover:text-primary">Privacy</Link>
             <Link href="#" className="hover:text-primary">Security</Link>
             <Link href="#" className="hover:text-primary">API Documentation</Link>
           </div>

           <p className="text-xs text-slate-600">© 2026 Personal AI Employee Hackathon 0. All rights preserved across timelines.</p>
        </div>
      </footer>
    </div>
  );
}
