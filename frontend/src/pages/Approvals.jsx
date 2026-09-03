import { useCallback, useEffect, useState } from 'react'
import { api } from '../api'
import { demoApprovals } from '../data'
import { useApi } from '../hooks'
import { ErrorState, Loading, SectionHeading } from '../components/Ui'

export default function Approvals() {
  const loadApprovals = useCallback(() => api.getApprovals(), [])
  const { data, loading, error } = useApi(loadApprovals, demoApprovals)
  const [requests, setRequests] = useState(data)
  const [message, setMessage] = useState(null)

  useEffect(() => {
    setRequests(data)
  }, [data])

  async function resolve(requestId, action) {
    setMessage(null)
    try {
      const result = await (action === 'approve' ? api.approve(requestId) : api.reject(requestId))
      setRequests((current) => current.filter((request) => request.request_id !== requestId))
      setMessage({ ok: true, text: result.status === 'APPROVED' ? 'Redemption approved and points deducted.' : 'Redemption rejected. No points were deducted.' })
    } catch (actionError) {
      setMessage({ ok: false, text: actionError.message })
    }
  }

  if (loading) return <Loading label="Loading approval queue" />
  return <><SectionHeading eyebrow="HUMAN REVIEW" title="Approval queue" action={<span className="record-count">{requests.length} pending</span>} />{error && <ErrorState message={error} />}{message && <div className={`queue-message ${message.ok ? 'message-ok' : 'message-error'}`}><span className={`approval-status ${message.text.includes('approved') ? 'status-approved' : 'status-rejected'}`}>{message.text.includes('approved') ? 'Approved' : 'Rejected'}</span>{message.text}</div>}<section className="approval-directory"><div className="approval-table"><div className="approval-header"><span>Member</span><span>Reward</span><span>Points</span><span>Date</span><span>Actions</span></div>{requests.length ? requests.map((request) => <div className="approval-row" key={request.request_id}><div><strong>{request.member_name}</strong><small>{request.member_id}</small></div><div><strong>{request.reward_type.replace('_', ' ')}</strong><small>{request.request_id}</small><span className="approval-status status-pending">Pending</span></div><strong>{request.points.toLocaleString()}</strong><span>{new Date(request.created_at).toLocaleDateString()}</span><div className="approval-actions"><button className="action-button approve" onClick={() => resolve(request.request_id, 'approve')}>Approve</button><button className="action-button reject" onClick={() => resolve(request.request_id, 'reject')}>Reject</button></div></div>) : <div className="queue-empty">No requests are waiting for review.</div>}</div></section></>
}