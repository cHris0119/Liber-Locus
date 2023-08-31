import { Route, Routes } from 'react-router-dom'
import Home from '../pages/Home'
import Marketplace from '../pages/Marketplace'
import PostDetail from '../pages/PostDetail/PostDetail'

const RoutesList = () => {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/marketplace" element={<Marketplace />} />
      <Route path="/foro" element={<h1>Foro</h1>} />
      <Route path="/reseña" element={<h1>Reseñas</h1>} />
      <Route path="/notificaciones" element={<h1>Notificaciones</h1>} />
      <Route path="/detallePost/:postId" element={<PostDetail />} />
      <Route path="*" element={<h1>Not found</h1>} />
    </Routes>
  )
}

export default RoutesList
