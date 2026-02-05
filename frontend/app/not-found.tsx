"use client";

import Link from "next/link";
import Image from "next/image";
import { ArrowLeft, Home } from "lucide-react";

export default function NotFound() {
  return (
    <div className="min-h-screen bg-[#020617] flex flex-col items-center justify-center relative overflow-hidden px-6">
      {/* Sharpened Background 404 */}
      <div className="absolute inset-0 flex items-center justify-center pointer-events-none select-none overflow-hidden z-0">
        <h1 className="text-[35vw] md:text-[45vw] font-black leading-none opacity-60" 
            style={{ 
              background: 'linear-gradient(to bottom, #06b6d4, #10b981)',
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent',
              filter: 'drop-shadow(0 0 20px rgba(6, 182, 212, 0.4))'
            }}>
          404
        </h1>
      </div>

      {/* Very Subtle Vignette instead of a wall of blur */}
      <div className="absolute inset-0 bg-gradient-to-t from-[#020617] via-transparent to-[#020617] opacity-80 pointer-events-none z-1" />

      {/* Main Content */}
      <div className="relative z-10 flex flex-col items-center text-center max-w-2xl">
        <div className="mb-12 animate-in slide-in-from-top duration-1000">
           <Image 
             src="/logo.png" 
             alt="ELYX Logo" 
             width={180} 
             height={60} 
             className="drop-shadow-[0_0_25px_rgba(79,209,243,0.3)]"
           />
        </div>

        <h2 className="text-4xl md:text-5xl font-black tracking-tight text-slate-50 mb-6 drop-shadow-sm">
          Reality Divergence Detected
        </h2>
        
        <p className="text-lg text-slate-400 font-medium mb-12 leading-relaxed">
          The causal path you're looking for does not exist in any monitored timeline. 
          The coordinates may have been purged or relocated to a secure sector.
        </p>

        <div className="flex flex-col sm:flex-row gap-4 w-full sm:w-auto">
          <Link 
            href="/dashboard"
            className="px-8 py-4 rounded-2xl font-black text-[#020617] flex items-center justify-center gap-3 hover:scale-105 active:scale-95 transition-all shadow-[0_0_30px_rgba(79,209,243,0.3)] group"
            style={{ background: 'linear-gradient(135deg, #06b6d4 0%, #10b981 100%)' }}
          >
            <Home size={20} className="group-hover:rotate-12 transition-transform" />
            Return to Mission Control
          </Link>
          
          <button 
            onClick={() => window.history.back()}
            className="px-8 py-4 bg-slate-900/50 backdrop-blur-md border border-slate-700/50 rounded-2xl font-bold text-slate-300 flex items-center justify-center gap-3 hover:bg-slate-800 transition-all active:scale-95 hover:border-slate-500"
          >
            <ArrowLeft size={20} />
            Revert Timeline
          </button>
        </div>
      </div>

      {/* Decorative Elements */}
      <div className="absolute bottom-10 left-10 opacity-20 hidden lg:block">
         <div className="text-[10px] font-mono text-slate-500 uppercase tracking-[0.5em] vertical-text">
            ERROR_CODE: REALITY_MISSING_VERSION_2.0
         </div>
      </div>
      
      <div className="absolute top-1/2 -right-20 w-80 h-80 bg-primary/10 rounded-full blur-[120px] pointer-events-none" />
      <div className="absolute -bottom-20 -left-20 w-80 h-80 bg-accent/10 rounded-full blur-[120px] pointer-events-none" />
    </div>
  );
}
