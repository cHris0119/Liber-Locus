import { linksNav, linksConfig } from "../../services/linksArray";
import { NavLink } from "react-router-dom";
import "./NavBar.css";
import AccountButton from "../AccountButton/AccountButton";

// eslint-disable-next-line react/prop-types
const NavBar = ({isOpen}) => {
  return (
    <div className="navbars-container">
      <ul className="navbar">
        {linksNav.map((link) => (
          <li key={link.label}>
            <NavLink className={({isActive})=>`link${isActive?` active`:``}`} to={link.to}>
              <div className="linkIcon">{link.icon}</div>
                {isOpen 
                ? <span>{link.label}</span>
                : undefined
                }
              
            </NavLink>
          </li>
        ))}
      </ul>

      <ul className="navbar none">
        {linksConfig.map((link) => (
          <li key={link.label}>
            <NavLink className="link" to={link.to}>
              <div className="linkIcon">{link.icon}</div>
                {isOpen 
                ? <span>{link.label}</span>
                : undefined
                }
            </NavLink>
          </li>
        ))}
      </ul>

      <AccountButton isOpen={isOpen} />
    </div>
  );
};

export default NavBar;
