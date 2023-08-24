
import "./SideBar.css";
import useSize from "../../hooks/useSize";
import NavBarContainer from "../NavBarContainer/NavBarContainer";

const Sidebar = () => {
  const isOpen = useSize();


  

  return (
    <aside className='sidebar-container'>
      {isOpen ? <h1 className="title">Liber Locus</h1> : <h1 className="title">LL</h1> }
      
      <NavBarContainer isOpen={isOpen} />
      
      

    </aside>
  );
};

export default Sidebar;
