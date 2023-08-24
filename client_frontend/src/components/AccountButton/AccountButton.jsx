import "./AccountButton.css";

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
    </div>
  );
};

export default AccountButton;
