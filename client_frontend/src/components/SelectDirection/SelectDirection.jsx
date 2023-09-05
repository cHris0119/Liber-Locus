import './SelectDirection.css'
import { NavLink } from 'react-router-dom'

const SelectDirection = () => {
  return (
    <div className='selectDirection-container'>

      <h2>Selecciona tu dirección</h2>

      <div className='direction-container'>
        <div className='direction-main'>
          <header className="direction-header">
            <p>Enviar a domicilio</p>
            <p>$ 3.000 <span>{'>'}</span></p>
          </header>
          <main className="direction-content">
            <p>Dirección falsa 1234</p>
          </main>
        </div>

        <footer className="direction-footer">
          <NavLink className='link-editDirection'>Editar o elegir otro domicilio</NavLink>
        </footer>
      </div>

    </div>
  )
}

export default SelectDirection
