export const demoMembers = [
  { id: 'MBR-001', name: 'Amelia Hartley', tier: 'GOLD', points_balance: 42500, lifetime_points: 44000, email: 'amelia.hartley@example.com' },
  { id: 'MBR-002', name: 'Rohan Mehta', tier: 'SILVER', points_balance: 18200, lifetime_points: 21200, email: 'rohan.mehta@example.com' },
  { id: 'MBR-003', name: 'Sofia Alvarez', tier: 'BASE', points_balance: 3400, lifetime_points: 7900, email: 'sofia.alvarez@example.com' },
  { id: 'MBR-004', name: 'Kenji Watanabe', tier: 'PLATINUM', points_balance: 88000, lifetime_points: 94000, email: 'kenji.watanabe@example.com' },
]

export const demoPromotions = [
  { id: 'PROMO-1', name: 'Double Points Weekend', type: 'EARN_MULTIPLIER', value: 2, start: '2026-09-20', end: '2026-09-22', applies_to: ['ROOM'] },
  { id: 'PROMO-2', name: '5k Bonus on 3rd Stay', type: 'BONUS_POINTS', value: 5000, start: '2026-09-01', end: '2026-12-31', applies_to: ['ROOM'] },
]

export const demoTransactions = [
  { id: 'TXN-0001', member_id: 'MBR-001', type: 'EARN', points: 1740, reference: 'BK-001', created_at: '2026-09-02T01:00:00Z' },
  { id: 'TXN-0002', member_id: 'MBR-004', type: 'EARN', points: 4400, reference: 'STAY-B', created_at: '2026-09-03T04:00:00Z' },
  { id: 'TXN-0003', member_id: 'MBR-001', type: 'REDEEM', points: -15000, reference: 'AWARD-NIGHT', created_at: '2026-09-07T03:00:00Z' },
]

export const demoAuditLogs = [
  { event_id: 'AUD-1001', event_type: 'EARN', member_id: 'MBR-001', points_delta: 1740, balance_before: 40760, balance_after: 42500, created_at: '2026-09-02T01:00:02Z' },
  { event_id: 'AUD-1002', event_type: 'REDEEM', member_id: 'MBR-001', points_delta: -15000, balance_before: 42500, balance_after: 27500, created_at: '2026-09-07T03:00:02Z' },
]

export const demoApprovals = [
  { request_id: 'REQ-004', member_id: 'MBR-004', member_name: 'Kenji Watanabe', reward_type: 'SUITE_AWARD', points: 40000, status: 'PENDING_APPROVAL', created_at: '2026-09-03T09:20:00Z' },
]
