import { Route, Routes } from 'react-router-dom'
import { PrivateRoute, PublicRoute } from './'
import { AuthRoutes } from '../auth/routes/AuthRoutes'
import { BooksRoutes } from '../books/routes/BooksRoutes'

const AppRouter = () => {
  return (
    <Routes>

      <Route path='/auth/*' element={
        <PublicRoute>
          <AuthRoutes />
        </PublicRoute>
      } />

      <Route path="/*" element={
        <PrivateRoute>
          <BooksRoutes />
        </PrivateRoute>
      } />

    </Routes>
  )
}

export default AppRouter
