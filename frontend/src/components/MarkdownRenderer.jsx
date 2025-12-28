import React from 'react'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import { Box, Link, Typography } from '@mui/material'
import { styled } from '@mui/material/styles'

// Styled container for markdown content
const MarkdownContainer = styled(Box)(({ theme }) => ({
  '& h1': {
    ...theme.typography.h4,
    marginTop: theme.spacing(3),
    marginBottom: theme.spacing(2),
  },
  '& h2': {
    ...theme.typography.h5,
    marginTop: theme.spacing(2.5),
    marginBottom: theme.spacing(1.5),
  },
  '& h3': {
    ...theme.typography.h6,
    marginTop: theme.spacing(2),
    marginBottom: theme.spacing(1),
  },
  '& h4, & h5, & h6': {
    ...theme.typography.subtitle1,
    fontWeight: 600,
    marginTop: theme.spacing(1.5),
    marginBottom: theme.spacing(1),
  },
  '& p': {
    ...theme.typography.body1,
    marginBottom: theme.spacing(1.5),
    lineHeight: 1.7,
  },
  '& ul, & ol': {
    paddingLeft: theme.spacing(3),
    marginBottom: theme.spacing(1.5),
  },
  '& li': {
    ...theme.typography.body1,
    marginBottom: theme.spacing(0.5),
  },
  '& code': {
    fontFamily: '"Fira Code", "Consolas", "Monaco", monospace',
    fontSize: '0.9em',
    backgroundColor: theme.palette.mode === 'dark' 
      ? 'rgba(255, 255, 255, 0.1)' 
      : 'rgba(0, 0, 0, 0.08)',
    padding: '2px 6px',
    borderRadius: 4,
  },
  '& pre': {
    backgroundColor: theme.palette.mode === 'dark' 
      ? 'rgba(0, 0, 0, 0.4)' 
      : 'rgba(0, 0, 0, 0.05)',
    padding: theme.spacing(2),
    borderRadius: theme.shape.borderRadius,
    overflow: 'auto',
    marginBottom: theme.spacing(2),
    '& code': {
      backgroundColor: 'transparent',
      padding: 0,
    },
  },
  '& blockquote': {
    borderLeft: `4px solid ${theme.palette.primary.main}`,
    margin: theme.spacing(2, 0),
    padding: theme.spacing(1, 2),
    backgroundColor: theme.palette.mode === 'dark'
      ? 'rgba(255, 255, 255, 0.05)'
      : 'rgba(0, 0, 0, 0.03)',
    '& p': {
      marginBottom: 0,
    },
  },
  '& table': {
    width: '100%',
    borderCollapse: 'collapse',
    marginBottom: theme.spacing(2),
  },
  '& th, & td': {
    border: `1px solid ${theme.palette.divider}`,
    padding: theme.spacing(1, 1.5),
    textAlign: 'left',
  },
  '& th': {
    backgroundColor: theme.palette.mode === 'dark'
      ? 'rgba(255, 255, 255, 0.08)'
      : 'rgba(0, 0, 0, 0.04)',
    fontWeight: 600,
  },
  '& hr': {
    border: 'none',
    borderTop: `1px solid ${theme.palette.divider}`,
    margin: theme.spacing(3, 0),
  },
  '& img': {
    maxWidth: '100%',
    borderRadius: theme.shape.borderRadius,
  },
  '& a': {
    color: theme.palette.primary.main,
    textDecoration: 'none',
    '&:hover': {
      textDecoration: 'underline',
    },
  },
  // Task list checkboxes (GFM)
  '& input[type="checkbox"]': {
    marginRight: theme.spacing(1),
  },
}))

// Custom components for react-markdown
const components = {
  a: ({ node, ...props }) => (
    <Link {...props} target="_blank" rel="noopener noreferrer" />
  ),
}

export default function MarkdownRenderer({ children, sx = {} }) {
  if (!children) return null
  
  return (
    <MarkdownContainer sx={sx}>
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        components={components}
      >
        {children}
      </ReactMarkdown>
    </MarkdownContainer>
  )
}
