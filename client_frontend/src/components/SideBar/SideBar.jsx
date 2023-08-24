
import "./SideBar.css";
import NavBar from "../NavBar/NavBar";
import useSize from "../../hooks/useSize";

const Sidebar = () => {
  const isOpen = useSize();


  

  return (
    <aside className='sidebar-container'>
      {isOpen ? <h1 className="title">Liber Locus</h1> : <h1 className="title">LL</h1> }
      
      <NavBar isOpen={isOpen} />
      
      

    </aside>
  );
};

export default Sidebar;
