import { Navigate, Route, Routes } from 'react-router-dom'
import { Login, Register, DirectionRegister, RecuperarContra } from '../pages'

export const AuthRoutes = () => {
  return (
        <Routes>
          <Route path="login" element={<Login />} />
          <Route path="registro" element={<Register />} />
          <Route path="direccionRegistro" element={<DirectionRegister />} />
          <Route path="recuperarContra" element={<RecuperarContra />} />
          <Route path="/*" element={<Navigate to='login' />} />
        </Routes>
  )
}
