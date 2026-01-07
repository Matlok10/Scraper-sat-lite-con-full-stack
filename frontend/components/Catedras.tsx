import React, { useState } from 'react';
import { Catedra } from '../types';
import { Search, Plus, MoreVertical, Star } from 'lucide-react';

interface CatedrasProps {
  catedras: Catedra[];
}

const Catedras: React.FC<CatedrasProps> = ({ catedras }) => {
  const [filter, setFilter] = useState('');

  const filtered = catedras.filter(c => 
    c.nombre.toLowerCase().includes(filter.toLowerCase()) || 
    c.titular.toLowerCase().includes(filter.toLowerCase()) ||
    c.codigo.includes(filter)
  );

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-slate-800">Directorio de Cátedras</h2>
          <p className="text-slate-500">Gestión de unidades académicas y su reputación social</p>
        </div>
        <button className="bg-indigo-600 text-white px-4 py-2 rounded-xl flex items-center gap-2 hover:bg-indigo-700 transition-colors shadow-sm">
          <Plus size={18} />
          Nueva Cátedra
        </button>
      </div>

      <div className="relative">
        <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400" size={18} />
        <input 
          type="text" 
          placeholder="Buscar por nombre, código o titular..."
          className="w-full pl-12 pr-4 py-3 bg-white border border-slate-200 rounded-2xl focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent shadow-sm"
          value={filter}
          onChange={(e) => setFilter(e.target.value)}
        />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
        {filtered.map((c) => (
          <div key={c.id} className="bg-white p-6 rounded-2xl border border-slate-100 shadow-sm hover:shadow-md transition-shadow group">
            <div className="flex justify-between items-start mb-4">
              <div className="px-3 py-1 bg-slate-100 text-slate-600 rounded-full text-xs font-bold">
                {c.codigo}
              </div>
              <button className="text-slate-400 hover:text-slate-600">
                <MoreVertical size={18} />
              </button>
            </div>
            <h3 className="text-lg font-bold text-slate-800 mb-1 group-hover:text-indigo-600 transition-colors">{c.nombre}</h3>
            <p className="text-slate-500 text-sm mb-4">Titular: <span className="font-semibold">{c.titular}</span></p>
            
            <div className="pt-4 border-t border-slate-50 flex items-center justify-between">
              <div className="flex items-center gap-2">
                <div className="flex text-amber-400">
                  {[1, 2, 3, 4, 5].map((s) => <Star key={s} size={14} fill={s <= 4 ? 'currentColor' : 'none'} />)}
                </div>
                <span className="text-xs text-slate-400">(4.2)</span>
              </div>
              <div className="text-right">
                <p className="text-xs text-slate-400 uppercase font-bold tracking-wider">Menciones</p>
                <p className="text-lg font-black text-slate-800">{c.menciones_fb}</p>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Catedras;
