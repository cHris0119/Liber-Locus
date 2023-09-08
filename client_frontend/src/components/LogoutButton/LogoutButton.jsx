import { useNavigate } from 'react-router-dom'
import { FiLogOut } from 'react-icons/fi'

import styles from './LogoutButton.module.css'

export const LogoutButton = () => {
  const navigate = useNavigate()

  const handleLogout = () => {
    navigate('/login')
  }
  return (
    <li className={styles.navbarLi}>

      <button
        className={styles.logoutButton}
        onClick={handleLogout}
      >

        <div className={styles.svg}>
          <FiLogOut />
        </div>
        <span>Salir</span>

      </button>

    </li>
  )
}
