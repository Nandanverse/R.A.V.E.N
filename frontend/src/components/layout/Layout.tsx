 import { useState, useEffect } from 'react'
 import { Outlet, NavLink, useLocation } from 'react-router-dom'
 import {
   Home,
   ClipboardList,
   Server,
   Search,
   Database,
   AlertTriangle,
   GitBranch,
   Brain,
   BarChart2,
   FileText,
   Settings,
   Info,
   ChevronLeft,
   ChevronRight,
   Menu,
   X,
 } from 'lucide-react'
 import { navigation } from '@/App'
 import clsx from 'clsx'
 
 const iconMap = {
   Home,
   ClipboardList,
   Server,
   Search,
   Database,
   AlertTriangle,
   GitBranch,
   Brain,
   BarChart2,
   FileText,
   Settings,
   Info,
 } as const
 
 export function Layout({ navigation: navItems }: { navigation: typeof navigation }) {
   const [collapsed, setCollapsed] = useState(false)
   const [mobileOpen, setMobileOpen] = useState(false)
   const location = useLocation()
 
   useEffect(() => {
     setMobileOpen(false)
   }, [location.pathname])
 
   return (
     <div className="min-h-screen bg-bg-base">
       {/* Mobile menu overlay */}
       {mobileOpen && (
         <div
           className="fixed inset-0 z-30 bg-black/50 lg:hidden"
           onClick={() => setMobileOpen(false)}
         />
       )}
 
       {/* Sidebar */}
       <aside
         className={clsx(
           'sidebar',
           collapsed && 'sidebar-collapsed',
           mobileOpen && 'lg:hidden translate-x-0',
           !mobileOpen && 'lg:hidden -translate-x-full'
         )}
         aria-label="Main navigation"
       >
         {/* Logo */}
         <div className="flex items-center justify-between h-12 px-3 border-b border-border">
           <span className={clsx('font-mono font-bold text-lg text-fg-primary transition-opacity', collapsed && 'opacity-0')}>
             RAVEN
           </span>
           <button
             onClick={() => setCollapsed(!collapsed)}
             className="p-1 text-fg-muted hover:text-fg-primary rounded-sm hover:bg-bg-hover transition-colors"
             aria-label={collapsed ? 'Expand sidebar' : 'Collapse sidebar'}
             aria-expanded={!collapsed}
           >
             {collapsed ? <ChevronRight size={18} /> : <ChevronLeft size={18} />}
           </button>
         </div>
 
         {/* Navigation */}
         <nav className="flex-1 overflow-y-auto py-3 px-2" aria-label="Main navigation">
           <ul className="space-y-1" role="list">
             {navItems.map((item) => {
               const Icon = iconMap[item.icon as keyof typeof iconMap]
               const isActive = location.pathname === item.path || 
                 (item.path !== '/' && location.pathname.startsWith(item.path))
 
               return (
                 <li key={item.path}>
                   <NavLink
                     to={item.path}
                     className={({ isActive: active }) => clsx(
                       'flex items-center gap-3 px-3 py-2 text-sm rounded-sm transition-colors duration-0',
                       'hover:bg-bg-hover hover:text-fg-primary',
                       active
                         ? 'bg-sev-info/10 text-sev-info border-l-2 border-sev-info'
                         : 'text-fg-secondary',
                       collapsed && 'justify-center'
                     )}
                     aria-current={isActive ? 'page' : undefined}
                     title={collapsed ? item.label : undefined}
                   >
                     <Icon size={18} aria-hidden="true" />
                     {!collapsed && <span className="truncate">{item.label}</span>}
                   </NavLink>
                 </li>
               )
             })}
           </ul>
         </nav>
 
         {/* Footer */}
         <div className="p-3 border-t border-border">
           <div className={clsx('text-xs text-fg-muted text-center transition-opacity', collapsed && 'opacity-0')}>
             v0.1.0
           </div>
         </div>
       </aside>
 
       {/* Mobile menu button */}
       <button
         className="lg:hidden fixed top-3 left-3 z-50 p-2 bg-bg-elevated border border-border rounded-sm text-fg-primary hover:bg-bg-hover"
         onClick={() => setMobileOpen(true)}
         aria-label="Open menu"
       >
         <Menu size={20} />
       </button>
 
       {/* Header */}
       <header className={clsx('header', collapsed && 'lg:pl-16')}>
         <div className="flex items-center gap-4">
           <h1 className="font-mono text-lg font-bold text-fg-primary">RAVEN</h1>
           <span className="hidden sm:block text-fg-muted">Risk-Aware Autonomous Vulnerability Exploration Network</span>
         </div>
         <div className="flex items-center gap-4">
           {/* Status indicator */}
           <div className="flex items-center gap-2 text-sm text-fg-secondary">
             <span className="w-2 h-2 rounded-full bg-status-success" aria-hidden="true" />
             <span>Backend Connected</span>
           </div>
         </div>
       </header>
 
       {/* Main content */}
       <main
         className={clsx('main-content', collapsed && 'main-content-expanded')}
         role="main"
         tabIndex={-1}
       >
         <Outlet />
       </main>
     </div>
   )
 }
