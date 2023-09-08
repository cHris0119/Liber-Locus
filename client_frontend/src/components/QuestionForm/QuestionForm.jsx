import styles from './QuestionForm.module.css'

export const QuestionForm = () => {
  return (

    <div className={styles.questionFormContainer}>

      <h3 style={{ color: '#fff' }}>Pregunta al vendedor</h3>

      <form className={styles.questionForm}>
        <input className={styles.questionFormInput} type="text" placeholder='Escribe tu pregunta' />
        <input className={styles.questionFormInput} type="submit" name="" id="" value='Preguntar' />
      </form>

    </div>
  )
}
