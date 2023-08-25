import "./App.css";
import Sidebar from "./components/SideBar/SideBar";
import RoutesList from "../RoutesList";
import useModalOpen from "./hooks/useModalOpen";

function App() {
  const [modalOpen, handleModal] = useModalOpen();

  return (
    <div className="app">
      <Sidebar handleModal={handleModal} modalOpen={modalOpen} />

      <main
        onClick={() => {
          modalOpen ? handleModal() : null;
        }}
        className="main"
      >
        <RoutesList />
      </main>
    </div>
  );
}
export default App;
