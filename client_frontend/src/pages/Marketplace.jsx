import MarketplaceHeader from '../components/MarketplaceHeader/MarketplaceHeader'
import PostList from '../components/PostList/PostList'

const Marketplace = () => {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>

      <h1 style={{ color: '#fff', textAlign: 'center', borderBottom: '2px solid #fff', paddingBottom: '20px', display: 'inline-block' }}>MARKETPLACE</h1>

      <MarketplaceHeader />
      <PostList />
    </div>
  )
}

export default Marketplace
