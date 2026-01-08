import React, { useState, useEffect } from 'react';
import Sidebar from './components/Sidebar';
import Dashboard from './components/Dashboard';
import Catedras from './components/Catedras';
import ScrapingCenter from './components/ScrapingCenter';
import Recommendations from './components/Recommendations';
import { INITIAL_STATE } from './constants';
import { AppState } from './types';
import { apiService } from './services/api';

const App: React.FC = () => {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [state, setState] = useState<AppState>(INITIAL_STATE);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const [catedras, grupos, tareas, sesiones, posts] = await Promise.all([
          apiService.getCatedras(),
          apiService.getGrupos(),
          apiService.getTareas(),
          apiService.getSesiones(),
          apiService.getPosts()
        ]);

        setState((prev: AppState) => ({
          ...prev,
          catedras,
          grupos,
          tareas,
          sesiones,
          posts
        }));
      } catch (error) {
        console.error("Error fetching data:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const renderContent = () => {
    if (loading) {
      return (
        <div className="flex items-center justify-center h-64">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
        </div>
      );
    }

    switch (activeTab) {
      case 'dashboard':
        return <Dashboard state={state} />;
      case 'catedras':
        return <Catedras catedras={state.catedras} />;
      case 'scraping':
        return <ScrapingCenter state={state} setState={setState} />;
      case 'recommendations':
        return <Recommendations state={state} />;
      case 'history':
        return (
          <div className="p-12 text-center bg-white rounded-3xl border border-slate-100">
            <h2 className="text-2xl font-bold text-slate-800 mb-2">Historial de Sesiones</h2>
            <p className="text-slate-500 mb-6">Módulo en construcción...</p>
            <div className="max-w-md mx-auto space-y-3">
              {state.sesiones.map((s: any) => (
                <div key={s.id} className="p-4 bg-slate-50 rounded-xl flex items-center justify-between">
                  <span className="text-sm font-bold text-slate-700">{s.fecha}</span>
                  <span className={`px-2 py-1 rounded-md text-[10px] font-bold ${s.estado === 'COMPLETADO' ? 'bg-emerald-100 text-emerald-700' : 'bg-orange-100 text-orange-700'}`}>{s.estado}</span>
                </div>
              ))}
            </div>
          </div>
        );
      default:
        return <Dashboard state={state} />;
    }
  };

  return (
    <div className="flex min-h-screen bg-slate-50">
      <Sidebar activeTab={activeTab} setActiveTab={setActiveTab} />

      <main className="flex-1 ml-64 p-8 custom-scroll h-screen overflow-y-auto">
        <header className="mb-8 flex items-center justify-between">
          <div>
            <p className="text-slate-400 text-xs font-bold uppercase tracking-widest mb-1">Bienvenido de nuevo,</p>
            <h1 className="text-3xl font-black text-slate-900">Control de Datos Académicos</h1>
          </div>
          <div className="flex items-center gap-4">
            <div className="bg-white p-2 rounded-xl border border-slate-200 shadow-sm relative">
              <span className="absolute -top-1 -right-1 w-3 h-3 bg-red-500 border-2 border-white rounded-full" />
              <svg className="w-5 h-5 text-slate-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"></path></svg>
            </div>
          </div>
        </header>

        <div className="animate-in fade-in duration-500">
          {renderContent()}
        </div>
      </main>
    </div>
  );
};

export default App;
