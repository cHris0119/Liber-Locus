import { linksNav, linksConfig } from "../../services/linksArray";
import "./NavBarContainer.css";
import AccountButton from "../AccountButton/AccountButton";
import NavBar from "../NavBar/NavBar";

// eslint-disable-next-line react/prop-types
const NavBarContainer = ({isOpen}) => {
  return (
    <div className="navbars-container">

      <NavBar links={linksNav} isOpen={isOpen} />

      <NavBar styles='none' links={linksConfig} isOpen={isOpen} />

      <AccountButton isOpen={isOpen} />
    </div>
  );
};

export default NavBarContainer;
