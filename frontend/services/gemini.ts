export interface GeminiResult {
  catedraNombre: string;
  recomendacionTexto: string;
  sentimiento: 'positivo' | 'negativo' | 'neutral';
  confianza: number;
}

export async function analyzePost(postTexto: string, catedraNombres: string[]): Promise<GeminiResult | null> {
  // Placeholder: aquí iría la llamada real a Gemini/Vertex o a tu API de NLP
  // Devolvemos un resultado ficticio para mantener la UI funcional
  const random = Math.random();
  const sentimiento: GeminiResult['sentimiento'] = random > 0.66 ? 'positivo' : random > 0.33 ? 'neutral' : 'negativo';
  const confianza = 0.7 + Math.random() * 0.3;
  const catedraNombre = catedraNombres[Math.floor(Math.random() * catedraNombres.length)] || 'Sin asignar';
  return {
    catedraNombre,
    recomendacionTexto: postTexto.slice(0, 120) + '...',
    sentimiento,
    confianza
  };
}
