import React, { useState, useContext } from 'react'
import {
  Box,
  Typography,
  Paper,
  Tabs,
  Tab,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Table,
  Chip,
  Divider,
  Alert,
  Card,
  CardContent,
  IconButton,
  Tooltip,
  Link,
} from '../fakemui'
import { LanguageContext } from '../main'

// Icons as SVG components
const ExpandMoreIcon = () => <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M16.59 8.59L12 13.17 7.41 8.59 6 10l6 6 6-6z"/></svg>
const CopyIcon = () => <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M16 1H4c-1.1 0-2 .9-2 2v14h2V3h12V1zm3 4H8c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h11c1.1 0 2-.9 2-2V7c0-1.1-.9-2-2-2zm0 16H8V7h11v14z"/></svg>
const ApiIcon = () => <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M14 12l-2 2-2-2 2-2 2 2zm-2-6l2.12 2.12 2.5-2.5L12 1 7.38 5.62l2.5 2.5L12 6zm-6 6l2.12-2.12-2.5-2.5L1 12l4.62 4.62 2.5-2.5L6 12zm12 0l-2.12 2.12 2.5 2.5L23 12l-4.62-4.62-2.5 2.5L18 12zm-6 6l-2.12-2.12-2.5 2.5L12 23l4.62-4.62-2.5-2.5L12 18z"/></svg>
const CodeIcon = () => <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M9.4 16.6L4.8 12l4.6-4.6L8 6l-6 6 6 6 1.4-1.4zm5.2 0l4.6-4.6-4.6-4.6L16 6l6 6-6 6-1.4-1.4z"/></svg>
const TerminalIcon = () => <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M20 19V7H4v12h16m0-16a2 2 0 012 2v14a2 2 0 01-2 2H4a2 2 0 01-2-2V5a2 2 0 012-2h16m-7 14v-2h5v2h-5m-3.42-4L5.57 9H8.4l3.3 3.3c.39.39.39 1.03 0 1.42L8.42 17H5.59l4-4z"/></svg>
const BookIcon = () => <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M18 2H6c-1.1 0-2 .9-2 2v16c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zM6 4h5v8l-2.5-1.5L6 12V4z"/></svg>
const GitHubIcon = () => <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M12 1.27a11 11 0 00-3.48 21.46c.55.09.73-.28.73-.55v-1.84c-3.03.64-3.67-1.46-3.67-1.46-.55-1.29-1.28-1.65-1.28-1.65-.92-.65.1-.65.1-.65 1.1 0 1.73 1.1 1.73 1.1.92 1.65 2.57 1.2 3.21.92a2.16 2.16 0 01.64-1.47c-2.47-.27-5.04-1.19-5.04-5.5 0-1.1.46-2.1 1.2-2.84a3.76 3.76 0 010-2.93s.91-.28 3.11 1.1c1.8-.49 3.7-.49 5.5 0 2.1-1.38 3.02-1.1 3.02-1.1a3.76 3.76 0 010 2.93c.83.74 1.2 1.74 1.2 2.94 0 4.21-2.57 5.13-5.04 5.4.45.37.82.92.82 2.02v3.03c0 .27.1.64.73.55A11 11 0 0012 1.27"/></svg>
const KeyIcon = () => <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M12.65 10C11.83 7.67 9.61 6 7 6c-3.31 0-6 2.69-6 6s2.69 6 6 6c2.61 0 4.83-1.67 5.65-4H17v4h4v-4h2v-4H12.65zM7 14c-1.1 0-2-.9-2-2s.9-2 2-2 2 .9 2 2-.9 2-2 2z"/></svg>
const SettingsIcon = () => <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M19.14 12.94c.04-.31.06-.63.06-.94 0-.31-.02-.63-.06-.94l2.03-1.58c.18-.14.23-.41.12-.61l-1.92-3.32c-.12-.22-.37-.29-.59-.22l-2.39.96c-.5-.38-1.03-.7-1.62-.94l-.36-2.54c-.04-.24-.24-.41-.48-.41h-3.84c-.24 0-.43.17-.47.41l-.36 2.54c-.59.24-1.13.57-1.62.94l-2.39-.96c-.22-.08-.47 0-.59.22L2.74 8.87c-.12.21-.08.47.12.61l2.03 1.58c-.04.31-.06.63-.06.94s.02.63.06.94l-2.03 1.58c-.18.14-.23.41-.12.61l1.92 3.32c.12.22.37.29.59.22l2.39-.96c.5.38 1.03.7 1.62.94l.36 2.54c.05.24.24.41.48.41h3.84c.24 0 .44-.17.47-.41l.36-2.54c.59-.24 1.13-.56 1.62-.94l2.39.96c.22.08.47 0 .59-.22l1.92-3.32c.12-.22.07-.47-.12-.61l-2.01-1.58zM12 15.6c-1.98 0-3.6-1.62-3.6-3.6s1.62-3.6 3.6-3.6 3.6 1.62 3.6 3.6-1.62 3.6-3.6 3.6z"/></svg>
const CheckIcon = () => <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"/></svg>
const ComputerIcon = () => <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M20 18c1.1 0 1.99-.9 1.99-2L22 6c0-1.1-.9-2-2-2H4c-1.1 0-2 .9-2 2v10c0 1.1.9 2 2 2H0v2h24v-2h-4zM4 6h16v10H4V6z"/></svg>
const ListIcon = () => <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M3 13h2v-2H3v2zm0 4h2v-2H3v2zm0-8h2V7H3v2zm4 4h14v-2H7v2zm0 4h14v-2H7v2zM7 7v2h14V7H7z"/></svg>
const AddIcon = () => <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z"/></svg>
const SearchIcon = () => <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M15.5 14h-.79l-.28-.27C15.41 12.59 16 11.11 16 9.5 16 5.91 13.09 3 9.5 3S3 5.91 3 9.5 5.91 16 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"/></svg>
const PaletteIcon = () => <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M12 3c-4.97 0-9 4.03-9 9s4.03 9 9 9c.83 0 1.5-.67 1.5-1.5 0-.39-.15-.74-.39-1.01-.23-.26-.38-.61-.38-.99 0-.83.67-1.5 1.5-1.5H16c2.76 0 5-2.24 5-5 0-4.42-4.03-8-9-8zm-5.5 9c-.83 0-1.5-.67-1.5-1.5S5.67 9 6.5 9 8 9.67 8 10.5 7.33 12 6.5 12zm3-4C8.67 8 8 7.33 8 6.5S8.67 5 9.5 5s1.5.67 1.5 1.5S10.33 8 9.5 8zm5 0c-.83 0-1.5-.67-1.5-1.5S13.67 5 14.5 5s1.5.67 1.5 1.5S15.33 8 14.5 8zm3 4c-.83 0-1.5-.67-1.5-1.5S16.67 9 17.5 9s1.5.67 1.5 1.5-.67 1.5-1.5 1.5z"/></svg>
const LanguageIcon = () => <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M11.99 2C6.47 2 2 6.48 2 12s4.47 10 9.99 10C17.52 22 22 17.52 22 12S17.52 2 11.99 2zm6.93 6h-2.95c-.32-1.25-.78-2.45-1.38-3.56 1.84.63 3.37 1.91 4.33 3.56zM12 4.04c.83 1.2 1.48 2.53 1.91 3.96h-3.82c.43-1.43 1.08-2.76 1.91-3.96zM4.26 14C4.1 13.36 4 12.69 4 12s.1-1.36.26-2h3.38c-.08.66-.14 1.32-.14 2 0 .68.06 1.34.14 2H4.26zm.82 2h2.95c.32 1.25.78 2.45 1.38 3.56-1.84-.63-3.37-1.9-4.33-3.56zm2.95-8H5.08c.96-1.66 2.49-2.93 4.33-3.56C8.81 5.55 8.35 6.75 8.03 8zM12 19.96c-.83-1.2-1.48-2.53-1.91-3.96h3.82c-.43 1.43-1.08 2.76-1.91 3.96zM14.34 14H9.66c-.09-.66-.16-1.32-.16-2 0-.68.07-1.35.16-2h4.68c.09.65.16 1.32.16 2 0 .68-.07 1.34-.16 2zm.25 5.56c.6-1.11 1.06-2.31 1.38-3.56h2.95c-.96 1.65-2.49 2.93-4.33 3.56zM16.36 14c.08-.66.14-1.32.14-2 0-.68-.06-1.34-.14-2h3.38c.16.64.26 1.31.26 2s-.1 1.36-.26 2h-3.38z"/></svg>

