import HeroSection from '../components/HeroSection/HeroSection'
import LastPosts from '../components/LastPosts/LastPosts'
import TrendForum from '../components/TrendForum/TrendForum'
import Suscriptions from '../components/Suscriptions/Suscriptions'

const Home = () => {
  return (
    <div className='home'>
      <HeroSection />
      <LastPosts />
      <TrendForum />
      <Suscriptions />
    </div>
  )
}

export default Home
