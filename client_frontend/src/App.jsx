import { useState } from 'react'
import Sidebar from './components/SideBar/SideBar'
import PrivateRoutes from './routes/PrivateRoutes'
import PublicRoutes from './routes/PublicRoutes'
import useModalOpen from './hooks/useModalOpen'
import ScrollToTop from './services/ScrollToTop'

import './App.css'

function App () {
  const [modalOpen, handleModal] = useModalOpen()
  const [isAuth, setIsAuth] = useState(false)

  return (
    <div className="app">

      {isAuth
        ? (
          <>
            <Sidebar handleModal={handleModal} modalOpen={modalOpen} />
            <main
              onClick={() => modalOpen && handleModal()}
              className="main">
              <PrivateRoutes />
            </main>
            <ScrollToTop />
          </>
        )
        : (
          <div>
            <button onClick={() => setIsAuth(!isAuth)}>Ir a home</button>
            <PublicRoutes />
          </div>
        )}

    </div>
  )
}
export default App
