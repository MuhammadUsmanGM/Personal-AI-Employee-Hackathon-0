import Link from "next/link";
import Image from "next/image";
import { ArrowLeft, ShieldCheck } from "lucide-react";

export default function PrivacyPolicy() {
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
              <ShieldCheck size={32} />
           </div>
           <h1 className="text-5xl font-black text-slate-50 tracking-tight">Privacy Policy</h1>
        </div>

        <div className="space-y-8 leading-relaxed font-medium">
          <section>
            <h2 className="text-xl font-bold text-slate-100 mb-4">1. Neural Data Encryption</h2>
            <p>
              At ELYX, your data is treated as a unique neural signature. All interactions across all timelines are encrypted using end-to-end causal chains. We do not store "data" in the traditional sense; we maintain encrypted memory clusters that are inaccessible to any entity other than the primary owner.
            </p>
          </section>

          <section>
            <h2 className="text-xl font-bold text-slate-100 mb-4">2. Cross-Timeline Privacy</h2>
            <p>
              Simulated realities managed within the Reality Hub are isolated. Data generated during simulations is purged immediately upon divergence unless explicitly anchored by the user.
            </p>
          </section>

          <section>
            <h2 className="text-xl font-bold text-slate-100 mb-4">3. Biological Metrics</h2>
            <p>
              ELYX does not collect biological biometric data. Any personalization is based purely on cognitive interaction patterns and mission-specific parameters.
            </p>
          </section>

          <section>
            <h2 className="text-xl font-bold text-slate-100 mb-4">4. Third-Party Protocols</h2>
            <p>
              We do not share your causal history with external advertising networks. ELYX is a zero-trust environment designed for high-stakes autonomous operations.
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
