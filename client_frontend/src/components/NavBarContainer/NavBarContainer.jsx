import "./NavBarContainer.css";


// eslint-disable-next-line react/prop-types
const NavBarContainer = ({ children, handleModal, modalOpen }) => {
  return <div   className="navbars-container"
  onClick={()=> {modalOpen ? handleModal() : null}}
  >{children}</div>;
};

export default NavBarContainer;
