import './TrendForum.css'
import HomeSection from '../HomeSection/HomeSection'
import trendForum from '../../mocks/trendForum.json'

const TrendForum = () => {
  const forums = trendForum.Forum

  return (
    <HomeSection styles='home-forum'>
      <div className="trendForum-container">
        <h2>Foros populares</h2>
        <div className="forums-container">
          {forums.map((forum) => (
            <article className='forum-card' key={forum.id}>
              <h4>{forum.name}</h4>
              <span>{'+'}</span>
            </article>
          ))}
        </div>
      </div>
    </HomeSection>
  )
}

export default TrendForum
