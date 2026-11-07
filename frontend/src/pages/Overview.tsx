 import { useQuery } from '@tanstack/react-query'
 import { api } from '@/lib/api'
 import {
   Server,
   AlertTriangle,
   Database,
   FileText,
   Activity,
   CheckCircle,
   AlertCircle,
   Clock,
 } from 'lucide-react'
 import { Card, CardHeader, CardBody } from '@/components/ui/Card'
 import { Badge } from '@/components/ui/Badge'
 import { LoadingSpinner } from '@/components/ui/LoadingSpinner'
 import { EmptyState } from '@/components/ui/EmptyState'
 
 interface OverviewStats {
   total_assessments: number
   running_assessments: number
   completed_assessments: number
   total_assets: number
   total_findings: number
   validated_findings: number
   critical_findings: number
   high_findings: number
   total_evidence: number
   total_jobs: number
 }
 
 export function Overview() {
   const { data: stats, isLoading, error } = useQuery({
     queryKey: ['overview'],
     queryFn: () => api.get<OverviewStats>('/analytics/overview'),
     refetchInterval: 30000,
   })
 
   if (isLoading) {
     return (
       <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 p-4">
         {[1, 2, 3, 4].map((i) => (
           <Card key={i}>
             <CardBody className="flex items-center justify-center h-24">
               <LoadingSpinner size="lg" />
             </CardBody>
           </Card>
         ))}
       </div>
     )
   }
 
   if (error) {
     return (
       <EmptyState
         icon={<AlertCircle size={48} />}
         title="Failed to load overview"
         description="Unable to fetch statistics from the backend."
       />
     )
   }
 
   const statCards = [
     { label: 'Total Assessments', value: stats?.total_assessments ?? 0, icon: Server, color: 'text-fg-primary' },
     { label: 'Running', value: stats?.running_assessments ?? 0, icon: Activity, color: 'text-sev-info' },
     { label: 'Completed', value: stats?.completed_assessments ?? 0, icon: CheckCircle, color: 'text-sev-low' },
     { label: 'Total Assets', value: stats?.total_assets ?? 0, icon: Database, color: 'text-fg-primary' },
     { label: 'Total Findings', value: stats?.total_findings ?? 0, icon: AlertTriangle, color: 'text-sev-high' },
     { label: 'Validated', value: stats?.validated_findings ?? 0, icon: CheckCircle, color: 'text-sev-low' },
     { label: 'Critical', value: stats?.critical_findings ?? 0, icon: AlertCircle, color: 'text-sev-critical' },
     { label: 'High', value: stats?.high_findings ?? 0, icon: AlertTriangle, color: 'text-sev-high' },
     { label: 'Evidence Items', value: stats?.total_evidence ?? 0, icon: FileText, color: 'text-fg-primary' },
     { label: 'Jobs Executed', value: stats?.total_jobs ?? 0, icon: Clock, color: 'text-fg-primary' },
   ]
 
   return (
     <div className="p-4 space-y-6">
       <div className="flex items-center justify-between">
         <div>
           <h1 className="text-2xl font-bold text-fg-primary">Overview</h1>
           <p className="text-sm text-fg-muted">System-wide assessment statistics</p>
         </div>
       </div>
 
       <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4">
         {statCards.map((stat, index) => (
           <Card key={index}>
             <CardBody className="flex items-center gap-4">
               <div className={clsx('p-3 rounded-sm bg-bg-base', stat.color)}>
                 <stat.icon size={24} aria-hidden="true" />
               </div>
               <div>
                 <p className="text-sm text-fg-secondary">{stat.label}</p>
                 <p className="text-2xl font-bold text-fg-primary font-mono">{stat.value}</p>
               </div>
             </CardBody>
           </Card>
         ))}
       </div>
 
       <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
         <Card>
           <CardHeader>
             <h2 className="text-lg font-medium text-fg-primary">Quick Actions</h2>
           </CardHeader>
           <CardBody className="space-y-3">
             <button className="btn-secondary w-full justify-start">Create New Assessment</button>
             <button className="btn-secondary w-full justify-start">Define Scope</button>
             <button className="btn-secondary w-full justify-start">View Recent Findings</button>
             <button className="btn-secondary w-full justify-start">Generate Report</button>
           </CardBody>
         </Card>
 
         <Card>
           <CardHeader>
             <h2 className="text-lg font-medium text-fg-primary">System Status</h2>
           </CardHeader>
           <CardBody className="space-y-3">
             <div className="flex items-center justify-between py-2 border-b border-separator">
               <span className="text-fg-secondary">API Server</span>
               <Badge variant="success">Online</Badge>
             </div>
             <div className="flex items-center justify-between py-2 border-b border-separator">
               <span className="text-fg-secondary">Database</span>
               <Badge variant="success">Connected</Badge>
             </div>
             <div className="flex items-center justify-between py-2 border-b border-separator">
               <span className="text-fg-secondary">Redis</span>
               <Badge variant="success">Connected</Badge>
             </div>
             <div className="flex items-center justify-between py-2">
               <span className="text-fg-secondary">Ollama (LLM)</span>
               <Badge variant="warning">Not Configured</Badge>
             </div>
           </CardBody>
         </Card>
       </div>
     </div>
   )
 }
 
 import clsx from 'clsx'
