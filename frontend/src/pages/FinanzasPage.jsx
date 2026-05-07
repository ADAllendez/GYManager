import React, { useEffect, useState } from "react";
import Layout from "../components/Layout";
import api from "../api/client";

const CARD = { backgroundColor: "#1a1a1a", border: "1px solid #2a2a2a", borderRadius: "12px", padding: "24px" };

const MESES_ES = ["Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"];

function StatCard({ label, value, color, icon, sub }) {
  return (
    <div style={CARD}>
      <div style={{ display: "flex", alignItems: "flex-start", justifyContent: "space-between" }}>
        <div>
          <p style={{ fontSize: 12, color: "#6b7280", marginBottom: 6, fontWeight: 600, textTransform: "uppercase", letterSpacing: "0.05em" }}>{label}</p>
          <p style={{ fontSize: 28, fontWeight: 800, color: color || "#fff", margin: 0 }}>
            ${Number(value || 0).toLocaleString("es-AR")}
          </p>
          {sub && <p style={{ fontSize: 12, color: "#4b5563", marginTop: 4 }}>{sub}</p>}
        </div>
        <div style={{ width: 40, height: 40, borderRadius: 10, backgroundColor: `${color}22`, display: "flex", alignItems: "center", justifyContent: "center" }}>
          <span style={{ color }}>{icon}</span>
        </div>
      </div>
    </div>
  );
}

