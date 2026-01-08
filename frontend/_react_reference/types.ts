export interface User {
  id: number;
  username: string;
  email: string;
}

export interface GrupoFacebook {
  id: number;
  nombre: string;
  url: string;
  prioridad: number;
  activo: boolean;
}

export interface TareaScrapeo {
  id: number;
  grupo_id: number;
  keywords: string[];
  frecuencia_dias: number;
}

export interface SesionScraping {
  id: number;
  usuario_id: number;
  tarea_id: number;
  estado: 'PENDIENTE' | 'PROCESANDO' | 'COMPLETADO' | 'FALLIDO';
  posts_encontrados: number;
  fecha: string;
}

export interface PostScrapeado {
  id: number;
  grupo_id: number;
  post_id: string;
  texto: string;
  procesado: boolean;
}

export interface Catedra {
  id: number;
  codigo: string;
  nombre: string;
  titular: string;
  menciones_fb: number;
}

export interface Recomendacion {
  id: number;
  catedra_id: number;
  post_origen_id: number;
  contribuidor_id?: number;
  texto: string;
  sentimiento: 'POSITIVO' | 'NEUTRAL' | 'NEGATIVO';
  confianza: number;
  votos_utilidad: number;
}

export interface AppState {
  users: User[];
  grupos: GrupoFacebook[];
  tareas: TareaScrapeo[];
  sesiones: SesionScraping[];
  posts: PostScrapeado[];
  catedras: Catedra[];
  recomendaciones: Recomendacion[];
}
