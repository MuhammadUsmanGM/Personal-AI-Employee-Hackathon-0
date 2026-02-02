// Basic Email MCP Server for AI Employee
const express = require('express');
const nodemailer = require('nodemailer');
require('dotenv').config();

const app = express();
app.use(express.json());

// Configure email transport
let transporter = nodemailer.createTransporter({
  // Use environment-specific configuration
  service: 'gmail',
  auth: {
    user: process.env.EMAIL_USER,
    pass: process.env.EMAIL_PASS
  }
});

// MCP endpoints
app.post('/send_email', (req, res) => {
  const { to, subject, body, attachments } = req.body;

  const mailOptions = {
    from: process.env.EMAIL_USER,
    to: to,
    subject: subject,
    text: body,
    attachments: attachments || []
  };

  transporter.sendMail(mailOptions, (error, info) => {
    if (error) {
      console.error('Email error:', error);
      res.status(500).json({ error: error.message });
    } else {
      console.log('Email sent: ' + info.response);
      res.json({ success: true, messageId: info.messageId });
    }
  });
});

app.post('/draft_email', (req, res) => {
  const { to, subject, body } = req.body;

  // Store draft email (in a real implementation, this would save to a drafts folder)
  const draft = {
    to,
    subject,
    body,
    timestamp: new Date().toISOString()
  };

  res.json({ success: true, draftId: `draft_${Date.now()}`, draft });
});

app.post('/search_emails', (req, res) => {
  const { query } = req.body;

  // In a real implementation, this would connect to the email provider's API
  // For now, return empty results
  res.json({ success: true, emails: [], query });
});

const PORT = process.env.PORT || 8080;
app.listen(PORT, () => {
  console.log(`Email MCP Server running on port ${PORT}`);
});