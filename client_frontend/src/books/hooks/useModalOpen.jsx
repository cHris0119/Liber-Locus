import useNavOpen from './useNavOpen'
import { useState, useEffect } from 'react'

const useModalOpen = () => {
  const [modalOpen, setModalOpen] = useState(false)
  const NavOpen = useNavOpen()

  const handleModal = () => {
    setModalOpen(!modalOpen)
  }

  useEffect(() => {
    setModalOpen(false)
  }, [NavOpen])

  return [modalOpen, handleModal]
}

export default useModalOpen
