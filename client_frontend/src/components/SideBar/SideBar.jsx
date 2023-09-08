import useNavOpen from '../../hooks/useNavOpen'
import { NavBar, AccountButton } from '../'
import { linksConfig, linksNav } from '../../services/linksArray'

import styles from './SideBar.module.css'

export const Sidebar = ({ handleModal, modalOpen }) => {
  const NavOpen = useNavOpen()

  return (
    <aside
      className={styles['Sidebar-container']}
      onClick={() => modalOpen && handleModal()}>

      <NavBar links={linksNav} NavOpen={NavOpen} />
      <NavBar style="None" links={linksConfig} NavOpen={NavOpen} />
      <AccountButton
        NavOpen={NavOpen}
        modalOpen={modalOpen}
        handleModal={handleModal}/>

    </aside>
  )
}
