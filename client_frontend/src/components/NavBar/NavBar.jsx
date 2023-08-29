import './NavBar.css'
import { NavLink } from 'react-router-dom'

const NavBar = ({ links, NavOpen, styles }) => {
  const RenderLinks = ({ links }) => {
    return (
      <>
        {/* eslint-disable-next-line react/prop-types */}
        {links.map((link) => (
          <li key={link.label}>
            <NavLink
              className={({ isActive }) => `link${isActive ? ' active' : ''}`}
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
    <ul className={`navbar ${styles || ''}`}>
      <RenderLinks links={links} />
    </ul>
  )
}

export default NavBar
