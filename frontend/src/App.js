import { BrowserRouter, Routes, Route } from "react-router-dom";
import HomePage from "./pages/HomePage";
import MiembrosPage from "./pages/MiembrosPage";
import DisciplinasPage from "./pages/DisciplinasPage";
import InstructoresPage from "./pages/InstructoresPage";
import MembresiaPage from "./pages/MembresiaPage";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/"              element={<HomePage />} />
        <Route path="/miembros"      element={<MiembrosPage />} />
        <Route path="/disciplinas"   element={<DisciplinasPage />} />
        <Route path="/instructores"  element={<InstructoresPage />} />
        <Route path="/membresias"    element={<MembresiaPage />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
