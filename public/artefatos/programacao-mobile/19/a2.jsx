import { useState } from 'react';

export default function Atividade() {
  const [status, setStatus] = useState('Aguardando validação');
  return (
    <main>
      <h1>Aula 2- Integracao com AWS S3 – Aula complementar - 47370</h1>
      <p aria-live="polite">{status}</p>
      <button type="button" onClick={() => setStatus('Evidência registrada em ambiente controlado')}>
        Registrar evidência
      </button>
    </main>
  );
}
