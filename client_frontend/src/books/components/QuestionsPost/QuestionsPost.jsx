import { QuestionForm, AnswerPost } from '../'

import styles from './QuestionsPost.module.css'

export const QuestionsPost = () => {
  return (

    <div className={styles.questionsContainer}>
      <h2 style={{ color: '#fff' }}>Preguntas y respuestas</h2>

      <QuestionForm />
      <AnswerPost />

    </div>

  )
}
