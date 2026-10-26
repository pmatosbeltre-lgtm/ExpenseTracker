import { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8080/gastos';

function App() {
  const [gastos, setGastos] = useState([]);
  const [form, setForm] = useState({
    concepto: '',
    monto: '',
    tipo: 'gasto',
    fecha: new Date().toISOString().split('T')[0]
  });

  const obtenerGastos = async () => {
    try {
      const res = await axios.get(API_URL);
      setGastos(res.data);
    } catch (err) {
      console.error("Error al obtener gastos:", err);
    }
  };

  useEffect(() => {
    obtenerGastos();
  }, []);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post(API_URL, {
        concepto: form.concepto,
        monto: parseFloat(form.monto),
        tipo: form.tipo,
        fecha: form.fecha
      });
      setForm({ concepto: '', monto: '', tipo: 'gasto', fecha: new Date().toISOString().split('T')[0] });
      obtenerGastos();
    } catch (err) {
      console.error("Error al guardar gasto:", err);
    }
  };

  const handleDelete = async (id) => {
    try {
      await axios.delete(`${API_URL}/${id}`);
      obtenerGastos();
    } catch (err) {
      console.error("Error al eliminar gasto:", err);
    }
  };

  const total = gastos.reduce((acc, g) => {
    return g.tipo === 'ingreso' ? acc + g.monto : acc - g.monto;
  }, 0);

  return (
    <div className="container">
      {/* Header y Balance */}
      <div className="header-card">
        <h1>Control de Gastos</h1>
        <div className="balance-box">
          <div className="balance-title">Balance Total</div>
          <div className={`balance-amount ${total >= 0 ? 'positive' : 'negative'}`}>
            ${total.toFixed(2)}
          </div>
        </div>
      </div>

      {/* Formulario */}
      <div className="form-card">
        <form onSubmit={handleSubmit} className="form-grid">
          <input
            name="concepto"
            placeholder="Concepto (ej. Supermercado)"
            value={form.concepto}
            onChange={handleChange}
            required
          />
          <input
            name="monto"
            type="number"
            step="0.01"
            placeholder="Monto"
            value={form.monto}
            onChange={handleChange}
            required
          />
          <select name="tipo" value={form.tipo} onChange={handleChange}>
            <option value="gasto">Gasto</option>
            <option value="ingreso">Ingreso</option>
          </select>
          <input
            name="fecha"
            type="date"
            value={form.fecha}
            onChange={handleChange}
            required
          />
          <button type="submit" className="btn-primary">Agregar</button>
        </form>
      </div>

      {/* Tabla de Movimientos */}
      <div className="table-card">
        <table>
          <thead>
            <tr>
              <th>Concepto</th>
              <th>Monto</th>
              <th>Tipo</th>
              <th>Fecha</th>
              <th>Acción</th>
            </tr>
          </thead>
          <tbody>
            {gastos.length === 0 ? (
              <tr>
                <td colSpan="5" style={{ textAlign: 'center', color: 'var(--text-secondary)' }}>
                  No hay movimientos registrados.
                </td>
              </tr>
            ) : (
              gastos.map((g) => (
                <tr key={g.id}>
                  <td><strong>{g.concepto}</strong></td>
                  <td style={{ fontWeight: '600', color: g.tipo === 'ingreso' ? 'var(--accent-green)' : 'var(--accent-red)' }}>
                    {g.tipo === 'ingreso' ? '+' : '-'}${g.monto.toFixed(2)}
                  </td>
                  <td>
                    <span className={`badge ${g.tipo}`}>{g.tipo}</span>
                  </td>
                  <td>{g.fecha}</td>
                  <td>
                    <button className="btn-delete" onClick={() => handleDelete(g.id)}>Eliminar</button>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default App;