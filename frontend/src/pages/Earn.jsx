import { useState } from 'react'
import { api } from '../api'
import { demoMembers, demoPromotions } from '../data'
import { useApi } from '../hooks'
import { ErrorState, Loading, SectionHeading, TierBadge } from '../components/Ui'

export default function Earn() {
	const members = useApi(api.getMembers, demoMembers)
	const promotions = useApi(api.getPromotions, demoPromotions)
	const [memberId, setMemberId] = useState('MBR-001')
	const [usd, setUsd] = useState('')
	const [message, setMessage] = useState(null)
	const member = members.data.find((item) => item.id === memberId)
	const basePoints = usd && member ? Math.floor(Number(usd) * 10 * ({ BASE: 1, SILVER: 1.1, GOLD: 1.25, PLATINUM: 1.5 }[member.tier])) : 0
	const promo = promotions.data.find((item) => item.type === 'EARN_MULTIPLIER')
	const points = promo && basePoints ? Math.floor(basePoints * promo.value) : basePoints

	async function submit(event) {
		event.preventDefault()
		setMessage(null)
		try {
			const result = await api.earn({ member_id: memberId, amount_usd: Number(usd) })
			setMessage({ ok: true, text: `${result.earned_points.toLocaleString()} points recorded for ${memberId}. New balance: ${result.new_balance.toLocaleString()}.` })
		} catch (error) {
			setMessage({ ok: false, text: error.message })
		}
	}

	if (members.loading) return <Loading label="Loading earn form" />
	return <><SectionHeading eyebrow="EARNING ENGINE" title="Earn points" action={<div className="formula">USD × 10 × tier × promo</div>} />{members.error && <ErrorState message={members.error} />}<div className="form-layout"><form className="panel form-panel" onSubmit={submit}><div className="field"><label>Member</label><select value={memberId} onChange={(event) => setMemberId(event.target.value)}>{members.data.map((item) => <option key={item.id} value={item.id}>{item.id} · {item.name}</option>)}</select></div><div className="field"><label>Eligible spend <small>USD</small></label><input type="number" min="0" step="0.01" value={usd} onChange={(event) => setUsd(event.target.value)} placeholder="0.00" required /></div><div className="context-line"><span>Current tier</span><TierBadge tier={member?.tier} /></div><button className="button button-dark button-wide" type="submit">Submit earn transaction <span>↗</span></button>{message && <div className={`message ${message.ok ? 'message-ok' : 'message-error'}`}>{message.text}</div>}</form><aside className="panel calculation-panel"><div className="eyebrow">CALCULATION PREVIEW</div><div className="calculation-total"><small>Points to be issued</small><strong>{points.toLocaleString()}</strong></div><div className="calc-line"><span>Base points</span><b>{basePoints.toLocaleString()}</b></div><div className="calc-line"><span>Applied promotion</span><b>{promo ? `${promo.name} · ${promo.value}×` : 'None'}</b></div><div className="note">The backend remains the source of truth when this transaction is submitted.</div></aside></div></>
}
