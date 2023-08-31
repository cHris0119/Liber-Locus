import { useNavigate } from 'react-router-dom'
import './BackButton.css'
import { AiFillBackward } from 'react-icons/ai'

const BackButton = () => {
  const navigate = useNavigate()

  return (
    <>
      <button className='backButton' onClick={() => navigate(-1)} ><AiFillBackward/></button>
    </>
  )
}

export default BackButton
