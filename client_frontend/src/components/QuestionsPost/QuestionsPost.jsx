import './QuestionsPost.css'
import QuestionForm from '../QuestionForm/QuestionForm'
import AnswerPost from '../AnswerPost/AnswerPost'

const QuestionsPost = () => {
  return (
    <div className='questions-container'>
      <h2 style={{ color: '#fff' }}>Preguntas y respuestas</h2>

      <QuestionForm />

      <AnswerPost />
    </div>
  )
}

export default QuestionsPost
