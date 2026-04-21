import React from "react";
import { NavLink } from "react-router-dom";

const navItems = [
  {
    to: "/",
    label: "Dashboard",
    icon: (
      <svg className="w-5 h-5" fill="none" stroke="currentColor" strokeWidth={1.8} viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" d="M3 12l9-9 9 9M4.5 10.5V19a1.5 1.5 0 001.5 1.5h4.5V15h3v5.5H18A1.5 1.5 0 0019.5 19v-8.5" />
      </svg>
    ),
  },
  {
    to: "/miembros",
    label: "Miembros",
    icon: (
      <svg className="w-5 h-5" fill="none" stroke="currentColor" strokeWidth={1.8} viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" d="M17 20h5v-2a4 4 0 00-5.197-3.794M9 20H4v-2a4 4 0 015.197-3.794M15 11a4 4 0 11-8 0 4 4 0 018 0zm6 0a3 3 0 11-6 0 3 3 0 016 0z" />
      </svg>
    ),
  },
  {
    to: "/membresias",
    label: "Membresías",
    icon: (
      <svg className="w-5 h-5" fill="none" stroke="currentColor" strokeWidth={1.8} viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" d="M15 5v2m0 4v2m0 4v2M5 5a2 2 0 00-2 2v3a2 2 0 110 4v3a2 2 0 002 2h14a2 2 0 002-2v-3a2 2 0 110-4V7a2 2 0 00-2-2H5z" />
      </svg>
    ),
  },
  {
    to: "/disciplinas",
    label: "Disciplinas",
    icon: (
      <svg className="w-5 h-5" fill="none" stroke="currentColor" strokeWidth={1.8} viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" d="M3.75 13.5l10.5-11.25L12 10.5h8.25L9.75 21.75 12 13.5H3.75z" />
      </svg>
    ),
  },
  {
    to: "/instructores",
    label: "Instructores",
    icon: (
      <svg className="w-5 h-5" fill="none" stroke="currentColor" strokeWidth={1.8} viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 6a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0zM4.501 20.118a7.5 7.5 0 0114.998 0A17.933 17.933 0 0112 21.75c-2.676 0-5.216-.584-7.499-1.632z" />
      </svg>
    ),
  },
];

function Layout({ children }) {
  return (
    <div className="min-h-screen flex" style={{ backgroundColor: "#0f0f0f" }}>
      {/* SIDEBAR */}
      <aside className="w-64 flex flex-col" style={{ backgroundColor: "#111111", borderRight: "1px solid #2a2a2a" }}>
        {/* Logo */}
        <div className="px-6 py-5" style={{ borderBottom: "1px solid #2a2a2a" }}>
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-lg flex items-center justify-center" style={{ backgroundColor: "#f97316" }}>
              <svg className="w-5 h-5 text-white" fill="currentColor" viewBox="0 0 24 24">
                <path d="M20.57 14.86L22 13.43 20.57 12 17 15.57 8.43 7 12 3.43 10.57 2 9.14 3.43 7.71 2 5.57 4.14 4.14 2.71 2.71 4.14l1.43 1.43L2 7.71l1.43 1.43L2 10.57 3.43 12 7 8.43 15.57 17 12 20.57 13.43 22l1.43-1.43L16.29 22l2.14-2.14 1.43 1.43 1.43-1.43-1.43-1.43L22 16.29l-1.43-1.43z" />
              </svg>
            </div>
            <div>
              <h1 className="font-bold text-white text-lg leading-tight">GYM Manager</h1>
              <p className="text-xs" style={{ color: "#6b7280" }}>Panel de control</p>
            </div>
          </div>
        </div>

        {/* Navegación */}
        <nav className="flex-1 px-3 py-4">
          <p className="mb-3 px-3 text-xs font-semibold uppercase tracking-widest" style={{ color: "#4b5563" }}>
            Menú principal
          </p>
          <ul className="space-y-1">
            {navItems.map(({ to, label, icon }) => (
              <li key={to}>
                <NavLink
                  to={to}
                  end={to === "/"}
                  className={({ isActive }) =>
                    `flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all duration-150 ${
                      isActive
                        ? "text-white"
                        : "hover:text-white"
                    }`
                  }
                  style={({ isActive }) => ({
                    backgroundColor: isActive ? "#f97316" : "transparent",
                    color: isActive ? "#ffffff" : "#9ca3af",
                  })}
                  onMouseEnter={(e) => {
                    if (!e.currentTarget.classList.contains("active")) {
                      e.currentTarget.style.backgroundColor = "#1f1f1f";
                    }
                  }}
                  onMouseLeave={(e) => {
                    if (e.currentTarget.getAttribute("aria-current") !== "page") {
                      e.currentTarget.style.backgroundColor = "transparent";
                    }
                  }}
                >
                  {icon}
                  {label}
                </NavLink>
              </li>
            ))}
          </ul>
        </nav>

        {/* Footer del sidebar */}
        <div className="px-6 py-4" style={{ borderTop: "1px solid #2a2a2a" }}>
          <p className="text-xs" style={{ color: "#4b5563" }}>© 2025 GYM Manager</p>
        </div>
      </aside>

      {/* CONTENIDO PRINCIPAL */}
      <main className="flex-1 overflow-auto px-6 py-6" style={{ backgroundColor: "#0f0f0f" }}>
        {children}
      </main>
    </div>
  );
}

export default Layout;
