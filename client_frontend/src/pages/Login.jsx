import React from 'react'
import { NavLink } from 'react-router-dom'

const Login = ({ setLoggedIn }) => {
  return (
    <div>Login

      <NavLink to={'/home'}>
        <button onClick={() => setLoggedIn(true)}>Iniciar sesion</button>
      </NavLink>
    </div>

  )
}

export default Login
