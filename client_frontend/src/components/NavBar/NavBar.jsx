import { linksNav, linksConfig } from "../../services/linksArray";
import { NavLink } from "react-router-dom";
import "./NavBar.css";

// eslint-disable-next-line react/prop-types
const NavBar = ({isOpen}) => {
  return (
    <>
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

      <ul className="navbar">
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
    </>
  );
};

export default NavBar;
