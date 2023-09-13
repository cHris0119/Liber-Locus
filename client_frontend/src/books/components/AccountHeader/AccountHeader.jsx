import styles from './AccountHeader.module.css'

export const AccountHeader = () => {
  return (
    <header className={styles.accountHeader}>
            <section className={styles.headerLeft}>
                <div className={styles.headerContainerImg}>
                    <img src="#" alt="img-user" />
                </div>
            </section>
            <section className={styles.headerRight}>
                <h1>Nombre de usuario</h1>
                <div className={styles.userFollowers}>
                    <p><span>100</span> Seguidores</p>
                    <p><span>5</span> Seguidos</p>
                </div>
                <button className={styles.followButton}>Editar perfil</button>
            </section>
        </header>
  )
}
