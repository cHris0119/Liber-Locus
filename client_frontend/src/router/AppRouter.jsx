import { Route, Routes } from 'react-router-dom'
import { PrivateRoute, PublicRoute, BooksRoutes, AuthRoutes } from './'

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