function TabPanel({ children, value, index }) {
  return (
    <Box role="tabpanel" hidden={value !== index} sx={{ py: 2 }}>
      {value === index && children}
    </Box>
  )
}

function CodeBlock({ code, language = 'bash' }) {
  const [copied, setCopied] = useState(false)
  
  const handleCopy = () => {
    navigator.clipboard.writeText(code)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }
  
  return (
    <Paper
      sx={{
        p: 2,
        bgcolor: 'grey.900',
        borderRadius: 1,
        position: 'relative',
        fontFamily: 'monospace',
        overflow: 'auto',
      }}
    >
      <Tooltip title={copied ? 'Copied!' : 'Copy'}>
        <IconButton
          size="small"
          onClick={handleCopy}
          sx={{ position: 'absolute', top: 8, right: 8, color: 'grey.400' }}
        >
          {copied ? <CheckIcon fontSize="small" /> : <CopyIcon fontSize="small" />}
        </IconButton>
      </Tooltip>
      <Typography
        component="pre"
        sx={{
          m: 0,
          color: 'grey.100',
          fontSize: '0.85rem',
          lineHeight: 1.6,
          whiteSpace: 'pre-wrap',
          wordBreak: 'break-word',
        }}
      >
        {code}
      </Typography>
    </Paper>
  )
}

