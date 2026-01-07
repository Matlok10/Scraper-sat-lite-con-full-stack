import React, { useState } from 'react';
import { AppState } from '../types';
import { Play, Settings2, Globe, AlertTriangle, ExternalLink, Cpu } from 'lucide-react';
import { analyzePost } from '../services/gemini';

interface ScrapingCenterProps {
  state: AppState;
  setState: React.Dispatch<React.SetStateAction<AppState>>;
}

const ScrapingCenter: React.FC<ScrapingCenterProps> = ({ state, setState }) => {
  const [isProcessing, setIsProcessing] = useState(false);
  const [processingStatus, setProcessingStatus] = useState('');

  const runAIAudit = async () => {
    setIsProcessing(true);
    setProcessingStatus('Analizando posts pendientes con Gemini...');
    
    const pendingPosts = state.posts.filter(p => !p.procesado);
    const catedraNombres = state.catedras.map(c => c.nombre);
    
    for (const post of pendingPosts) {
      setProcessingStatus(`Procesando post: ${post.post_id}...`);
      const result = await analyzePost(post.texto, catedraNombres);
      
      if (result) {
        const matchedCatedra = state.catedras.find(c => 
          c.nombre.toLowerCase().includes(result.catedraNombre.toLowerCase()) ||
          result.catedraNombre.toLowerCase().includes(c.nombre.toLowerCase())
        );

        if (matchedCatedra) {
          const newRec = {
            id: Date.now() + Math.random(),
            catedra_id: matchedCatedra.id,
            post_origen_id: post.id,
            texto: result.recomendacionTexto,
            sentimiento: result.sentimiento.toUpperCase() as any,
            confianza: result.confianza,
            votos_utilidad: 0
          };

          setState(prev => ({
            ...prev,
            recomendaciones: [...prev.recomendaciones, newRec],
            posts: prev.posts.map(p => p.id === post.id ? { ...p, procesado: true } : p),
            catedras: prev.catedras.map(c => c.id === matchedCatedra.id ? { ...c, menciones_fb: c.menciones_fb + 1 } : c)
          }));
        }
      }
      await new Promise(r => setTimeout(r, 800));
    }
    
    setProcessingStatus('Análisis completado.');
    setTimeout(() => {
      setIsProcessing(false);
      setProcessingStatus('');
    }, 2000);
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-slate-800">Centro de Scraping</h2>
          <p className="text-slate-500">Configuración de fuentes y auditoría IA</p>
        </div>
        <div className="flex gap-3">
           <button 
            onClick={runAIAudit}
            disabled={isProcessing}
            className={`px-4 py-2 rounded-xl flex items-center gap-2 transition-all shadow-sm ${
              isProcessing ? 'bg-slate-200 text-slate-500 cursor-not-allowed' : 'bg-indigo-600 text-white hover:bg-indigo-700'
            }`}
          >
            <Cpu size={18} className={isProcessing ? 'animate-spin' : ''} />
            {isProcessing ? 'Procesando IA...' : 'Auditar con IA'}
          </button>
          <button className="bg-emerald-600 text-white px-4 py-2 rounded-xl flex items-center gap-2 hover:bg-emerald-700 transition-all shadow-sm">
            <Play size={18} />
            Lanzar Scraper
          </button>
        </div>
      </div>

      {processingStatus && (
        <div className="bg-indigo-50 border border-indigo-100 p-4 rounded-2xl flex items-center gap-4 animate-pulse">
           <div className="w-2 h-2 bg-indigo-600 rounded-full animate-ping" />
           <p className="text-indigo-700 text-sm font-medium">{processingStatus}</p>
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-6">
          <div className="bg-white rounded-2xl border border-slate-100 shadow-sm overflow-hidden">
            <div className="p-6 border-b border-slate-50 flex items-center justify-between">
              <h3 className="font-bold text-slate-800">Fuentes Configuradas</h3>
              <Globe size={18} className="text-slate-400" />
            </div>
            <div className="divide-y divide-slate-50">
              {state.grupos.map(grupo => (
                <div key={grupo.id} className="p-6 flex items-center justify-between hover:bg-slate-50 transition-colors">
                  <div className="flex items-center gap-4">
                    <div className={`w-10 h-10 rounded-xl flex items-center justify-center ${grupo.activo ? 'bg-indigo-100 text-indigo-600' : 'bg-slate-100 text-slate-400'}`}>
                      <Globe size={20} />
                    </div>
                    <div>
                      <h4 className="font-bold text-slate-800 text-sm">{grupo.nombre}</h4>
                      <p className="text-xs text-slate-500 flex items-center gap-1">
                        {grupo.url} <ExternalLink size={10} />
                      </p>
                    </div>
                  </div>
                  <div className="flex items-center gap-6">
                    <div className="text-center">
                      <p className="text-[10px] text-slate-400 uppercase font-bold">Prioridad</p>
                      <p className="text-sm font-bold text-slate-700">{grupo.prioridad}</p>
                    </div>
                    <div className="flex items-center gap-2">
                       <span className={`w-2 h-2 rounded-full ${grupo.activo ? 'bg-emerald-500' : 'bg-slate-300'}`} />
                       <span className="text-xs font-medium text-slate-600">{grupo.activo ? 'Activo' : 'Inactivo'}</span>
                    </div>
                    <button className="p-2 text-slate-400 hover:text-slate-600 bg-slate-50 rounded-lg">
                      <Settings2 size={16} />
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        <div className="space-y-6">
           <div className="bg-amber-50 border border-amber-100 p-6 rounded-2xl">
            <div className="flex items-center gap-3 mb-4">
              <AlertTriangle className="text-amber-600" size={24} />
              <h3 className="font-bold text-amber-900">Posts sin Procesar</h3>
            </div>
            <p className="text-amber-800 text-sm mb-4">
              Hay <span className="font-bold">{state.posts.filter(p => !p.procesado).length} posts</span> nuevos que requieren análisis de sentimiento y extracción de recomendaciones.
            </p>
            <button 
               onClick={runAIAudit}
               className="w-full bg-amber-600 text-white py-2 rounded-xl font-bold hover:bg-amber-700 transition-colors shadow-sm text-sm"
            >
              Auditar Pendientes
            </button>
          </div>

          <div className="bg-white p-6 rounded-2xl border border-slate-100 shadow-sm">
            <h3 className="font-bold text-slate-800 mb-4">Configuración de Tareas</h3>
            <div className="space-y-4">
               {state.tareas.map(tarea => (
                 <div key={tarea.id} className="p-4 bg-slate-50 rounded-xl border border-slate-100">
                    <div className="flex justify-between items-start mb-2">
                       <span className="text-xs font-bold text-indigo-600 uppercase">Frecuencia: {tarea.frecuencia_dias} días</span>
                       <button className="text-slate-400"><Settings2 size={14} /></button>
                    </div>
                    <div className="flex flex-wrap gap-2">
                       {tarea.keywords.map((k, i) => (
                         <span key={i} className="px-2 py-0.5 bg-white text-slate-600 text-[10px] rounded-md border border-slate-200">#{k}</span>
                       ))}
                    </div>
                 </div>
               ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ScrapingCenter;
