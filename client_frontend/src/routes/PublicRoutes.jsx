import { Route, Routes } from 'react-router-dom'

const PublicRoutes = () => {
  return (
    <Routes>
      <Route path="/" element={<h1>Hola</h1>} />
      <Route path="/registro" element={<h2>Crear cuenta</h2>} />
      <Route path="*" element={<h1>Not found</h1>} />
    </Routes>
  )
}

export default PublicRoutes
