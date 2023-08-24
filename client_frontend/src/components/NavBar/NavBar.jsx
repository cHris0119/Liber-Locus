import "./NavBar.css";
import { NavLink } from "react-router-dom";

// eslint-disable-next-line react/prop-types
const NavBar = ({links, isOpen, styles}) => {
  return (
    <ul className={`navbar ${styles? styles : ''}`}>
      {/* eslint-disable-next-line react/prop-types */}
      {links.map((link) => (
        <li key={link.label}>
          <NavLink
            className={({ isActive }) => `link${isActive ? ` active` : ``}`}
            to={link.to}
          >
            <div className="linkIcon">{link.icon}</div>
            {isOpen ? <span>{link.label}</span> : undefined}
          </NavLink>
        </li>
      ))}
    </ul>
  );
};

export default NavBar;
