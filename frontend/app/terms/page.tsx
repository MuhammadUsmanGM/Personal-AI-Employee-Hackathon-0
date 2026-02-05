"use client";

import Link from "next/link";
import Image from "next/image";
import { ArrowLeft, FileText } from "lucide-react";

export default function TermsAndConditions() {
  return (
    <div className="min-h-screen bg-[#020617] text-slate-300 py-20 px-6 selection:bg-primary selection:text-slate-950 relative overflow-hidden">
      {/* Premium Watermark */}
      <div className="absolute inset-0 flex items-center justify-center pointer-events-none select-none overflow-hidden z-0 opacity-[0.03]">
        <Image 
          src="/icon.png" 
          alt="" 
          width={800} 
          height={800} 
          className="grayscale"
        />
      </div>

      <div className="max-w-3xl mx-auto relative z-10">
        <Link href="/" className="inline-flex items-center gap-2 text-primary font-bold mb-12 hover:gap-3 transition-all">
          <ArrowLeft size={20} />
          Back to Reality
        </Link>
        
        <div className="flex items-center gap-4 mb-8">
           <div className="p-3 rounded-2xl bg-primary/10 text-primary border border-primary/20">
              <FileText size={32} />
           </div>
           <h1 className="text-5xl font-black text-slate-50 tracking-tight">Terms of Service</h1>
        </div>

        <div className="space-y-8 leading-relaxed font-medium">
          <section>
            <h2 className="text-xl font-bold text-slate-100 mb-4">1. Acceptance of Neural Terms</h2>
            <p>
              By accessing ELYX, you agree to bound by these terms across all primary and simulated timelines. You represent that you have the cognitive authority to enter into this agreement.
            </p>
          </section>

          <section>
            <h2 className="text-xl font-bold text-slate-100 mb-4">2. Autonomy and Usage</h2>
            <p>
              ELYX operates as a semi-autonomous digital entity. While ELYX provides high-level business reasoning and reality simulation, the ultimate decision-making responsibility remains with the primary owner (User). ELYX is not responsible for outcomes resulting from autonomous task execution initiated by the user.
            </p>
          </section>

          <section>
            <h2 className="text-xl font-bold text-slate-100 mb-4">3. Prohibited Realities</h2>
            <p>
              Users may not use ELYX to simulate illicit activities, generate malicious causal loops, or attempt to breach the neural integrity of other users' realities.
            </p>
          </section>

          <section>
            <h2 className="text-xl font-bold text-slate-100 mb-4">4. Termination of Access</h2>
            <p>
              Violation of safety protocols may result in the immediate suspension of your neural signature and purging of all associated temporal data.
            </p>
          </section>
        </div>

        <div className="mt-20 pt-8 border-t border-card-border text-xs text-slate-500">
           Last updated: February 2026 • Version 2.0 (Diamond Tier)
        </div>
      </div>
    </div>
  );
}
