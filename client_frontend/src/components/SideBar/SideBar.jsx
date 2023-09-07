import useNavOpen from '../../hooks/useNavOpen'
import NavBar from '../NavBar/NavBar'
import AccountButton from '../AccountButton/AccountButton'
import { linksConfig, linksNav } from '../../services/linksArray'

import styles from './SideBar.module.css'

const Sidebar = ({ handleModal, modalOpen }) => {
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

export default Sidebar
