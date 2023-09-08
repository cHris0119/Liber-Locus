import { Route, Routes } from 'react-router-dom'
import { Login } from '../auth/pages/Login'
import PrivateRoutes from './PrivateRoutes'

const PublicRoutes = () => {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/registro" element={<h2>Crear cuenta</h2>} />

      <Route path="/*" element={<PrivateRoutes />} />
    </Routes>
  )
}

export default PublicRoutes
