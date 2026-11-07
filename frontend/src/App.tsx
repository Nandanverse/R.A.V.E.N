 import { Routes, Route, Navigate } from 'react-router-dom'
 import { Layout } from '@/components/layout/Layout'
 import { Overview } from '@/pages/Overview'
 import { Assessments } from '@/pages/Assessments'
 import { Assets } from '@/pages/Assets'
 import { Recon } from '@/pages/Recon'
 import { Intel } from '@/pages/Intel'
 import { Findings } from '@/pages/Findings'
 import { AttackGraph } from '@/pages/AttackGraph'
 import { AIAnalysis } from '@/pages/AIAnalysis'
 import { Analytics } from '@/pages/Analytics'
 import { Reports } from '@/pages/Reports'
 import { Settings } from '@/pages/Settings'
 import { About } from '@/pages/About'
 
 const navigation = [
   { path: '/', label: 'Overview', icon: 'Home' },
   { path: '/assessments', label: 'Assessments', icon: 'ClipboardList' },
   { path: '/assets', label: 'Asset Inventory', icon: 'Server' },
   { path: '/recon', label: 'Reconnaissance', icon: 'Search' },
   { path: '/intel', label: 'Vulnerability Intelligence', icon: 'Database' },
   { path: '/findings', label: 'Findings', icon: 'AlertTriangle' },
   { path: '/graph', label: 'Attack Graph', icon: 'GitBranch' },
   { path: '/brain', label: 'AI Analysis', icon: 'Brain' },
   { path: '/analytics', label: 'Analytics', icon: 'BarChart2' },
   { path: '/reports', label: 'Reports', icon: 'FileText' },
   { path: '/settings', label: 'Settings', icon: 'Settings' },
   { path: '/about', label: 'About', icon: 'Info' },
 ] as const
 
 export function App() {
   return (
     <Layout navigation={navigation}>
       <Routes>
         <Route path="/" element={<Overview />} />
         <Route path="/assessments" element={<Assessments />} />
         <Route path="/assets" element={<Assets />} />
         <Route path="/recon" element={<Recon />} />
         <Route path="/intel" element={<Intel />} />
         <Route path="/findings" element={<Findings />} />
         <Route path="/graph" element={<AttackGraph />} />
         <Route path="/brain" element={<AIAnalysis />} />
         <Route path="/analytics" element={<Analytics />} />
         <Route path="/reports" element={<Reports />} />
         <Route path="/settings" element={<Settings />} />
         <Route path="/about" element={<About />} />
         <Route path="*" element={<Navigate to="/" replace />} />
       </Routes>
     </Layout>
   )
 }
