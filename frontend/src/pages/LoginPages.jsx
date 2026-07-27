import React, {useState, useContext} from "react";
import {AuthContext} from "../context/AuthContext";
import {useNavigate} from "react-router-dom";
import api from "../api/client";

export default function LoginPages() {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");
    const {login} = useContext(AuthContext);
    const navigate = useNavigate();

    // ── Estado del flujo "Olvidé mi contraseña" ──
    const [paso, setPaso] = useState(0);
    // 0 = login normal, 1 = pedir PIN, 2 = procesando, 3 = éxito
    const [resetData, setResetData] = useState(null);
    const [resetError, setResetError] = useState("");
    const [pin, setPin] = useState("");

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError("");
        try {
            await login(username, password);
            navigate("/");
        } catch (err) {
            setError("Usuario o contraseña incorrectos");
        }
    }

    const hacerReset = async (e) => {
        e.preventDefault();
        if (!pin.trim()) return setResetError("Ingresá el PIN de seguridad.");
        setPaso(2);
        setResetError("");
        try {
            const res = await api.post("/api/usuarios/reset-root", { pin: pin.trim() });
            setResetData(res.data);
            setPaso(3);
        } catch (err) {
            setResetError(err?.response?.data?.detail || "Error al restablecer la contraseña.");
            setPaso(1);
        }
    };

    const volverAlLogin = () => {
        setPaso(0);
        setResetData(null);
        setResetError("");
        setError("");
        setPin("");
    };

    return (
    <div className="min-h-screen flex items-center justify-center bg-[#0f0f0f]">
      <div className="bg-[#111111] p-8 rounded-xl border border-[#2a2a2a] w-96" style={{ position: "relative", overflow: "hidden" }}>

        {/* Header — siempre visible */}
        <div className="flex items-center gap-3 mb-8 justify-center">
          <div className="w-10 h-10 rounded-lg flex items-center justify-center bg-orange-500">
            <svg className="w-6 h-6 text-white" fill="currentColor" viewBox="0 0 24 24">
              <path d="M20.57 14.86L22 13.43 20.57 12 17 15.57 8.43 7 12 3.43 10.57 2 9.14 3.43 7.71 2 5.57 4.14 4.14 2.71 2.71 4.14l1.43 1.43L2 7.71l1.43 1.43L2 10.57 3.43 12 7 8.43 15.57 17 12 20.57 13.43 22l1.43-1.43L16.29 22l2.14-2.14 1.43 1.43 1.43-1.43-1.43-1.43L22 16.29l-1.43-1.43z" />
            </svg>
          </div>
          <h1 className="text-2xl font-bold text-white">GYM Manager</h1>
        </div>

        {/* ══════ PASO 0: Login normal ══════ */}
        {paso === 0 && (
          <>
            {error && <p className="text-red-400 bg-red-500/20 p-3 rounded mb-4 text-sm text-center">{error}</p>}

            <form onSubmit={handleSubmit} className="flex flex-col gap-4">
              <div>
                <label className="text-gray-400 text-xs font-semibold mb-1 block">Usuario</label>
                <input 
                  className="w-full bg-[#1a1a1a] border border-[#2a2a2a] text-white p-2.5 rounded outline-none focus:border-orange-500 transition"
                  value={username} onChange={e => setUsername(e.target.value)} required 
                />
              </div>
              <div>
                <label className="text-gray-400 text-xs font-semibold mb-1 block">Contraseña</label>
                <input 
                  type="password"
                  className="w-full bg-[#1a1a1a] border border-[#2a2a2a] text-white p-2.5 rounded outline-none focus:border-orange-500 transition"
                  value={password} onChange={e => setPassword(e.target.value)} required 
                />
              </div>
              <button type="submit" className="w-full bg-orange-500 hover:bg-orange-600 text-white font-bold p-3 rounded mt-2 transition">
                Iniciar Sesión
              </button>
            </form>

            {/* Link "He olvidado mi contraseña" */}
            <div style={{ textAlign: "center", marginTop: 16 }}>
              <button
                type="button"
                onClick={() => { setPaso(1); setError(""); }}
                style={{
                  background: "none", border: "none", cursor: "pointer",
                  color: "#6b7280", fontSize: 13, textDecoration: "none",
                  transition: "color 0.15s",
                }}
                onMouseEnter={e => e.currentTarget.style.color = "#f97316"}
                onMouseLeave={e => e.currentTarget.style.color = "#6b7280"}
              >
                ¿Olvidaste tu contraseña?
              </button>
            </div>
          </>
        )}

        {/* ══════ PASO 1: Pedir PIN de seguridad ══════ */}
        {paso === 1 && (
          <div style={{ textAlign: "center" }}>
            {/* Ícono de candado */}
            <div style={{
              width: 56, height: 56, borderRadius: "50%", margin: "0 auto 16px",
              backgroundColor: "#f9731622", display: "flex", alignItems: "center", justifyContent: "center",
            }}>
              <svg style={{ width: 28, height: 28, color: "#f97316" }} fill="none" stroke="currentColor" strokeWidth={1.8} viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" d="M16.5 10.5V6.75a4.5 4.5 0 10-9 0v3.75m-.75 11.25h10.5a2.25 2.25 0 002.25-2.25v-6.75a2.25 2.25 0 00-2.25-2.25H6.75a2.25 2.25 0 00-2.25 2.25v6.75a2.25 2.25 0 002.25 2.25z" />
              </svg>
            </div>

            <h2 style={{ color: "#fff", fontSize: 16, fontWeight: 700, marginBottom: 8 }}>
              Restablecer contraseña
            </h2>
            <p style={{ color: "#9ca3af", fontSize: 13, lineHeight: 1.5, marginBottom: 16 }}>
              Ingresá el <strong style={{ color: "#f97316" }}>PIN de seguridad</strong> para restablecer la contraseña del administrador.
            </p>

            {resetError && (
              <div style={{ marginBottom: 14, padding: "8px 12px", borderRadius: 7, backgroundColor: "#ef444422", color: "#ef4444", fontSize: 12, border: "1px solid #ef444433" }}>
                {resetError}
              </div>
            )}

            <form onSubmit={hacerReset}>
              <input
                type="password"
                value={pin}
                onChange={e => setPin(e.target.value)}
                placeholder="PIN de seguridad"
                autoFocus
                style={{
                  width: "100%", backgroundColor: "#1a1a1a", border: "1px solid #2a2a2a",
                  color: "#fff", padding: "12px 14px", borderRadius: 8, fontSize: 16,
                  textAlign: "center", letterSpacing: "6px", fontWeight: 700,
                  outline: "none", boxSizing: "border-box", marginBottom: 16,
                }}
                onFocus={e => e.currentTarget.style.borderColor = "#f97316"}
                onBlur={e => e.currentTarget.style.borderColor = "#2a2a2a"}
              />

              <div style={{ display: "flex", gap: 10 }}>
                <button
                  type="button"
                  onClick={volverAlLogin}
                  style={{
                    flex: 1, padding: "10px", borderRadius: 8,
                    border: "1px solid #2a2a2a", backgroundColor: "#1a1a1a",
                    color: "#9ca3af", fontSize: 13, fontWeight: 600, cursor: "pointer",
                    transition: "all 0.15s",
                  }}
                  onMouseEnter={e => { e.currentTarget.style.backgroundColor = "#222"; e.currentTarget.style.color = "#fff"; }}
                  onMouseLeave={e => { e.currentTarget.style.backgroundColor = "#1a1a1a"; e.currentTarget.style.color = "#9ca3af"; }}
                >
                  Cancelar
                </button>
                <button
                  type="submit"
                  style={{
                    flex: 1, padding: "10px", borderRadius: 8,
                    border: "none", backgroundColor: "#f97316",
                    color: "#fff", fontSize: 13, fontWeight: 700, cursor: "pointer",
                    transition: "all 0.15s",
                  }}
                  onMouseEnter={e => e.currentTarget.style.backgroundColor = "#ea580c"}
                  onMouseLeave={e => e.currentTarget.style.backgroundColor = "#f97316"}
                >
                  Restablecer
                </button>
              </div>
            </form>

            <p style={{ fontSize: 11, color: "#4b5563", marginTop: 14, lineHeight: 1.4 }}>
              Si no conocés el PIN, contactá al administrador del sistema.
            </p>
          </div>
        )}

        {/* ══════ PASO 2: Procesando ══════ */}
        {paso === 2 && (
          <div style={{ textAlign: "center", padding: "30px 0" }}>
            <div style={{
              width: 36, height: 36, borderRadius: "50%", margin: "0 auto 16px",
              border: "3px solid #f97316", borderTopColor: "transparent",
              animation: "spin 0.7s linear infinite",
            }} />
            <p style={{ color: "#9ca3af", fontSize: 13 }}>Restableciendo contraseña...</p>
          </div>
        )}

        {/* ══════ PASO 3: Éxito ══════ */}
        {paso === 3 && resetData && (
          <div style={{ textAlign: "center" }}>
            {/* Ícono de éxito */}
            <div style={{
              width: 56, height: 56, borderRadius: "50%", margin: "0 auto 16px",
              backgroundColor: "#22c55e22", display: "flex", alignItems: "center", justifyContent: "center",
            }}>
              <svg style={{ width: 28, height: 28, color: "#22c55e" }} fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>

            <h2 style={{ color: "#fff", fontSize: 16, fontWeight: 700, marginBottom: 8 }}>
              ¡Contraseña restablecida!
            </h2>
            <p style={{ color: "#9ca3af", fontSize: 13, marginBottom: 16 }}>
              Usá estas credenciales para iniciar sesión:
            </p>

            {/* Tarjeta con las credenciales */}
            <div style={{
              backgroundColor: "#0f0f0f", border: "1px solid #2a2a2a", borderRadius: 10,
              padding: "14px 18px", marginBottom: 20, textAlign: "left",
            }}>
              <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 8 }}>
                <span style={{ color: "#6b7280", fontSize: 12, fontWeight: 600 }}>Usuario</span>
                <span style={{ color: "#f97316", fontSize: 13, fontWeight: 700, fontFamily: "monospace" }}>{resetData.username}</span>
              </div>
              <div style={{ display: "flex", justifyContent: "space-between" }}>
                <span style={{ color: "#6b7280", fontSize: 12, fontWeight: 600 }}>Contraseña</span>
                <span style={{ color: "#f97316", fontSize: 13, fontWeight: 700, fontFamily: "monospace" }}>{resetData.default_password}</span>
              </div>
            </div>

            <p style={{ color: "#6b7280", fontSize: 11, marginBottom: 16, lineHeight: 1.4 }}>
              ⚠️ Recordá cambiar la contraseña desde tu perfil después de iniciar sesión.
            </p>

            <button
              onClick={volverAlLogin}
              style={{
                width: "100%", padding: "10px", borderRadius: 8,
                border: "none", backgroundColor: "#f97316",
                color: "#fff", fontSize: 13, fontWeight: 700, cursor: "pointer",
                transition: "all 0.15s",
              }}
              onMouseEnter={e => e.currentTarget.style.backgroundColor = "#ea580c"}
              onMouseLeave={e => e.currentTarget.style.backgroundColor = "#f97316"}
            >
              Volver al login
            </button>
          </div>
        )}
      </div>
    </div>
  );
}