import styles from './Input.module.css'

export const Input = ({
  label,
  type,
  value,
  placeholder,
  error,
  name
}) => {
  return (
    <div className={styles.inputContainer}>
      <label htmlFor={name}>{label}</label>
      <input
        id={name}
        type={type}
        name={name}
        value={value}
        placeholder={placeholder}
      />
      {error && <span>{error}</span>}
    </div>
  )
}
