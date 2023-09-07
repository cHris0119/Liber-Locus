import Sidebar from './components/SideBar/SideBar'
import RoutesList from './routes/RoutesList'
import useModalOpen from './hooks/useModalOpen'
import ScrollToTop from './services/ScrollToTop'

import './App.css'

function App () {
  const [modalOpen, handleModal] = useModalOpen()

  return (
    <div className="app">

      <Sidebar handleModal={handleModal} modalOpen={modalOpen} />
      <main
        onClick={() => modalOpen && handleModal()}
        className="main">
        <RoutesList />
      </main>
      <ScrollToTop />

    </div>
  )
}
export default App