export default function FinanzasPage() {
  const hoy = new Date();
  const [anio, setAnio]       = useState(hoy.getFullYear());
  const [mes, setMes]         = useState(hoy.getMonth() + 1); // 1-12
  const [datos, setDatos]     = useState(null);
  const [cargando, setCarg]   = useState(true);
  const [error, setError]     = useState("");

  useEffect(() => { cargar(anio, mes); }, [anio, mes]); // eslint-disable-line

  async function cargar(a, m) {
    setCarg(true); setError("");
    try {
      const res = await api.get(`/api/finanzas/dashboard?anio=${a}&mes=${m}`);
      setDatos(res.data);
    } catch (e) {
      setError("Error al cargar los datos financieros.");
      console.error(e);
    } finally { setCarg(false); }
  }

  function irAnterior() {
    if (mes === 1) { setMes(12); setAnio(a => a - 1); }
    else setMes(m => m - 1);
  }
  function irSiguiente() {
    const ahora = new Date();
    if (anio === ahora.getFullYear() && mes === ahora.getMonth() + 1) return; // no ir al futuro
    if (mes === 12) { setMes(1); setAnio(a => a + 1); }
    else setMes(m => m + 1);
  }

  const esMesActual = anio === hoy.getFullYear() && mes === hoy.getMonth() + 1;
  const enPositivo  = datos && datos.ganancia_neta >= 0;

  return (
    <Layout>
      {/* Header */}
      <div style={{ display: "flex", alignItems: "flex-start", justifyContent: "space-between", marginBottom: 24 }}>
        <div>
          <h1 style={{ fontSize: 22, fontWeight: 800, color: "#fff", margin: 0 }}>Finanzas</h1>
          <p style={{ fontSize: 13, color: "#6b7280", marginTop: 4 }}>Resumen financiero — solo visible para root</p>
        </div>
        <button onClick={() => cargar(anio, mes)}
          style={{ display: "flex", alignItems: "center", gap: 6, padding: "8px 16px", borderRadius: 8, backgroundColor: "#1a1a1a", border: "1px solid #2a2a2a", color: "#9ca3af", fontSize: 13, fontWeight: 600, cursor: "pointer" }}
          onMouseEnter={e => e.currentTarget.style.borderColor = "#f97316"}
          onMouseLeave={e => e.currentTarget.style.borderColor = "#2a2a2a"}>
          <svg style={{ width: 15, height: 15 }} fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" d="M16.023 9.348h4.992v-.001M2.985 19.644v-4.992m0 0h4.992m-4.993 0l3.181 3.183a8.25 8.25 0 0013.803-3.7M4.031 9.865a8.25 8.25 0 0113.803-3.7l3.181 3.182m0-4.991v4.99" />
          </svg>
          Actualizar
        </button>
      </div>

      {/* Navegador de meses */}
      <div style={{ display: "flex", alignItems: "center", gap: 12, marginBottom: 20 }}>
        <button onClick={irAnterior} style={{ width: 32, height: 32, borderRadius: "50%", backgroundColor: "#1a1a1a", border: "1px solid #2a2a2a", color: "#9ca3af", cursor: "pointer", display: "flex", alignItems: "center", justifyContent: "center" }}
          onMouseEnter={e => { e.currentTarget.style.borderColor="#f97316"; e.currentTarget.style.color="#f97316"; }}
          onMouseLeave={e => { e.currentTarget.style.borderColor="#2a2a2a"; e.currentTarget.style.color="#9ca3af"; }}>
          <svg style={{ width: 14, height: 14 }} fill="none" stroke="currentColor" strokeWidth={2.5} viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 19.5L8.25 12l7.5-7.5" />
          </svg>
        </button>

        <span style={{ padding: "5px 16px", borderRadius: 999, backgroundColor: "#f9731622", color: "#f97316", fontSize: 13, fontWeight: 700, letterSpacing: "0.04em", minWidth: 140, textAlign: "center" }}>
          📅 {MESES_ES[mes - 1]} {anio}
          {esMesActual && <span style={{ marginLeft: 6, fontSize: 10, opacity: 0.7 }}>· actual</span>}
        </span>

        <button onClick={irSiguiente} disabled={esMesActual}
          style={{ width: 32, height: 32, borderRadius: "50%", backgroundColor: "#1a1a1a", border: "1px solid #2a2a2a", color: esMesActual ? "#2a2a2a" : "#9ca3af", cursor: esMesActual ? "not-allowed" : "pointer", display: "flex", alignItems: "center", justifyContent: "center" }}
          onMouseEnter={e => { if (!esMesActual) { e.currentTarget.style.borderColor="#f97316"; e.currentTarget.style.color="#f97316"; }}}
          onMouseLeave={e => { e.currentTarget.style.borderColor="#2a2a2a"; e.currentTarget.style.color= esMesActual ? "#2a2a2a" : "#9ca3af"; }}>
          <svg style={{ width: 14, height: 14 }} fill="none" stroke="currentColor" strokeWidth={2.5} viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" d="M8.25 4.5l7.5 7.5-7.5 7.5" />
          </svg>
        </button>
      </div>

      {cargando ? (
        <div style={{ display: "flex", justifyContent: "center", alignItems: "center", height: 200 }}>
          <div style={{ width: 32, height: 32, borderRadius: "50%", border: "3px solid #f97316", borderTopColor: "transparent", animation: "spin 0.7s linear infinite" }} />
        </div>
      ) : error ? (
        <div style={{ padding: 20, borderRadius: 10, backgroundColor: "#ef444415", border: "1px solid #ef444433", color: "#ef4444", fontSize: 14 }}>{error}</div>
      ) : datos && (
        <>
          {/* Cards principales */}
          <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: 16, marginBottom: 20 }}>
            <StatCard label="Ingresos del mes" value={datos.ingresos_totales} color="#22c55e" sub="Membresías cobradas"
              icon={<svg style={{ width: 20, height: 20 }} fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M2.25 18L9 11.25l4.306 4.307a11.95 11.95 0 015.814-5.519l2.74-1.22m0 0l-5.94-2.28m5.94 2.28l-2.28 5.941" /></svg>} />
            <StatCard label="Gastos en insumos" value={datos.gastos_insumos} color="#f97316" sub="Equipamiento, servicios, etc."
              icon={<svg style={{ width: 20, height: 20 }} fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M2.25 6L9 12.75l4.286-4.286a11.948 11.948 0 014.306 6.43l.776 2.898m0 0l3.182-5.511m-3.182 5.51l-5.511-3.181" /></svg>} />
            <StatCard label="Sueldos pagados" value={datos.pago_instructores} color="#a78bfa" sub="Trabajadores e instructores"
              icon={<svg style={{ width: 20, height: 20 }} fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M15.75 6a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0zM4.501 20.118a7.5 7.5 0 0114.998 0" /></svg>} />
          </div>

          {/* Card ganancia neta */}
          <div style={{ ...CARD, border: `1px solid ${enPositivo ? "#22c55e44" : "#ef444444"}`, background: enPositivo ? "linear-gradient(135deg, #1a1a1a 60%, #16a34a10)" : "linear-gradient(135deg, #1a1a1a 60%, #ef444410)" }}>
            <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between" }}>
              <div>
                <p style={{ fontSize: 12, color: "#6b7280", fontWeight: 600, textTransform: "uppercase", letterSpacing: "0.05em", marginBottom: 8 }}>Ganancia neta del mes</p>
                <p style={{ fontSize: 40, fontWeight: 800, color: enPositivo ? "#22c55e" : "#ef4444", margin: 0 }}>
                  {enPositivo ? "+" : ""}${Number(datos.ganancia_neta).toLocaleString("es-AR")}
                </p>
                <p style={{ fontSize: 13, marginTop: 6, color: enPositivo ? "#16a34a" : "#dc2626" }}>
                  {enPositivo ? "✓ El gym está en positivo este mes" : "⚠ El gym está en negativo este mes — revisá los gastos"}
                </p>
              </div>
              <div style={{ width: 64, height: 64, borderRadius: "50%", backgroundColor: enPositivo ? "#22c55e15" : "#ef444415", border: `2px solid ${enPositivo ? "#22c55e33" : "#ef444433"}`, display: "flex", alignItems: "center", justifyContent: "center" }}>
                <svg style={{ width: 30, height: 30, color: enPositivo ? "#22c55e" : "#ef4444" }} fill="none" stroke="currentColor" strokeWidth={1.8} viewBox="0 0 24 24">
                  {enPositivo
                    ? <path strokeLinecap="round" strokeLinejoin="round" d="M12 6v12m-3-2.818l.879.659c1.171.879 3.07.879 4.242 0 1.172-.879 1.172-2.303 0-3.182C13.536 12.219 12.768 12 12 12c-.725 0-1.45-.22-2.003-.659-1.106-.879-1.106-2.303 0-3.182s2.9-.879 4.006 0l.415.33M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                    : <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126zM12 15.75h.007v.008H12v-.008z" />
                  }
                </svg>
              </div>
            </div>
            <div style={{ marginTop: 20, paddingTop: 16, borderTop: "1px solid #2a2a2a", display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: 12 }}>
              {[
                { label: "Total ingresos", val: datos.ingresos_totales, color: "#22c55e" },
                { label: "Total egresos", val: datos.gastos_insumos + datos.pago_instructores, color: "#ef4444" },
                { label: "Balance", val: datos.ganancia_neta, color: enPositivo ? "#22c55e" : "#ef4444" },
              ].map(({ label, val, color }) => (
                <div key={label} style={{ textAlign: "center", padding: "10px 0" }}>
                  <p style={{ fontSize: 11, color: "#6b7280", margin: "0 0 4px", fontWeight: 600, textTransform: "uppercase" }}>{label}</p>
                  <p style={{ fontSize: 16, fontWeight: 700, color, margin: 0 }}>${Number(val).toLocaleString("es-AR")}</p>
                </div>
              ))}
            </div>
          </div>
        </>
      )}
    </Layout>
  );
}
