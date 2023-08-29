import MarketplaceHeader from '../components/MarketplaceHeader/MarketplaceHeader'
import PostList from '../components/PostList/PostList'

const Marketplace = () => {
  return (
    <div className="mainContent" style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>

      <h1 style={{ textAlign: 'center' }}>MARKETPLACE</h1>

      <MarketplaceHeader />
      <PostList />
    </div>
  )
}

export default Marketplace
