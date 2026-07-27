import api from "./client";

export const ejecutarCierreMensual = (anio, mes) =>
  api.post(`/api/cierres/mensual?anio=${anio}&mes=${mes}`);

export const listarCierres = (tipo) =>
  api.get("/api/cierres", { params: tipo ? { tipo } : {} });

export const eliminarCierre = (id) =>
  api.delete(`/api/cierres/${id}`);
