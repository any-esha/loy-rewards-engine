import { Link } from 'react-router-dom'
import { demoMembers, demoPromotions, demoTransactions } from '../data'
import { api } from '../api'
import { useApi } from '../hooks'
import { Loading, ErrorState, SectionHeading, StatCard, TierBadge } from '../components/Ui'

export default function Dashboard() {
  const members = useApi(api.getMembers, demoMembers)
  const promotions = useApi(api.getPromotions, demoPromotions)
  const transactions = useApi(api.getTransactions, demoTransactions)
  if (members.loading || promotions.loading || transactions.loading) return <Loading label="Loading overview" />
  const tierCounts = ['PLATINUM', 'GOLD', 'SILVER', 'BASE'].map((tier) => ({ tier, count: members.data.filter((member) => member.tier === tier).length }))
  const featured = members.data[0]
  const tierThresholds = { BASE: 0, SILVER: 10000, GOLD: 30000, PLATINUM: 75000 }
  const nextTier = featured?.tier === 'PLATINUM' ? 'PLATINUM' : ['SILVER', 'GOLD', 'PLATINUM'].find((tier) => tierThresholds[tier] > featured?.lifetime_points) || 'PLATINUM'
  const progress = featured ? Math.min(100, Math.round((featured.lifetime_points / tierThresholds[nextTier]) * 100)) : 0
  return <>
    <SectionHeading eyebrow="Tuesday · 03 September 2026" title="Your rewards, in focus." action={<Link className="button button-blue" to="/earn">Record earn <span>↗</span></Link>} />
    {members.error && <ErrorState message={members.error} />}
    <div className="bento-grid"><section className="glass-card hero-card"><div className="eyebrow">FEATURED MEMBER</div><div className="hero-member"><div><span className="avatar avatar-xl">{featured?.name?.split(' ').map((part) => part[0]).join('')}</span><h2>{featured?.name}</h2><span className="muted">{featured?.id} · {featured?.tier} member</span></div><div className="hero-balance"><small>Available balance</small><strong>{featured?.points_balance.toLocaleString()}</strong><span>points</span></div></div><Link className="text-link" to="/members">View member profile →</Link></section><section className="glass-card ring-card"><div className="eyebrow">TIER MOMENTUM</div><div className="ring-wrap"><div className="progress-ring" style={{ '--progress': `${progress}%` }}><div><strong>{progress}%</strong><small>to {nextTier}</small></div></div><div><h2>{featured?.tier}</h2><p>{featured?.lifetime_points.toLocaleString()} lifetime points</p><span className="blue-chip">{nextTier === featured?.tier ? 'Peak tier' : `${(tierThresholds[nextTier] - featured?.lifetime_points).toLocaleString()} pts to go`}</span></div></div></section><section className="glass-card stat-cluster"><StatCard label="Members" value={members.data.length} detail="All tiers" accent="accent-blue" /><StatCard label="Transactions" value={transactions.data.length} detail="In the ledger" accent="accent-sky" /></section><section className="glass-card tier-card"><div className="panel-head"><div><div className="eyebrow">MEMBER MIX</div><h2>Tier distribution</h2></div><Link to="/members" className="text-link">Explore →</Link></div><div className="tier-pills">{tierCounts.map(({ tier, count }) => <div key={tier}><span className={`tier-orb orb-${tier.toLowerCase()}`} /><strong>{count}</strong><small>{tier}</small></div>)}</div></section><section className="glass-card promo-panel"><div className="panel-head"><div><div className="eyebrow">LIVE NOW</div><h2>Promotions</h2></div><Link to="/promotions" className="text-link">All →</Link></div>{promotions.data.slice(0, 2).map((promo) => <div className="promo-row" key={promo.id}><span className="promo-icon">✦</span><div><strong>{promo.name}</strong><small>{promo.type === 'EARN_MULTIPLIER' ? `${promo.value}× points` : `+${promo.value.toLocaleString()} points`}</small></div><span className="live-pill">LIVE</span></div>)}</section><section className="glass-card table-panel"><div className="panel-head"><div><div className="eyebrow">RECENT ACTIVITY</div><h2>Latest transactions</h2></div><Link to="/transactions" className="text-link">Open ledger →</Link></div><TransactionRows transactions={transactions.data.slice(0, 3)} /></section></div>
  </>
}

function TransactionRows({ transactions }) { return <div className="mini-list">{transactions.map((transaction) => <details className="mini-row expandable" key={transaction.id}><summary><span className={`transaction-dot ${transaction.type.toLowerCase()}`} /><span><strong>{transaction.reference}</strong><small>{transaction.member_id} · {new Date(transaction.created_at).toLocaleDateString()}</small></span><b className={transaction.points > 0 ? 'positive' : 'negative'}>{transaction.points > 0 ? '+' : ''}{transaction.points.toLocaleString()}</b></summary><div className="transaction-detail">{transaction.type} · immutable ledger entry · {transaction.id}</div></details>)}</div> }
