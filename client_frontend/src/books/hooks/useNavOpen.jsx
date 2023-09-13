import { useEffect, useState } from 'react'

const useNavOpen = () => {
  const [NavOpen, setNavOpen] = useState(true)

  const handleResize = () => {
    if (window.innerWidth < 1265) {
      setNavOpen(false)
    } else {
      setNavOpen(true)
    }
  }

  useEffect(() => {
    handleResize()
  }, [])

  window.addEventListener('resize', handleResize)

  return NavOpen
}

export default useNavOpen
