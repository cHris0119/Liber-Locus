import './App.css'
import Sidebar from './components/SideBar/SideBar'
import RoutesList from './routes/RoutesList'
import useModalOpen from './hooks/useModalOpen'

function App () {
  const [modalOpen, handleModal] = useModalOpen()
  return (
    <div className="app">
      <Sidebar handleModal={handleModal} modalOpen={modalOpen} />

      <main
        onClick={() => {
          if (modalOpen) {
            handleModal()
          }
        }}
        className="main"
      >
        <RoutesList />
      </main>
    </div>
  )
}
export default App
