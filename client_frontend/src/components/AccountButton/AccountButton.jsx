import "./AccountButton.css";
import NavBar from "../NavBar/NavBar";
import { linksModal } from "../../services/linksArray";


// eslint-disable-next-line react/prop-types
const AccountButton = ({isOpen}) => {
  return (
    <div className="account-container">
      <div className="account">
        <div className="account-img"></div>

        {isOpen 
          ? <p className="userName">Nombre usuario</p>
          : undefined
        }
        
      </div>

      <div className="modal">
        <NavBar links={linksModal} isOpen={true} styles='navbar-modal' />
      </div>
    </div>
  );
};

export default AccountButton;
