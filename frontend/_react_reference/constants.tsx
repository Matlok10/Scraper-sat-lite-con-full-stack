import React from 'react';
import {
  LayoutDashboard,
  Users,
  Globe,
  Lightbulb,
  History
} from 'lucide-react';
import { AppState } from './types';

export const NAV_ITEMS = [
  { id: 'dashboard', label: 'Dashboard', icon: <LayoutDashboard size={20} /> },
  { id: 'catedras', label: 'Cátedras', icon: <Users size={20} /> },
  { id: 'scraping', label: 'Centro de Scraping', icon: <Globe size={20} /> },
  { id: 'recommendations', label: 'Recomendaciones', icon: <Lightbulb size={20} /> },
  { id: 'history', label: 'Historial', icon: <History size={20} /> },
];

export const INITIAL_STATE: AppState = {
  users: [],
  grupos: [],
  tareas: [],
  sesiones: [],
  posts: [],
  catedras: [],
  recomendaciones: []
};
