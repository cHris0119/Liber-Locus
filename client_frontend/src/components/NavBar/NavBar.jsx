import "./NavBar.css";
import { NavLink } from "react-router-dom";

// eslint-disable-next-line react/prop-types
const NavBar = ({links, NavOpen, styles}) => {

  // eslint-disable-next-line react/prop-types
  const RenderLinks = ({links}) => {
    return(
      <>
      {/* eslint-disable-next-line react/prop-types */}
      {links.map((link) => (
        <li key={link.label}>
          <NavLink
            className={({ isActive }) => `link${isActive ? ` active` : ``}`}
            to={link.to}
          >
            <div className="linkIcon">{link.icon}</div>
            {NavOpen ? <span>{link.label}</span> : undefined}
          </NavLink>
        </li>
      ))}
      </>
    )
  }

  return (
    <ul className={`navbar ${styles? styles : ''}`}>
      <RenderLinks links={links} />
    </ul>
  );
};

export default NavBar;
