import { NavLink, Outlet } from 'react-router-dom'

const navItems = [
  ['/', 'Overview'],
  ['/members', 'Members'],
  ['/earn', 'Earn points'],
  ['/redeem', 'Redeem points'],
  ['/approvals', 'Approval queue'],
  ['/promotions', 'Promotions'],
  ['/transactions', 'Transactions'],
  ['/audit', 'Audit log'],
]

export default function Layout() {
  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand"><span className="brand-mark">F</span><span>Folio <small>REWARDS OS</small></span></div>
        <nav className="nav-list" aria-label="Primary navigation">
          {navItems.map(([to, label]) => <NavLink key={to} to={to} end={to === '/'}>{label}</NavLink>)}
        </nav>
        <div className="sidebar-foot"><span className="status-dot" /> System live<br /><small>Ruleset v1.0.0</small></div>
      </aside>
      <main className="main-content">
        <header className="topbar"><div className="eyebrow">LOYALTY OPERATIONS</div><div className="topbar-user"><span className="avatar">OP</span><span>Operator</span></div></header>
        <div className="page-wrap"><Outlet /></div>
      </main>
    </div>
  )
}
