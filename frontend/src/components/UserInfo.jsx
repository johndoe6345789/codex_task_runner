import React from 'react'
import {
  Box,
  Card,
  CardContent,
  Typography,
  Avatar,
  List,
  ListItem,
  ListItemText,
  Divider,
  Chip,
} from '@mui/material'
import { Person as PersonIcon } from '@mui/icons-material'

export default function UserInfo({ user, apiBase }) {
  if (!user) {
    return (
      <Box sx={{ textAlign: 'center', mt: 4 }}>
        <Typography color="text.secondary">Loading user info...</Typography>
      </Box>
    )
  }

  return (
    <Box sx={{ maxWidth: 600, mx: 'auto' }}>
      <Card>
        <CardContent>
          <Box sx={{ display: 'flex', alignItems: 'center', mb: 3 }}>
            <Avatar
              src={user.picture || user.image}
              sx={{ width: 64, height: 64, mr: 2 }}
            >
              <PersonIcon />
            </Avatar>
            <Box>
              <Typography variant="h5">
                {user.name || user.email || 'User'}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                {user.email}
              </Typography>
            </Box>
          </Box>

          <Divider sx={{ my: 2 }} />

          <List dense>
            {Object.entries(user).map(([key, value]) => {
              if (typeof value === 'object') return null
              return (
                <ListItem key={key}>
                  <ListItemText
                    primary={key}
                    secondary={String(value)}
                    primaryTypographyProps={{ variant: 'caption', color: 'text.secondary' }}
                  />
                </ListItem>
              )
            })}
          </List>
        </CardContent>
      </Card>

      <Card sx={{ mt: 2 }}>
        <CardContent>
          <Typography variant="subtitle2" gutterBottom>
            API Connection
          </Typography>
          <Chip label="Connected" color="success" size="small" />
          <Typography variant="caption" display="block" sx={{ mt: 1 }}>
            API Base: {apiBase || window.location.origin}
          </Typography>
        </CardContent>
      </Card>
    </Box>
  )
}
