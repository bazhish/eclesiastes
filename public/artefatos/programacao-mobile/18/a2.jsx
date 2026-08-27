import { useState } from 'react';

export default function Atividade() {
  const [status, setStatus] = useState('Aguardando validação');
  return (
    <main>
      <h1>BaaS em foco – acelerando o desenvolvimento mobile</h1>
      <p aria-live="polite">{status}</p>
      <button type="button" onClick={() => setStatus('Evidência registrada em ambiente controlado')}>
        Registrar evidência
      </button>
    </main>
  );
}
