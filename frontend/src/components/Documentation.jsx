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
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Chip,
  Divider,
  Alert,
  Card,
  CardContent,
  IconButton,
  Tooltip,
  Link,
} from '@mui/material'
import {
  ExpandMore as ExpandMoreIcon,
  ContentCopy as CopyIcon,
  Api as ApiIcon,
  Code as CodeIcon,
  Terminal as TerminalIcon,
  Book as BookIcon,
  GitHub as GitHubIcon,
  Key as KeyIcon,
  Settings as SettingsIcon,
  Check as CheckIcon,
  Computer as ComputerIcon,
  List as ListIcon,
  Add as AddIcon,
  Search as SearchIcon,
  Palette as PaletteIcon,
  Language as LanguageIcon,
} from '@mui/icons-material'
import { LanguageContext } from '../main'

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
      
      {/* API Reference Tab */}
      <TabPanel value={tabValue} index={1}>
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
      <TabPanel value={tabValue} index={2}>
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
      <TabPanel value={tabValue} index={3}>
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