function EndpointRow({ method, path, description }) {
  const methodColors = {
    GET: 'success',
    POST: 'primary',
    PUT: 'warning',
    DELETE: 'error',
  }
  
  return (
    <TableRow hover>
      <TableCell>
        <Chip
          label={method}
          size="small"
          color={methodColors[method] || 'default'}
          sx={{ fontFamily: 'monospace', fontWeight: 'bold' }}
        />
      </TableCell>
      <TableCell>
        <Typography variant="body2" sx={{ fontFamily: 'monospace' }}>
          {path}
        </Typography>
      </TableCell>
      <TableCell>{description}</TableCell>
    </TableRow>
  )
}

export default function Documentation() {
  const [tabValue, setTabValue] = useState(0)
  const { t } = useContext(LanguageContext)
  
  return (
    <Box>
      <Typography variant="h4" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
        <BookIcon /> {t('documentation') || 'Documentation'}
      </Typography>
      
      <Paper sx={{ mb: 3 }}>
        <Tabs
          value={tabValue}
          onChange={(e, v) => setTabValue(v)}
          variant="scrollable"
          scrollButtons="auto"
          sx={{ borderBottom: 1, borderColor: 'divider' }}
        >
          <Tab icon={<TerminalIcon />} label={t('gettingStarted') || 'Getting Started'} iconPosition="start" />
          <Tab icon={<ComputerIcon />} label={t('usingTheUI') || 'Using the UI'} iconPosition="start" />
          <Tab icon={<ApiIcon />} label={t('apiReference') || 'API Reference'} iconPosition="start" />
          <Tab icon={<CodeIcon />} label={t('cliCommands') || 'CLI Commands'} iconPosition="start" />
          <Tab icon={<KeyIcon />} label={t('authentication') || 'Authentication'} iconPosition="start" />
        </Tabs>
      </Paper>
      
      {/* Getting Started Tab */}
      <TabPanel value={tabValue} index={0}>
        <Box sx={{ display: 'flex', flexDirection: 'column', gap: 3 }}>
          <Alert severity="info" icon={<BookIcon />}>
            {t('docsIntro') || 'Codex Task Runner is a tool for managing OpenAI Codex tasks via CLI and web interface.'}
          </Alert>
          
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                <SettingsIcon /> {t('installation') || 'Installation'}
              </Typography>
              <Divider sx={{ mb: 2 }} />
              
              <Typography variant="subtitle2" color="text.secondary" gutterBottom>
                1. Clone and install:
              </Typography>
              <CodeBlock code={`git clone https://github.com/sandover/obi.git
cd obi
python -m venv venv
source venv/bin/activate
pip install -e .`} />
              
              <Typography variant="subtitle2" color="text.secondary" gutterBottom sx={{ mt: 2 }}>
                2. Set up environment:
              </Typography>
              <CodeBlock code={`cp env.template .env
# Edit .env with your Codex session cookie`} />
              
              <Typography variant="subtitle2" color="text.secondary" gutterBottom sx={{ mt: 2 }}>
                3. Verify installation:
              </Typography>
              <CodeBlock code={`codex-runner ping`} />
            </CardContent>
          </Card>
          
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                <GitHubIcon /> {t('quickStart') || 'Quick Start'}
              </Typography>
              <Divider sx={{ mb: 2 }} />
              
              <Typography variant="body2" paragraph>
                {t('quickStartDesc') || 'Common workflows to get you started:'}
              </Typography>
              
              <Typography variant="subtitle2" color="text.secondary" gutterBottom>
                List your tasks:
              </Typography>
              <CodeBlock code={`codex-runner tasks`} />
              
              <Typography variant="subtitle2" color="text.secondary" gutterBottom sx={{ mt: 2 }}>
                Create a new task:
              </Typography>
              <CodeBlock code={`codex-runner prompt "Add unit tests for auth module"`} />
              
              <Typography variant="subtitle2" color="text.secondary" gutterBottom sx={{ mt: 2 }}>
                View task details:
              </Typography>
              <CodeBlock code={`codex-runner task 1  # Use alias number from list`} />
              
              <Typography variant="subtitle2" color="text.secondary" gutterBottom sx={{ mt: 2 }}>
                Get the patch/diff:
              </Typography>
              <CodeBlock code={`codex-runner patch 1`} />
              
              <Typography variant="subtitle2" color="text.secondary" gutterBottom sx={{ mt: 2 }}>
                Start the web UI:
              </Typography>
              <CodeBlock code={`codex-runner serve
# Open http://localhost:8642`} />
            </CardContent>
          </Card>
        </Box>
      </TabPanel>
      
      {/* Using the UI Tab */}
      <TabPanel value={tabValue} index={1}>
        <Box sx={{ display: 'flex', flexDirection: 'column', gap: 3 }}>
          <Alert severity="info" icon={<ComputerIcon />}>
            {t('uiIntro') || 'The web interface provides a visual way to manage your Codex tasks, view diffs, and create PRs.'}
          </Alert>
          
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                <ListIcon /> {t('taskListSection') || 'Task List'}
              </Typography>
              <Divider sx={{ mb: 2 }} />
              
              <Typography variant="body2" paragraph>
                The main view shows all your Codex tasks. Each task card displays:
              </Typography>
              
              <Box component="ul" sx={{ pl: 2, '& li': { mb: 1 } }}>
                <li><Typography variant="body2"><strong>Title</strong> — The task description or auto-generated title</Typography></li>
                <li><Typography variant="body2"><strong>Repository</strong> — The GitHub repo the task targets</Typography></li>
                <li><Typography variant="body2"><strong>Status</strong> — Current state (pending, running, completed, failed)</Typography></li>
                <li><Typography variant="body2"><strong>Alias #</strong> — Short number for CLI reference (e.g., task 1, task 2)</Typography></li>
                <li><Typography variant="body2"><strong>PR Link</strong> — Direct link to the pull request if created</Typography></li>
              </Box>
              
              <Typography variant="subtitle2" color="text.secondary" gutterBottom sx={{ mt: 2 }}>
                Filtering Tasks:
              </Typography>
              <Typography variant="body2" paragraph>
                Use the <strong>Filter</strong> dropdown to switch between:
              </Typography>
              <Box component="ul" sx={{ pl: 2, '& li': { mb: 0.5 } }}>
                <li><Typography variant="body2"><Chip label="Current" size="small" /> — Active tasks (default)</Typography></li>
                <li><Typography variant="body2"><Chip label="Archived" size="small" /> — Completed/archived tasks</Typography></li>
                <li><Typography variant="body2"><Chip label="All" size="small" /> — Everything</Typography></li>
              </Box>
            </CardContent>
          </Card>
          
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                <BookIcon /> {t('taskDetailSection') || 'Task Detail View'}
              </Typography>
              <Divider sx={{ mb: 2 }} />
              
              <Typography variant="body2" paragraph>
                Click any task to see its full details. The detail view has several tabs:
              </Typography>
              
              <Accordion>
                <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                  <Typography><strong>Details</strong> — Task metadata and summary</Typography>
                </AccordionSummary>
                <AccordionDetails>
                  <Typography variant="body2">
                    Shows the task ID, creation date, repository, branch, and status. 
                    If a PR was created, you'll see links to it here.
                  </Typography>
                </AccordionDetails>
              </Accordion>
              
              <Accordion>
                <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                  <Typography><strong>Turns</strong> — Conversation history</Typography>
                </AccordionSummary>
                <AccordionDetails>
                  <Typography variant="body2">
                    View the back-and-forth between you and Codex. Each "turn" represents 
                    either your prompt (user turn) or Codex's response (assistant turn).
                    The current turn shows the latest code changes.
                  </Typography>
                </AccordionDetails>
              </Accordion>
              
              <Accordion>
                <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                  <Typography><strong>Patch</strong> — View the diff</Typography>
                </AccordionSummary>
                <AccordionDetails>
                  <Typography variant="body2">
                    See the actual code changes in unified diff format. 
                    Click <strong>Load Patch</strong> to fetch the latest diff.
                    Use the copy button to grab the patch for local application.
                  </Typography>
                </AccordionDetails>
              </Accordion>
              
              <Box sx={{ mt: 2, p: 2, bgcolor: 'action.hover', borderRadius: 1 }}>
                <Typography variant="subtitle2" gutterBottom>💡 Pro Tips:</Typography>
                <Typography variant="body2">
                  • Click <strong>Create PR</strong> to open a pull request directly from the UI<br />
                  • Use <strong>Archive</strong> to move completed tasks out of your current list<br />
                  • Enable <strong>Nerd Mode</strong> to see raw JSON and task IDs
                </Typography>
              </Box>
            </CardContent>
          </Card>
          
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                <AddIcon /> {t('newTaskSection') || 'Creating New Tasks'}
              </Typography>
              <Divider sx={{ mb: 2 }} />
              
              <Typography variant="body2" paragraph>
                Click <strong>New Task</strong> in the sidebar to create a task:
              </Typography>
              
              <Box component="ol" sx={{ pl: 2, '& li': { mb: 1 } }}>
                <li><Typography variant="body2">Enter your prompt describing what you want Codex to do</Typography></li>
                <li><Typography variant="body2">Optionally specify a target branch (defaults to "main")</Typography></li>
                <li><Typography variant="body2">Set "Best Of" &gt; 1 to generate multiple solutions</Typography></li>
                <li><Typography variant="body2">Click <strong>Create Task</strong> to submit</Typography></li>
              </Box>
              
              <Alert severity="success" sx={{ mt: 2 }}>
                <Typography variant="body2">
                  <strong>Tip:</strong> Be specific! Include file paths, function names, or code snippets 
                  for better results.
                </Typography>
              </Alert>
            </CardContent>
          </Card>
          
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                <SearchIcon /> {t('searchSection') || 'Search'}
              </Typography>
              <Divider sx={{ mb: 2 }} />
              
              <Typography variant="body2" paragraph>
                Press <Chip label="⌘K" size="small" sx={{ fontFamily: 'monospace' }} /> (or <Chip label="Ctrl+K" size="small" sx={{ fontFamily: 'monospace' }} />) 
                to open the search dialog. You can search across:
              </Typography>
              
              <Box component="ul" sx={{ pl: 2, '& li': { mb: 0.5 } }}>
                <li><Typography variant="body2">Task titles</Typography></li>
                <li><Typography variant="body2">Repository names</Typography></li>
                <li><Typography variant="body2">Branch names</Typography></li>
                <li><Typography variant="body2">Task IDs</Typography></li>
              </Box>
            </CardContent>
          </Card>
          
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                <PaletteIcon /> {t('customizationSection') || 'Customization'}
              </Typography>
              <Divider sx={{ mb: 2 }} />
              
              <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                <Box>
                  <Typography variant="subtitle2" sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                    <PaletteIcon fontSize="small" /> Themes
                  </Typography>
                  <Typography variant="body2">
                    Click the theme selector in the sidebar to choose from multiple color schemes: 
                    Dark, Light, Solarized Dark, Monokai, Nord, and Dracula.
                  </Typography>
                </Box>
                
                <Divider />
                
                <Box>
                  <Typography variant="subtitle2" sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                    <LanguageIcon fontSize="small" /> Languages
                  </Typography>
                  <Typography variant="body2">
                    The UI supports 19 languages. Click the language selector to switch.
                    Available: English, Spanish, French, German, Japanese, Chinese, Korean, Russian, 
                    Arabic, Hindi, Portuguese, Italian, Dutch, Polish, Swedish, Turkish, Ukrainian, 
                    Vietnamese, and Thai.
                  </Typography>
                </Box>
                
                <Divider />
                
                <Box>
                  <Typography variant="subtitle2" sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                    <CodeIcon fontSize="small" /> Nerd Mode
                  </Typography>
                  <Typography variant="body2">
                    Toggle Nerd Mode to see technical details: raw JSON responses, 
                    full task IDs, API request/response info, and debug data.
                  </Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Box>
      </TabPanel>
      
      {/* API Reference Tab */}
      <TabPanel value={tabValue} index={2}>
        <Box sx={{ display: 'flex', flexDirection: 'column', gap: 3 }}>
          <Alert severity="warning">
            {t('apiDisclaimer') || 'These endpoints are observed from browser network traffic. Exact schemas may vary.'}
          </Alert>
          
          <Accordion defaultExpanded>
            <AccordionSummary expandIcon={<ExpandMoreIcon />}>
              <Typography variant="h6">WHAM (Codex) Endpoints</Typography>
            </AccordionSummary>
            <AccordionDetails>
              <Typography variant="body2" color="text.secondary" paragraph>
                Base URL: <code>https://chatgpt.com/backend-api</code>
              </Typography>
              <TableContainer>
                <Table size="small">
                  <TableHead>
                    <TableRow>
                      <TableCell width={100}>Method</TableCell>
                      <TableCell>Path</TableCell>
                      <TableCell>Description</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    <EndpointRow method="GET" path="/wham/tasks/list" description="List tasks (with ?limit=N&task_filter=current|archived|all)" />
                    <EndpointRow method="POST" path="/wham/tasks" description="Create new task (send prompt)" />
                    <EndpointRow method="GET" path="/wham/tasks/{task_id}" description="Get task detail" />
                    <EndpointRow method="POST" path="/wham/tasks/{task_id}/archive" description="Archive a task" />
                    <EndpointRow method="GET" path="/wham/tasks/{task_id}/turns" description="List turns for a task" />
                    <EndpointRow method="GET" path="/wham/tasks/{task_id}/turns/{turn_id}/pr" description="Get PR status for a turn" />
                    <EndpointRow method="POST" path="/wham/tasks/{task_id}/turns/{turn_id}/pr" description="Create PR for a turn" />
                    <EndpointRow method="GET" path="/wham/environments" description="List environments" />
                    <EndpointRow method="GET" path="/wham/environments/recent" description="Recently used environments" />
                    <EndpointRow method="GET" path="/wham/usage" description="Usage statistics" />
                  </TableBody>
                </Table>
              </TableContainer>
            </AccordionDetails>
          </Accordion>
          
          <Accordion>
            <AccordionSummary expandIcon={<ExpandMoreIcon />}>
              <Typography variant="h6">Task Creation Request</Typography>
            </AccordionSummary>
            <AccordionDetails>
              <Typography variant="body2" color="text.secondary" gutterBottom>
                POST /backend-api/wham/tasks
              </Typography>
              <CodeBlock code={`{
  "new_task": {
    "environment_id": "<environment_id>",
    "branch": "main",
    "run_environment_in_qa_mode": false
  },
  "metadata": {
    "best_of_n": 1
  },
  "input_items": [
    {
      "type": "message",
      "role": "user",
      "content": [
        {
          "content_type": "text",
          "text": "Your prompt here"
        }
      ]
    }
  ]
}`} />
            </AccordionDetails>
          </Accordion>
          
          <Accordion>
            <AccordionSummary expandIcon={<ExpandMoreIcon />}>
              <Typography variant="h6">ID Naming Conventions</Typography>
            </AccordionSummary>
            <AccordionDetails>
              <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                <Box>
                  <Typography variant="subtitle2" color="primary">Task IDs</Typography>
                  <Typography variant="body2" sx={{ fontFamily: 'monospace' }}>
                    task_e_69502ab28bcc8331a29f727e77deb37c
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Format: task_e_&lt;hex_id&gt; — The "_e_" likely means "entity"
                  </Typography>
                </Box>
                <Divider />
                <Box>
                  <Typography variant="subtitle2" color="primary">Turn IDs</Typography>
                  <Typography variant="body2" sx={{ fontFamily: 'monospace' }}>
                    task_e_xxx~assttrn_e_yyy
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Format: &lt;task_id&gt;~&lt;turn_type&gt;trn_e_&lt;hex_id&gt;
                    <br />• assttrn = assistant turn (Codex's response)
                    <br />• usertrn = user turn (your prompt)
                  </Typography>
                </Box>
              </Box>
            </AccordionDetails>
          </Accordion>
          
          <Accordion>
            <AccordionSummary expandIcon={<ExpandMoreIcon />}>
              <Typography variant="h6">Account Endpoints</Typography>
            </AccordionSummary>
            <AccordionDetails>
              <TableContainer>
                <Table size="small">
                  <TableHead>
                    <TableRow>
                      <TableCell width={100}>Method</TableCell>
                      <TableCell>Path</TableCell>
                      <TableCell>Description</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    <EndpointRow method="GET" path="/me" description="Current user info" />
                    <EndpointRow method="GET" path="/accounts/check/v4-2023-04-27" description="Account status" />
                    <EndpointRow method="GET" path="/settings/user" description="User settings" />
                    <EndpointRow method="GET" path="/subscriptions" description="Subscription info" />
                  </TableBody>
                </Table>
              </TableContainer>
            </AccordionDetails>
          </Accordion>
        </Box>
      </TabPanel>
      
      {/* CLI Commands Tab */}
      <TabPanel value={tabValue} index={3}>
        <Box sx={{ display: 'flex', flexDirection: 'column', gap: 3 }}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>Core Commands</Typography>
              <Divider sx={{ mb: 2 }} />
              
              <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                <Box>
                  <Chip label="tasks" color="primary" size="small" sx={{ fontFamily: 'monospace' }} />
                  <Typography variant="body2" sx={{ mt: 0.5 }}>
                    List all Codex tasks
                  </Typography>
                  <CodeBlock code={`codex-runner tasks
codex-runner tasks --filter archived
codex-runner tasks --limit 50`} />
                </Box>
                
                <Divider />
                
                <Box>
                  <Chip label="task" color="primary" size="small" sx={{ fontFamily: 'monospace' }} />
                  <Typography variant="body2" sx={{ mt: 0.5 }}>
                    Get details for a specific task
                  </Typography>
                  <CodeBlock code={`codex-runner task 1          # By alias
codex-runner task task_e_xxx  # By full ID`} />
                </Box>
                
                <Divider />
                
                <Box>
                  <Chip label="prompt" color="primary" size="small" sx={{ fontFamily: 'monospace' }} />
                  <Typography variant="body2" sx={{ mt: 0.5 }}>
                    Create a new task from a prompt
                  </Typography>
                  <CodeBlock code={`codex-runner prompt "Add login form validation"
codex-runner prompt "Fix bug in auth" --branch develop
codex-runner prompt "Refactor API" --best-of 3`} />
                </Box>
                
                <Divider />
                
                <Box>
                  <Chip label="patch" color="primary" size="small" sx={{ fontFamily: 'monospace' }} />
                  <Typography variant="body2" sx={{ mt: 0.5 }}>
                    Get the diff/patch for a task
                  </Typography>
                  <CodeBlock code={`codex-runner patch 1
codex-runner p 1  # Short alias`} />
                </Box>
                
                <Divider />
                
                <Box>
                  <Chip label="turns" color="primary" size="small" sx={{ fontFamily: 'monospace' }} />
                  <Typography variant="body2" sx={{ mt: 0.5 }}>
                    List conversation turns for a task
                  </Typography>
                  <CodeBlock code={`codex-runner turns 1`} />
                </Box>
              </Box>
            </CardContent>
          </Card>
          
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>Server Commands</Typography>
              <Divider sx={{ mb: 2 }} />
              
              <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                <Box>
                  <Chip label="serve" color="success" size="small" sx={{ fontFamily: 'monospace' }} />
                  <Typography variant="body2" sx={{ mt: 0.5 }}>
                    Start the web API server
                  </Typography>
                  <CodeBlock code={`codex-runner serve
codex-runner serve --port 8080
codex-runner serve --host 0.0.0.0`} />
                </Box>
                
                <Divider />
                
                <Box>
                  <Chip label="ui" color="success" size="small" sx={{ fontFamily: 'monospace' }} />
                  <Typography variant="body2" sx={{ mt: 0.5 }}>
                    Launch the native PyQt6 desktop UI
                  </Typography>
                  <CodeBlock code={`codex-runner ui`} />
                </Box>
              </Box>
            </CardContent>
          </Card>
          
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>Automation Commands</Typography>
              <Divider sx={{ mb: 2 }} />
              
              <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                <Box>
                  <Chip label="yolo" color="warning" size="small" sx={{ fontFamily: 'monospace' }} />
                  <Typography variant="body2" sx={{ mt: 0.5 }}>
                    Full automation: Create PRs and merge all tasks
                  </Typography>
                  <CodeBlock code={`codex-runner yolo  # ⚠️ Use with caution!`} />
                </Box>
                
                <Divider />
                
                <Box>
                  <Chip label="run" color="warning" size="small" sx={{ fontFamily: 'monospace' }} />
                  <Typography variant="body2" sx={{ mt: 0.5 }}>
                    Process tasks with configurable merge behavior
                  </Typography>
                  <CodeBlock code={`codex-runner run
codex-runner run --no-merge`} />
                </Box>
                
                <Divider />
                
                <Box>
                  <Chip label="ping" color="info" size="small" sx={{ fontFamily: 'monospace' }} />
                  <Typography variant="body2" sx={{ mt: 0.5 }}>
                    Test API connectivity
                  </Typography>
                  <CodeBlock code={`codex-runner ping`} />
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Box>
      </TabPanel>
      
      {/* Authentication Tab */}
      <TabPanel value={tabValue} index={4}>
        <Box sx={{ display: 'flex', flexDirection: 'column', gap: 3 }}>
          <Alert severity="warning">
            {t('authWarning') || 'Session cookies expire periodically. You may need to refresh your cookie from the browser.'}
          </Alert>
          
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                <KeyIcon /> Setting Up Authentication
              </Typography>
              <Divider sx={{ mb: 2 }} />
              
              <Typography variant="body2" paragraph>
                The Codex API requires authentication via session cookies. Here's how to set it up:
              </Typography>
              
              <Typography variant="subtitle2" color="text.secondary" gutterBottom>
                1. Get your session cookie:
              </Typography>
              <Typography variant="body2" paragraph>
                • Open <Link href="https://chatgpt.com/codex" target="_blank">chatgpt.com/codex</Link> in your browser
                <br />• Open DevTools (F12) → Application → Cookies
                <br />• Copy the value of <code>__Secure-next-auth.session-token</code>
              </Typography>
              
              <Typography variant="subtitle2" color="text.secondary" gutterBottom>
                2. Create your .env file:
              </Typography>
              <CodeBlock code={`# Copy from env.template
cp env.template .env

# Edit with your cookie
nano .env`} />
              
              <Typography variant="subtitle2" color="text.secondary" gutterBottom sx={{ mt: 2 }}>
                3. .env format:
              </Typography>
              <CodeBlock code={`COOKIE=__Secure-next-auth.session-token=your_long_cookie_value_here`} />
            </CardContent>
          </Card>
          
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>Troubleshooting</Typography>
              <Divider sx={{ mb: 2 }} />
              
              <Accordion>
                <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                  <Typography>401 Unauthorized errors</Typography>
                </AccordionSummary>
                <AccordionDetails>
                  <Typography variant="body2">
                    • Your session cookie may have expired — refresh it from the browser
                    <br />• Make sure the cookie includes the full <code>__Secure-next-auth.session-token=</code> prefix
                    <br />• Check that there are no extra spaces or newlines in your .env file
                  </Typography>
                </AccordionDetails>
              </Accordion>
              
              <Accordion>
                <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                  <Typography>Connection refused</Typography>
                </AccordionSummary>
                <AccordionDetails>
                  <Typography variant="body2">
                    • Make sure the API server is running (<code>codex-runner serve</code>)
                    <br />• Check the port (default: 8642)
                    <br />• Verify no firewall is blocking the connection
                  </Typography>
                </AccordionDetails>
              </Accordion>
              
              <Accordion>
                <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                  <Typography>No tasks found</Typography>
                </AccordionSummary>
                <AccordionDetails>
                  <Typography variant="body2">
                    • Check if you have any tasks on <Link href="https://chatgpt.com/codex" target="_blank">chatgpt.com/codex</Link>
                    <br />• Try changing the filter to "all" instead of "current"
                    <br />• Verify your GitHub is connected in Codex settings
                  </Typography>
                </AccordionDetails>
              </Accordion>
            </CardContent>
          </Card>
        </Box>
      </TabPanel>
    </Box>
  )
}
