"use client";

import { useState } from "react";
import DashboardLayout from "@/components/DashboardLayout";
import { 
  Settings, 
  MessageSquare, 
  CheckCircle2, 
  Bell, 
  Cpu, 
  Shield, 
  BrainCircuit,
  Save,
  RefreshCw,
  ToggleLeft,
  ToggleRight,
  ChevronRight
} from "lucide-react";

export default function SettingsPage() {
  const [activeTab, setActiveTab] = useState("communication");

  const tabs = [
    { id: "communication", label: "Communication", icon: <MessageSquare size={18} /> },
    { id: "workflow", label: "Workflow", icon: <CheckCircle2 size={18} /> },
    { id: "notifications", label: "Notifications", icon: <Bell size={18} /> },
    { id: "ai_behavior", label: "AI Behavior", icon: <Cpu size={18} /> },
    { id: "security", label: "System Security", icon: <Shield size={18} /> }
  ];

  return (
    <DashboardLayout>
      <div className="p-8 max-w-6xl mx-auto">
        {/* Header */}
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-6 mb-12">
          <div>
            <h1 className="text-4xl font-black text-white mb-2 flex items-center gap-3">
              <Settings className="text-primary" size={32} />
              System Configuration
            </h1>
            <p className="text-slate-500 font-medium">Fine-tune your ELYX digital employee's neural constraints and operational scope.</p>
          </div>
          <button className="btn-premium-primary !px-8 !py-4">
            <Save size={18} />
            Commit Changes
          </button>
        </div>

        <div className="grid lg:grid-cols-[280px_1fr] gap-10">
          {/* Navigation Tabs */}
          <div className="space-y-2">
            {tabs.map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`w-full flex items-center justify-between p-4 rounded-2xl transition-all duration-300 group ${
                  activeTab === tab.id 
                    ? "bg-primary/10 text-primary border border-primary/20 shadow-[0_0_20px_rgba(6,182,212,0.1)]" 
                    : "text-slate-400 hover:bg-slate-800/50 hover:text-slate-200"
                }`}
              >
                <div className="flex items-center gap-3">
                  <div className={`transition-colors ${activeTab === tab.id ? "text-primary" : "text-slate-500 group-hover:text-primary"}`}>
                    {tab.icon}
                  </div>
                  <span className="font-bold text-sm uppercase tracking-widest">{tab.label}</span>
                </div>
                <ChevronRight size={16} className={`transition-transform ${activeTab === tab.id ? "opacity-100 translate-x-0" : "opacity-0 -translate-x-2"}`} />
              </button>
            ))}
          </div>

          {/* Settings Content */}
          <div className="glass-panel rounded-[2rem] p-10 min-h-[600px] border-card-border/30">
            {activeTab === "communication" && (
              <div className="space-y-10 animate-fade-in">
                <section>
                  <h3 className="text-xl font-bold text-white mb-6 flex items-center gap-2">
                    <MessageSquare size={20} className="text-primary" />
                    Communication Preferences
                  </h3>
                  <div className="space-y-6">
                    <SettingToggle 
                      title="Autonomous WhatsApp Engagement" 
                      desc="Allow ELYX to initiate and respond to WhatsApp messages without human oversight."
                      active={true}
                    />
                    <SettingToggle 
                      title="LinkedIn Outreach Protocol" 
                      desc="Enable autonomous processing of LinkedIn connection requests and direct messages."
                      active={true}
                    />
                    <SettingToggle 
                      title="Email Priority Sorting" 
                      desc="Automatically categorize incoming emails based on neural urgency detection."
                      active={false}
                    />
                  </div>
                </section>

                <section className="pt-10 border-t border-card-border/30">
                  <h3 className="text-lg font-bold text-white mb-4">Brand Voice Profile</h3>
                  <select className="w-full bg-slate-900 border border-card-border rounded-xl p-4 text-slate-300 font-medium focus:border-primary outline-none transition-all">
                    <option>Corporate Professional (Standard)</option>
                    <option>Technical Specialist</option>
                    <option>Friendly & Approachable</option>
                    <option>Minimalist / Concise</option>
                  </select>
                </section>
              </div>
            )}

            {activeTab === "workflow" && (
              <div className="space-y-10 animate-fade-in">
                <section>
                  <h3 className="text-xl font-bold text-white mb-6 flex items-center gap-2">
                    <CheckCircle2 size={20} className="text-primary" />
                    Approval Workflow
                  </h3>
                  <div className="space-y-8">
                    <SettingToggle 
                      title="Strict Causal Verification" 
                      desc="Require dual-layered reality verification for all high-stakes business decisions."
                      active={true}
                    />
                    <div className="p-6 rounded-2xl bg-primary/5 border border-primary/10">
                      <p className="text-xs font-black uppercase tracking-[0.2em] text-primary mb-2">Threshold Configuration</p>
                      <input type="range" className="w-full accent-primary h-2 bg-slate-900 rounded-lg appearance-none cursor-pointer" />
                      <div className="flex justify-between mt-2 text-[10px] font-bold text-slate-500 uppercase tracking-widest">
                        <span>Low Autonomy</span>
                        <span className="text-primary">Current: 85% Auto</span>
                        <span>Full Autonomy</span>
                      </div>
                    </div>
                  </div>
                </section>
              </div>
            )}

            {activeTab === "ai_behavior" && (
              <div className="space-y-10 animate-fade-in">
                <section>
                  <h3 className="text-xl font-bold text-white mb-6 flex items-center gap-2">
                    <BrainCircuit size={20} className="text-primary" />
                    Neural Logic Constraints
                  </h3>
                  <div className="space-y-6">
                    <SettingToggle 
                      title="Temporal Projection" 
                      desc="Enable the AI to project outcomes into simulated future timelines before responding."
                      active={true}
                    />
                    <SettingToggle 
                      title="Emotional Resonance System" 
                      desc="Allow AI to adjust communication tone based on detected human emotional states."
                      active={true}
                    />
                    <SettingToggle 
                      title="Existential Safety Mode" 
                      desc="Ensure all AI reasoning adheres to primary ethical and operational anchors."
                      active={true}
                    />
                  </div>
                </section>
              </div>
            )}

            {activeTab === "notifications" && (
              <div className="space-y-10 animate-fade-in">
                <section>
                  <h3 className="text-xl font-bold text-white mb-6 flex items-center gap-2">
                    <Bell size={20} className="text-primary" />
                    Neural Alert Configurations
                  </h3>
                  <div className="space-y-6">
                    <SettingToggle 
                      title="Instant Operational Alerts" 
                      desc="Receive real-time notifications for every autonomous action performed."
                      active={true}
                    />
                    <SettingToggle 
                      title="Strategy Verification Requests" 
                      desc="Notify via desktop and mobile when a high-stakes decision requires manual oversight."
                      active={true}
                    />
                    <SettingToggle 
                      title="Daily Intelligence Digest" 
                      desc="Synthesize all interactions into a single comprehensive morning report."
                      active={false}
                    />
                  </div>
                </section>

                <section className="pt-10 border-t border-card-border/30">
                  <h3 className="text-lg font-bold text-white mb-4">Notification Channels</h3>
                  <div className="grid grid-cols-2 gap-4">
                    <button className="flex items-center justify-between p-4 rounded-xl bg-slate-900 border border-card-border hover:border-primary/50 transition-all">
                      <span className="text-xs font-bold text-slate-300">Desktop Push</span>
                      <div className="w-2 h-2 rounded-full bg-primary" />
                    </button>
                    <button className="flex items-center justify-between p-4 rounded-xl bg-slate-900 border border-card-border hover:border-primary/50 transition-all">
                      <span className="text-xs font-bold text-slate-300">Email Alerts</span>
                      <div className="w-2 h-2 rounded-full bg-primary" />
                    </button>
                  </div>
                </section>
              </div>
            )}

            {/* Placeholder for other tabs to keep UI consistent */}
            {activeTab === "security" && (
              <div className="flex flex-col items-center justify-center h-full text-center space-y-6">
                 <div className="p-8 rounded-full bg-slate-900/50 border border-card-border animate-pulse">
                   <RefreshCw size={48} className="text-slate-600" />
                 </div>
                 <h3 className="text-xl font-bold text-slate-400 uppercase tracking-widest">Sector Initializing</h3>
                 <p className="text-slate-600 max-w-xs mx-auto">This neural configuration module is currently being optimized for your tier.</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
}

function SettingToggle({ title, desc, active }: { title: string, desc: string, active: boolean }) {
  return (
    <div className="flex items-start justify-between gap-6 p-4 hover:bg-slate-900/40 rounded-2xl transition-colors">
      <div className="space-y-1">
        <h4 className="text-sm font-bold text-slate-100 uppercase tracking-wider">{title}</h4>
        <p className="text-xs text-slate-500 leading-relaxed max-w-md">{desc}</p>
      </div>
      <button className={`transition-colors duration-300 ${active ? 'text-primary' : 'text-slate-800'}`}>
        {active ? <ToggleRight size={40} /> : <ToggleLeft size={40} />}
      </button>
    </div>
  );
}
