import QuestionForm from '../QuestionForm/QuestionForm'
import AnswerPost from '../AnswerPost/AnswerPost'

import styles from './QuestionsPost.module.css'

const QuestionsPost = () => {
  return (
    <div className={styles.questionsContainer}>
      <h2 style={{ color: '#fff' }}>Preguntas y respuestas</h2>

      <QuestionForm />

      <AnswerPost />
    </div>
  )
}

export default QuestionsPost
