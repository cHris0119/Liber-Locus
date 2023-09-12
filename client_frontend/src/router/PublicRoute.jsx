import { Navigate } from 'react-router-dom'
import { useContext } from 'react'
import { AuthContext } from '../auth/context/AuthContext'

export const PublicRoute = ({ children }) => {
  //
  const { authState } = useContext(AuthContext)
  return (!authState.logged)
    ? children
    : <Navigate to='/home' />
}
