"use client";

import { useEffect } from "react";
import Image from "next/image";
import Link from "next/link";
import { RefreshCcw, Home, AlertTriangle } from "lucide-react";

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    // Log the error to an error reporting service
    console.error(error);
  }, [error]);

  return (
    <div className="min-h-screen bg-[#020617] flex flex-col items-center justify-center relative overflow-hidden px-6">
      {/* Sharpened Background "ERROR" Text */}
      <div className="absolute inset-0 flex items-center justify-center pointer-events-none select-none overflow-hidden z-0">
        <h1 className="text-[25vw] md:text-[35vw] font-black leading-none opacity-30 text-red-500/50" 
            style={{ 
              filter: 'drop-shadow(0 0 30px rgba(239, 68, 68, 0.3))'
            }}>
          ERROR
        </h1>
      </div>

      {/* Subtle Depth Overlay */}
      <div className="absolute inset-0 bg-gradient-to-b from-[#020617] via-transparent to-[#020617] opacity-90 pointer-events-none z-1" />

      {/* Main Content */}
      <div className="relative z-10 flex flex-col items-center text-center max-w-2xl px-4">
        <div className="mb-12 animate-bounce">
           <div className="w-24 h-24 rounded-3xl bg-red-500/10 border border-red-500/20 flex items-center justify-center text-red-500 shadow-[0_0_50px_rgba(239,68,68,0.2)]">
              <AlertTriangle size={48} />
           </div>
        </div>

        <div className="mb-8">
           <Image 
             src="/logo.png" 
             alt="ELYX Logo" 
             width={140} 
             height={48} 
             className="opacity-50 grayscale brightness-200"
           />
        </div>

        <h2 className="text-4xl md:text-5xl font-black tracking-tight text-slate-50 mb-6 drop-shadow-lg">
          System Neural Divergence
        </h2>
        
        <p className="text-lg text-slate-400 font-medium mb-12 leading-relaxed">
          The ELYX core encountered a cognitive anomaly during execution. 
          The local timeline has been temporarily suspended to prevent data corruption.
        </p>

        <div className="flex flex-col sm:flex-row gap-4 w-full sm:w-auto">
          <button 
            onClick={() => reset()}
            className="px-8 py-4 bg-emerald-blue-gradient rounded-2xl font-black text-[#020617] flex items-center justify-center gap-3 hover:scale-105 active:scale-95 transition-all shadow-[0_0_30px_rgba(79,209,243,0.3)] group"
          >
            <RefreshCcw size={20} className="group-hover:rotate-180 transition-transform duration-500" />
            Synchronize Core (Retry)
          </button>
          
          <Link 
            href="/"
            className="px-8 py-4 bg-slate-900/50 backdrop-blur-md border border-slate-700/50 rounded-2xl font-bold text-slate-300 flex items-center justify-center gap-3 hover:bg-slate-800 transition-all active:scale-95"
          >
            <Home size={20} />
            Safe Point Rebound
          </Link>
        </div>

        {/* Technical Digest */}
        {error.digest && (
          <div className="mt-12 p-3 rounded-xl bg-slate-900/20 border border-slate-800/50">
             <p className="text-[10px] font-mono text-slate-600 uppercase tracking-widest leading-none">
                Anomaly Hash: {error.digest}
             </p>
          </div>
        )}
      </div>

      {/* Decorative Red Pulse */}
      <div className="absolute -top-40 -left-40 w-[600px] h-[600px] bg-red-900/10 rounded-full blur-[150px] pointer-events-none" />
      <div className="absolute -bottom-40 -right-40 w-[600px] h-[600px] bg-primary/10 rounded-full blur-[150px] pointer-events-none" />
    </div>
  );
}
