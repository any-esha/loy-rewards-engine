import { useState } from 'react'
import { api } from '../api'
import { demoMembers } from '../data'
import { useApi } from '../hooks'
import { EmptyState, ErrorState, Loading, Modal, SectionHeading, TierBadge } from '../components/Ui'

export default function Members() {
	const { data, loading, error } = useApi(api.getMembers, demoMembers)
	const [query, setQuery] = useState('')
	const [selected, setSelected] = useState(null)
	if (loading) return <Loading label="Loading members" />
	const filtered = data.filter((member) => member.id.toLowerCase().includes(query.toLowerCase()))

	return <>
		<SectionHeading eyebrow="DIRECTORY" title="Members" action={<span className="record-count">{filtered.length} records</span>} />
		{error && <ErrorState message={error} />}
		<section className="member-directory">
			<div className="member-toolbar"><label className="search member-search"><span>⌕</span><input value={query} onChange={(event) => setQuery(event.target.value)} placeholder="Search by member ID" /></label><span className="muted">{filtered.length} members · select a card for details</span></div>
			{filtered.length ? <div className="member-grid">{filtered.map((member) => <button className="member-card" key={member.id} onClick={() => setSelected(member)}><div className="member-card-top"><span className="avatar member-avatar">{member.name?.split(' ').map((part) => part[0]).join('')}</span><span className="card-arrow">↗</span></div><div className="member-card-identity"><span className="card-label">Member ID</span><strong>{member.id}</strong><span className="card-label">Name</span><h2>{member.name}</h2></div><div className="member-card-tier"><span className="card-label">Tier</span><TierBadge tier={member.tier} /></div><div className="member-card-stats"><div><span className="card-label">Available Points</span><strong>{member.points_balance.toLocaleString()}</strong></div><div><span className="card-label">Lifetime Points</span><strong>{member.lifetime_points.toLocaleString()}</strong></div></div></button>)}</div> : <div className="panel"><EmptyState /></div>}
		</section>
		<Modal member={selected} onClose={() => setSelected(null)} />
	</>
}
