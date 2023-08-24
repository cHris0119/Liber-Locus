import "./App.css";
import Sidebar from "./components/SideBar/Sidebar";
import RoutesList from "../RoutesList";

function App() {
  return (
    <div className="app">

      <Sidebar />

      <main className="main">
      <RoutesList />
      </main>
      
    </div>
  );
}
export default App;
