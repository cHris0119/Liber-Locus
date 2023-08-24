import "./App.css";
import { Route, Routes} from "react-router-dom";
import Home from "./pages/Home";
import Marketplace from "./pages/Marketplace";
import Sidebar from "./components/SideBar/Sidebar";

function App() {
  return (
    <div className="app">

      <Sidebar />
      
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/marketplace" element={<Marketplace />} />
        <Route path="*" element={<h1>Not found</h1>} />
      </Routes>
    </div>
  );
}
export default App;
