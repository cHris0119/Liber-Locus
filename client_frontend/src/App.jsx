import { AuthProvider } from './auth/'
import AppRouter from './router/AppRouter'

import './App.css'

export default function App () {
  return (
    <AuthProvider>

      <AppRouter />

    </AuthProvider>
  )
}
