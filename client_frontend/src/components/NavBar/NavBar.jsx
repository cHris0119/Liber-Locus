import { NavLink } from 'react-router-dom'

import styles from './NavBar.module.css'

const RenderLinks = ({ links, NavOpen }) => {
  return (
    <>
      {links.map((link) => (
        <li key={link.label} className={styles['Navbar-li']}>
          <NavLink className={styles.Link}
            to={link.to}
          >
            <div className={styles.Svg}>{link.icon}</div>
            {NavOpen ? <span>{link.label}</span> : undefined}
          </NavLink>
        </li>
      ))}
    </>
  )
}

export const NavBar = ({ links, style, NavOpen }) => {
  return (
    <ul className={`${styles.Navbar} ${style && styles[style]}`}>
      <RenderLinks links={links} NavOpen={NavOpen} />
    </ul>
  )
}
