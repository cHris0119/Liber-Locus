import { Navigate, Route, Routes } from 'react-router-dom'
import { Home, Marketplace, PaymentSelection, PostDetail, ShippingDetail, AccountPage } from '../pages'
import { MyAuction, MyPost, PublishBookForm, Sidebar } from '../components'
import useModalOpen from '../hooks/useModalOpen'
import ScrollToTop from '../services/ScrollToTop'

export const BooksRoutes = () => {
  const [modalOpen, handleModal] = useModalOpen()
  return (
    <>

      <Sidebar
        handleModal={handleModal}
        modalOpen={modalOpen} /
      >

      <main
        onClick={() => modalOpen && handleModal()}
        className="main"
      >

        <Routes>
          <Route path="home" element={<Home />} />
          <Route path="marketplace" element={<Marketplace />} />
          <Route path="foro" element={<h1>Foro</h1>} />
          <Route path="reseña" element={<h1>Reseñas</h1>} />
          <Route path="notificaciones" element={<h1>Notificaciones</h1>} />
          <Route path="publicarLibro" element={<PublishBookForm />} />
          <Route path="/detallePost/:postId" element={<PostDetail />} />
          <Route path="/detalleEnvio/:postId" element={<ShippingDetail />} />
          <Route path="/seleccionPago/:postId" element={<PaymentSelection />} />
          <Route path="/perfil/" element={<AccountPage />}>
            <Route path="misPost" element={<MyPost />} />
            <Route path="misSubastas" element={<MyAuction/>} />
          </Route>

          <Route path="/*" element={<Navigate to='home' />} />
        </Routes>

      </main>

      <ScrollToTop />

    </>
  )
}
