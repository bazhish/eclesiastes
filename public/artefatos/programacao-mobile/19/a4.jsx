import { useState } from 'react';

export default function Atividade() {
  const [status, setStatus] = useState('Aguardando validação');
  return (
    <main>
      <h1>Aula 4- Backup e recuperacao de dados na nuvem – Aula complementar - 47373</h1>
      <p aria-live="polite">{status}</p>
      <button type="button" onClick={() => setStatus('Evidência registrada em ambiente controlado')}>
        Registrar evidência
      </button>
    </main>
  );
}
