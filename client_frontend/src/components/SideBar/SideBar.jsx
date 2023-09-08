import useNavOpen from '../../hooks/useNavOpen'
import { NavBar, AccountButton } from '../'
import { linksNav } from '../../services/linksArray'

import styles from './SideBar.module.css'

export const Sidebar = ({ handleModal, modalOpen }) => {
  const NavOpen = useNavOpen()

  return (

    <aside
      className={styles.sidebarContainer}
      onClick={() => modalOpen && handleModal()}>

      <NavBar links={linksNav} NavOpen={NavOpen} />

      <AccountButton
        NavOpen={NavOpen}
        modalOpen={modalOpen}
        handleModal={handleModal}/>

    </aside>
  )
}
