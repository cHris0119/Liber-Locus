import "./SideBar.css";
import useNavOpen from "../../hooks/useNavOpen";
import NavBarContainer from "../NavBarContainer/NavBarContainer";
import NavBar from "../NavBar/NavBar";
import AccountButton from "../AccountButton/AccountButton";
import { linksConfig, linksNav } from "../../services/linksArray";

// eslint-disable-next-line react/prop-types
const Sidebar = ({ handleModal, modalOpen }) => {
  const NavOpen = useNavOpen();

  return (
    <aside className="sidebar-container">
      <NavBarContainer handleModal={handleModal} modalOpen={modalOpen}>
        {/* {NavOpen ? (
          <h1 className="title">Liber Locus</h1>
        ) : (
          <h1 className="title">LL</h1>
        )} */}
        <NavBar links={linksNav} NavOpen={NavOpen} />
        <NavBar styles="none" links={linksConfig} NavOpen={NavOpen} />
        <AccountButton
          NavOpen={NavOpen}
          modalOpen={modalOpen}
          handleModal={handleModal}
        />
      </NavBarContainer>
    </aside>
  );
};

export default Sidebar;
