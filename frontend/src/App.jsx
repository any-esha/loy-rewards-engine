import { Navigate, Route, Routes } from 'react-router-dom'
import Layout from './components/Layout'
import Dashboard from './pages/Dashboard'
import Members from './pages/Members'
import Earn from './pages/Earn'
import Redeem from './pages/Redeem'
import Promotions from './pages/Promotions'
import Transactions from './pages/Transactions'
import Audit from './pages/Audit'
import Approvals from './pages/Approvals'

export default function App() {
  return <Routes><Route element={<Layout />}><Route path="/" element={<Dashboard />} /><Route path="/members" element={<Members />} /><Route path="/earn" element={<Earn />} /><Route path="/redeem" element={<Redeem />} /><Route path="/approvals" element={<Approvals />} /><Route path="/promotions" element={<Promotions />} /><Route path="/transactions" element={<Transactions />} /><Route path="/audit" element={<Audit />} /><Route path="*" element={<Navigate to="/" replace />} /></Route></Routes>
}
