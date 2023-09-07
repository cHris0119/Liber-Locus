import { Route, Routes } from 'react-router-dom'

import Home from '../pages/Home'
import Marketplace from '../pages/Marketplace'
import PostDetail from '../pages/PostDetail'
import ShippingDetail from '../pages/ShippingDetail'
import PaymentSelection from '../pages/PaymentSelection'
import PublishBookForm from '../components/PublishBookForm/PublishBookForm'

const PrivateRoutes = () => {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/marketplace" element={<Marketplace />} />
      <Route path="/foro" element={<h1>Foro</h1>} />
      <Route path="/reseña" element={<h1>Reseñas</h1>} />
      <Route path="/notificaciones" element={<h1>Notificaciones</h1>} />
      <Route path="/publicarLibro" element={<PublishBookForm />} />
      <Route path="/detallePost/:postId" element={<PostDetail />} />
      <Route path="/detalleEnvio/:postId" element={<ShippingDetail />} />
      <Route path="/seleccionPago/:postId" element={<PaymentSelection />} />
      <Route path="*" element={<h1>Not found</h1>} />
    </Routes>
  )
}

export default PrivateRoutes
