 import { clsx } from 'clsx'
 
 export interface CardProps extends React.HTMLAttributes<HTMLDivElement> {}
 
 export function Card({ className, children, ...props }: CardProps) {
   return (
     <div className={clsx('card', className)} {...props}>
       {children}
     </div>
   )
 }
 
 export function CardHeader({ className, children, ...props }: CardProps) {
   return (
     <div className={clsx('card-header', className)} {...props}>
       {children}
     </div>
   )
 }
 
 export function CardBody({ className, children, ...props }: CardProps) {
   return (
     <div className={clsx('card-body', className)} {...props}>
       {children}
     </div>
   )
 }
 
 export function CardFooter({ className, children, ...props }: CardProps) {
   return (
     <div className={clsx('card-footer', className)} {...props}>
       {children}
     </div>
   )
 }
