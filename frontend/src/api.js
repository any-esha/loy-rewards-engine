const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export async function request(path, options = {}) {
  const response = await fetch(`${API_BASE}${path}`, {
    headers: { 'Content-Type': 'application/json', ...options.headers },
    ...options,
  })

  if (!response.ok) {
    const body = await response.text()
    let detail = body
    try {
      const parsed = JSON.parse(body)
      detail = parsed.detail || parsed.message || body
      if (Array.isArray(detail)) detail = detail.map((item) => item.msg).join(', ')
    } catch {
      detail = body
    }
    throw new Error(detail || `Request failed with status ${response.status}`)
  }

  return response.status === 204 ? null : response.json()
}

function normalizeMember(member) {
  return { ...member, id: member.id || member.member_id }
}

function normalizeTransaction(transaction) {
  return { ...transaction, id: transaction.id || transaction.transaction_id }
}

export const api = {
  getMembers: async () => (await request('/members')).map(normalizeMember),
  getMember: async (id) => normalizeMember(await request(`/members/${id}`)),
  earn: (payload) => request('/earn', { method: 'POST', body: JSON.stringify(payload) }),
  redeem: (payload) => request('/redeem', { method: 'POST', body: JSON.stringify(payload) }),
  getPromotions: () => request('/promotions'),
  getTransactions: async () => (await request('/transactions')).map(normalizeTransaction),
  getAuditLogs: () => request('/audit-logs'),
  getApprovals: () => request('/approvals'),
  approve: (requestId) => request(`/approvals/${requestId}/approve`, { method: 'POST' }),
  reject: (requestId) => request(`/approvals/${requestId}/reject`, { method: 'POST' }),
}
