import { NavLink } from 'react-router-dom'
import { LogoutButton } from '../'

import styles from './NavBar.module.css'

const RenderLinks = ({ links, NavOpen }) => {
  return (
    <>

      {links.map((link) => (
        <li key={link.label} className={styles.navbarLi}>

          <NavLink className={styles.link} to={link.to} >

            <div className={styles.svg}>
              {link.icon}
            </div>

            {NavOpen ? <span>{link.label}</span> : undefined}

          </NavLink>

        </li>
      ))}

    </>
  )
}

export const NavBar = ({ links, style, NavOpen, modal = false }) => {
  return (

    <ul className={ style ? style && styles[style] : styles.navbar }>

      <RenderLinks links={links} NavOpen={NavOpen} />

      {modal && <LogoutButton />}
    </ul>

  )
}
