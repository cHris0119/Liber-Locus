import './AccountButton.css'
import NavBar from '../NavBar/NavBar'
import { linksModal } from '../../services/linksArray'

const AccountButton = ({ NavOpen, modalOpen, handleModal }) => {
  return (
    <div onClick={() => handleModal()} className="account-container">
      <div className="account">
        <div className="account-img"></div>
        {NavOpen ? <p className="userName">Nombre usuario</p> : undefined}
      </div>
      {modalOpen
        ? (
          <div className="modal">
            <NavBar links={linksModal} NavOpen={true} styles="navbar-modal" />
          </div>
        )
        : undefined}
    </div>
  )
}

export default AccountButton
