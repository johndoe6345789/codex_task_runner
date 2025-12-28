import React from 'react'

export const Table = ({ children, className = '', ...props }) => (
  <table className={`table ${className}`} {...props}>{children}</table>
)

export const TableHead = ({ children, className = '', ...props }) => (
  <thead className={`table-head ${className}`} {...props}>{children}</thead>
)

export const TableBody = ({ children, className = '', ...props }) => (
  <tbody className={`table-body ${className}`} {...props}>{children}</tbody>
)

export const TableFooter = ({ children, className = '', ...props }) => (
  <tfoot className={`table-footer ${className}`} {...props}>{children}</tfoot>
)

export const TableRow = ({ children, hover, selected, className = '', ...props }) => (
  <tr className={`table-row ${hover ? 'table-row--hover' : ''} ${selected ? 'table-row--selected' : ''} ${className}`} {...props}>{children}</tr>
)

export const TableCell = ({ children, header, align, className = '', ...props }) => {
  const Tag = header ? 'th' : 'td'
  return <Tag className={`table-cell ${align ? `table-cell--${align}` : ''} ${className}`} {...props}>{children}</Tag>
}

export const TableContainer = ({ children, className = '', ...props }) => (
  <div className={`table-container ${className}`} {...props}>{children}</div>
)
