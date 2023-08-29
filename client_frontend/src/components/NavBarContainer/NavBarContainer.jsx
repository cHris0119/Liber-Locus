import './NavBarContainer.css'

const NavBarContainer = ({ children, handleModal, modalOpen }) => {
  return (
    <div
      className="navbars-container"
      onClick={() => {
        if (modalOpen) {
          handleModal()
        }
      }}
    >
      {children}
    </div>
  )
}

export default NavBarContainer
