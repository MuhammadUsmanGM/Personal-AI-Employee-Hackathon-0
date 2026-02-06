"use client";

import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { 
  ShieldCheck, 
  Fingerprint, 
  Zap, 
  Mail, 
  Lock, 
  ArrowRight, 
  Loader2, 
  Github, 
  Chrome,
  AlertCircle,
  Cpu
} from "lucide-react";
import Image from "next/image";
import { useRouter } from "next/navigation";
import { supabase } from "@/lib/supabase";

export default function AuthPage() {
  const [isLogin, setIsLogin] = useState(true);
  const [loading, setLoading] = useState(false);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [scanVisible, setScanVisible] = useState(false);
  const router = useRouter();

  useEffect(() => {
    // Check if user is already logged in
    const checkUser = async () => {
      const { data: { session } } = await supabase.auth.getSession();
      if (session) {
        router.push("/dashboard");
      }
    };
    checkUser();
    
    // Initial animation delay
    const timer = setTimeout(() => setScanVisible(true), 1000);
    return () => clearTimeout(timer);
  }, [router]);

  const handleAuth = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      if (isLogin) {
        const { error } = await supabase.auth.signInWithPassword({ email, password });
        if (error) throw error;
      } else {
        const { error } = await supabase.auth.signUp({ email, password });
        if (error) throw error;
        alert("Verification email sent! Please check your inbox.");
      }
      router.push("/dashboard");
    } catch (err: any) {
      setError(err.message || "Neural authentication failed. Access denied.");
    } finally {
      setLoading(false);
    }
  };

  const socialLogin = async (provider: 'github' | 'google') => {
    try {
      const { error } = await supabase.auth.signInWithOAuth({ provider });
      if (error) throw error;
    } catch (err: any) {
      setError(`OAuth relay failed: ${err.message}`);
    }
  };

  return (
    <div className="min-h-screen bg-[#020617] flex items-center justify-center p-6 relative overflow-hidden font-sans">
      
      {/* Dynamic Background */}
      <div className="absolute inset-0 z-0">
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_50%_50%,rgba(6,182,212,0.1),transparent_50%)]" />
        <div className="absolute top-0 left-0 w-full h-full opacity-20 pointer-events-none">
          <div className="absolute inset-0 overflow-hidden">
            {[...Array(20)].map((_, i) => (
              <motion.div
                key={i}
                initial={{ opacity: 0, y: Math.random() * 1000 }}
                animate={{ 
                  opacity: [0.1, 0.3, 0.1], 
                  y: [0, -1000],
                }}
                transition={{ 
                  duration: Math.random() * 10 + 10, 
                  repeat: Infinity, 
                  ease: "linear",
                  delay: Math.random() * 10
                }}
                className="absolute w-px h-20 bg-primary"
                style={{ left: `${Math.random() * 100}%` }}
              />
            ))}
          </div>
        </div>
      </div>

      <div className="w-full max-w-[1200px] grid grid-cols-1 lg:grid-cols-2 gap-12 items-center relative z-10">
        
        {/* Left Side: Branding & Visuals */}
        <motion.div 
          initial={{ opacity: 0, x: -50 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.8 }}
          className="hidden lg:flex flex-col space-y-8"
        >
          <div className="flex items-center gap-4 group">
            <div className="relative">
              <div className="absolute inset-0 bg-primary blur-2xl opacity-20 group-hover:opacity-40 transition-opacity" />
              <div className="w-16 h-16 relative z-10 border border-primary/30 rounded-2xl flex items-center justify-center bg-slate-950 shadow-[0_0_30px_rgba(6,182,212,0.15)]">
                <Cpu className="text-primary w-8 h-8" />
              </div>
            </div>
            <h1 className="text-4xl font-black text-white tracking-tighter">
              ELYX <span className="text-primary italic">NEURAL</span>
            </h1>
          </div>

          <div className="space-y-6">
            <h2 className="text-6xl font-black text-white leading-tight tracking-tighter">
              Delegate Your <br />
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-primary via-cyan-400 to-indigo-500">
                Strategic Intelligence.
              </span>
            </h2>
            <p className="text-slate-400 text-lg font-medium max-w-md leading-relaxed">
              Login to access your personal AI employee network. Managed auth, local memory, and quantum sovereignty.
            </p>
          </div>

          <div className="grid grid-cols-2 gap-6 pt-8">
            <div className="glass-panel p-6 rounded-3xl border-card-border/30">
              <ShieldCheck className="text-primary mb-3" size={24} />
              <p className="text-sm font-black text-white uppercase tracking-widest mb-1">AES-256 Vault</p>
              <p className="text-[10px] text-slate-500 font-bold">End-to-end memory encryption.</p>
            </div>
            <div className="glass-panel p-6 rounded-3xl border-card-border/30">
              <Zap className="text-accent mb-3" size={24} />
              <p className="text-sm font-black text-white uppercase tracking-widest mb-1">Causal Sync</p>
              <p className="text-[10px] text-slate-500 font-bold">Real-time reality anchoring.</p>
            </div>
          </div>
        </motion.div>

        {/* Right Side: Auth Form */}
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.5, delay: 0.2 }}
          className="relative"
        >
          <div className="absolute -inset-4 bg-gradient-to-tr from-primary/10 via-transparent to-indigo-500/10 blur-3xl rounded-[3rem] -z-10" />
          
          <div className="glass-panel border-card-border/50 rounded-[3rem] p-10 md:p-12 shadow-[0_0_50px_rgba(0,0,0,0.5)] relative overflow-hidden">
            
            {/* Swiping Biometric Line Animation */}
            <AnimatePresence>
              {scanVisible && (
                <motion.div 
                  initial={{ top: "0%" }}
                  animate={{ top: "100%" }}
                  exit={{ opacity: 0 }}
                  transition={{ duration: 3, repeat: Infinity, ease: "linear" }}
                  className="absolute left-0 right-0 h-px bg-primary shadow-[0_0_15px_rgba(6,182,212,0.8)] z-20 pointer-events-none opacity-30"
                />
              )}
            </AnimatePresence>

            <div className="text-center mb-10">
              <div className="mb-6 inline-block md:hidden">
                <Image src="/logo.png" alt="ELYX" width={60} height={60} className="mx-auto" />
              </div>
              <h3 className="text-3xl font-black text-white tracking-tight mb-2">
                {isLogin ? "Neural Terminal Access" : "Create Neural Core"}
              </h3>
              <p className="text-slate-500 font-bold text-sm tracking-wide">
                SYSTEM STATUS: <span className="text-primary">AWAITING AUTHORIZATION</span>
              </p>
            </div>

            <form onSubmit={handleAuth} className="space-y-6">
              <div className="space-y-4">
                <div className="relative group">
                  <Mail className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-500 group-focus-within:text-primary transition-colors" size={18} />
                  <input 
                    type="email"
                    required
                    placeholder="E-MAIL ADDRESS"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    className="w-full bg-slate-900/50 border border-card-border rounded-2xl py-4 pl-12 pr-4 text-xs font-black text-white outline-none focus:border-primary/50 transition-all tracking-widest placeholder:text-slate-600"
                  />
                </div>

                <div className="relative group">
                  <Lock className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-500 group-focus-within:text-primary transition-colors" size={18} />
                  <input 
                    type="password"
                    required
                    placeholder="SECURITY KEY"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    className="w-full bg-slate-900/50 border border-card-border rounded-2xl py-4 pl-12 pr-4 text-xs font-black text-white outline-none focus:border-primary/50 transition-all tracking-widest placeholder:text-slate-600"
                  />
                </div>
              </div>

              {error && (
                <motion.div 
                  initial={{ opacity: 0, y: -10 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="flex items-center gap-3 p-4 bg-red-500/10 border border-red-500/20 rounded-2xl text-red-500 text-[10px] font-black uppercase tracking-widest"
                >
                  <AlertCircle size={16} />
                  {error}
                </motion.div>
              )}

              <button 
                type="submit"
                disabled={loading}
                className="w-full btn-premium-primary !py-5 shadow-[0_20px_40px_rgba(6,182,212,0.15)] flex items-center justify-center gap-3 group relative overflow-hidden"
              >
                <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/10 to-transparent -translate-x-full group-hover:translate-x-full transition-transform duration-1000" />
                {loading ? (
                  <Loader2 className="animate-spin" size={20} />
                ) : (
                  <>
                    <span className="tracking-[.25em]">{isLogin ? "INITIATE SESSION" : "PROVISION CORE"}</span>
                    <ArrowRight size={18} className="group-hover:translate-x-1 transition-transform" />
                  </>
                )}
              </button>
            </form>

            <div className="mt-10">
              <div className="relative flex items-center justify-center mb-8">
                <div className="absolute inset-0 flex items-center"><div className="w-full border-t border-card-border" /></div>
                <span className="relative px-4 bg-[#020617] text-[10px] font-black text-slate-500 uppercase tracking-widest">Bridged Access</span>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <button 
                  onClick={() => socialLogin('github')}
                  className="flex items-center justify-center gap-3 p-4 bg-slate-900/50 border border-card-border rounded-2xl hover:bg-slate-800 transition-all text-slate-300 font-bold text-xs"
                >
                  <Github size={18} />
                  GITHUB
                </button>
                <button 
                  onClick={() => socialLogin('google')}
                  className="flex items-center justify-center gap-3 p-4 bg-slate-900/50 border border-card-border rounded-2xl hover:bg-slate-800 transition-all text-slate-300 font-bold text-xs"
                >
                  <Chrome size={18} />
                  GOOGLE
                </button>
              </div>
            </div>

            <div className="mt-10 text-center">
              <button 
                onClick={() => setIsLogin(!isLogin)}
                className="text-[10px] font-black text-slate-400 hover:text-primary uppercase tracking-[0.2em] transition-all"
              >
                {isLogin ? "New Neural Entity? Provision Access" : "Existing Node? Sync Terminal"}
              </button>
            </div>
          </div>

          <div className="mt-8 flex items-center justify-center gap-6 text-[10px] font-black text-slate-600 uppercase tracking-[0.3em]">
            <div className="flex items-center gap-2">
              <div className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse" />
              Gateway Stable
            </div>
            <div className="w-px h-3 bg-slate-800" />
            <div className="flex items-center gap-2">
              <Fingerprint size={12} className="text-primary" />
              Diamond v2.0
            </div>
          </div>
        </motion.div>

      </div>
    </div>
  );
}
