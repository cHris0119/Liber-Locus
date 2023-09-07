import styles from './InputLabelBook.module.css'

export const SelectLabelBook = ({ inputId, label }) => {
  return (
    <div className={styles.inputLabelContainer}>
      <label htmlFor={inputId}>{label}</label>
      <select>
        <option value="Terror">Terror</option>
        <option value="Romance">Romance</option>
      </select>
    </div>
  )
}

export const InputLabelBook = ({ label, inputId, placeholder }) => {
  return (
    <div className={styles.inputLabelContainer}>
      <label htmlFor={inputId}>{label}</label>
      <input type="text" id={inputId} name={inputId} placeholder={placeholder} />
    </div>
  )
}
