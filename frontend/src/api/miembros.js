import api from "./client";

export const getMiembros = async () => (await api.get("/miembros")).data;
export const getMiembro = async (id) => (await api.get(`/miembros/${id}`)).data;
export const crearMiembro = async (data) => (await api.post("/miembros", data)).data;
export const actualizarMiembro = async (id, data) => (await api.put(`/miembros/${id}`, data)).data;
export const eliminarMiembro = async (id) => (await api.delete(`/miembros/${id}`)).data;
