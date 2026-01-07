import React from 'react';
import { AppState } from '../types';
import { ThumbsUp, MessageSquare, TrendingDown, TrendingUp, Minus } from 'lucide-react';

interface RecommendationsProps {
  state: AppState;
}

const Recommendations: React.FC<RecommendationsProps> = ({ state }) => {
  const getCatedraName = (id: number) => state.catedras.find(c => c.id === id)?.nombre || 'Cátedra Desconocida';
  
  const getSentimentIcon = (sentiment: string) => {
    switch (sentiment) {
      case 'POSITIVO': return <TrendingUp className="text-emerald-500" size={18} />;
      case 'NEGATIVO': return <TrendingDown className="text-rose-500" size={18} />;
      default: return <Minus className="text-slate-400" size={18} />;
    }
  };

  const getSentimentClass = (sentiment: string) => {
    switch (sentiment) {
      case 'POSITIVO': return 'bg-emerald-50 text-emerald-700 border-emerald-100';
      case 'NEGATIVO': return 'bg-rose-50 text-rose-700 border-rose-100';
      default: return 'bg-slate-50 text-slate-700 border-slate-100';
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-slate-800">Base de Recomendaciones</h2>
        <p className="text-slate-500">Perspectivas curadas por IA a partir de interacciones de estudiantes</p>
      </div>

      <div className="grid grid-cols-1 gap-4">
        {state.recomendaciones.sort((a, b) => b.id - a.id).map((rec) => (
          <div key={rec.id} className="bg-white p-6 rounded-2xl border border-slate-100 shadow-sm flex flex-col md:flex-row gap-6">
            <div className="md:w-1/4">
               <div className="mb-2">
                 <span className={`px-3 py-1 rounded-full text-[10px] font-bold border ${getSentimentClass(rec.sentimiento)}`}>
                   {rec.sentimiento}
                 </span>
               </div>
               <h4 className="font-bold text-slate-800 text-sm leading-tight mb-2">{getCatedraName(rec.catedra_id)}</h4>
               <div className="flex items-center gap-2 text-slate-400 text-xs">
                 <span>Confianza:</span>
                 <div className="flex-1 h-1.5 bg-slate-100 rounded-full overflow-hidden">
                   <div 
                    className="h-full bg-indigo-500 transition-all" 
                    style={{ width: `${rec.confianza * 100}%` }} 
                   />
                 </div>
                 <span className="font-bold">{(rec.confianza * 100).toFixed(0)}%</span>
               </div>
            </div>

            <div className="flex-1 border-l border-slate-50 md:pl-6">
              <div className="flex items-start gap-4">
                 <div className="p-3 bg-indigo-50 text-indigo-600 rounded-xl">
                    <MessageSquare size={20} />
                 </div>
                 <div className="flex-1">
                    <p className="text-slate-700 italic text-sm mb-4">"{rec.texto}"</p>
                    <div className="flex items-center justify-between">
                       <p className="text-[10px] text-slate-400">Origen: Post #{rec.post_origen_id}</p>
                       <div className="flex items-center gap-4">
                          <button className="flex items-center gap-2 text-slate-400 hover:text-indigo-600 transition-colors text-xs font-bold">
                             <ThumbsUp size={14} />
                             Es útil ({rec.votos_utilidad})
                          </button>
                       </div>
                    </div>
                 </div>
              </div>
            </div>

            <div className="md:w-12 flex items-center justify-center">
               {getSentimentIcon(rec.sentimiento)}
            </div>
          </div>
        ))}

        {state.recomendaciones.length === 0 && (
          <div className="py-20 flex flex-col items-center text-slate-400 bg-white rounded-2xl border border-dashed border-slate-200">
             <MessageSquare size={48} className="mb-4 opacity-20" />
             <p className="text-lg">No hay recomendaciones generadas aún</p>
             <p className="text-sm">Inicia una auditoría de IA en el Centro de Scraping</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default Recommendations;
