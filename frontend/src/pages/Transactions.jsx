import { useState } from 'react'
import { api } from '../api'
import { demoTransactions } from '../data'
import { useApi } from '../hooks'
import { EmptyState, ErrorState, Loading, SectionHeading } from '../components/Ui'

export default function Transactions() {
	const { data, loading, error } = useApi(api.getTransactions, demoTransactions)
	const [member, setMember] = useState('')
	const [type, setType] = useState('')
	if (loading) return <Loading label="Loading transactions" />
	const filtered = data.filter((item) => (!member || item.member_id.toLowerCase().includes(member.toLowerCase())) && (!type || item.type === type))

	return <>
		<SectionHeading eyebrow="IMMUTABLE LEDGER" title="Transactions" action={<span className="record-count">{filtered.length} records</span>} />
		{error && <ErrorState message={error} />}
		<section className="transaction-directory">
			<div className="transaction-toolbar"><label className="search transaction-search"><span>⌕</span><input value={member} onChange={(event) => setMember(event.target.value)} placeholder="Filter by member ID" /></label><select className="compact-select" value={type} onChange={(event) => setType(event.target.value)}><option value="">All transaction types</option><option value="EARN">Earn</option><option value="REDEEM">Redeem</option></select></div>
			{filtered.length ? <div className="transaction-grid">{filtered.map((item) => <details className="transaction-card" key={item.id}><summary><div className="transaction-card-top"><span className={`transaction-dot ${item.type.toLowerCase()}`} /><span className={`type-pill ${item.type.toLowerCase()}`}>{item.type}</span><span className="card-arrow">↗</span></div><span className="card-label">Transaction</span><strong className="transaction-id">{item.id}</strong><h2>{item.reference}</h2><div className="transaction-points"><span className="card-label">Points delta</span><strong className={item.points > 0 ? 'positive' : 'negative'}>{item.points > 0 ? '+' : ''}{item.points.toLocaleString()}</strong></div></summary><div className="transaction-detail-grid"><div><span className="card-label">Member</span><strong>{item.member_id}</strong></div><div><span className="card-label">Created</span><strong>{new Date(item.created_at).toLocaleDateString()}</strong></div></div></details>)}</div> : <div className="panel"><EmptyState /></div>}
		</section>
	</>
}
