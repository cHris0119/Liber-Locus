import { Link } from "react-router-dom"

const Sidebar = () => {
  return (
    <aside>
      <h1>Liber Locus</h1>
      <ul>
        <li><Link to='/' >Home</Link></li>
        <li><Link to='/marketplace' >Marketplace</Link></li>
      </ul>

      </aside>
  )
}

export default Sidebar