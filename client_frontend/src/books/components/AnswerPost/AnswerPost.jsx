import lastQuestions from '../../mocks/lastQuestions.json'

import styles from './AnswerPost.module.css'

const RenderQuestions = () => {
  const lastTenQuestions = lastQuestions.Questions.slice(1, 4)

  return (
    lastTenQuestions.map((question) => (
      <div className={styles.lastAnswer} key={question.id}>
        <p className={styles.lastAnswerQuestion}>{question.question}</p>
        {question.answer
          ? <div className={styles.lastAnswerContainer}>
            <p className={styles.lastAnswerP}>{question.answer}</p><span className={styles.lastAnswerDate}>{question.created_at}</span>
          </div>
          : <form className={styles.formAnswer}>
            <input type="text" placeholder='...' />
            <input type="submit" value='Responder' />
          </form>}

      </div>
    ))
  )
}

export const AnswerPost = () => {
  return (
    <div className={styles.answerContainer}>
      <h3 style={{ color: '#fff' }} >Ultimas respuestas</h3>
      <RenderQuestions />
    </div>
  )
}
