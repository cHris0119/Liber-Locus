import HomeSection from '../HomeSection/HomeSection'
import trendForum from '../../mocks/trendForum.json'

import styles from './TrendForum.module.css'

const TrendForum = () => {
  const forums = trendForum.Forum

  return (
    <HomeSection>
      <div className={styles.trendForumContainer}>
        <h2>Foros populares</h2>
        <div className={styles.forumsContainer}>
          {forums.map((forum) => (
            <article className={styles.forumCard} key={forum.id}>
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
