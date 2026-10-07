const express = require('express');
const fs = require('fs');
const path = require('path');
const cors = require('cors');

const app = express();
const captureDir = process.env.XCAVATOR_OUTPUT_DIR || path.join(__dirname, 'captures');
fs.mkdirSync(captureDir, { recursive: true });
app.use(cors({ origin(origin, callback) {
  if (!origin || /^https:\/\/(?:x|twitter)\.com$/.test(origin) ||
      /^(?:moz|chrome)-extension:\/\/[a-z0-9-]+$/.test(origin)) {
    callback(null, true);
  } else {
    callback(new Error('Origin not allowed'));
  }
} }));
app.use(express.json({ limit: '1mb' }));

const seen = new Map();
function recordsFor(username) {
  const key = username.toLowerCase();
  if (!seen.has(key)) {
    const file = path.join(captureDir, `${key}.jsonl`);
    const records = new Map();
    if (fs.existsSync(file)) {
      for (const line of fs.readFileSync(file, 'utf8').split('\n')) {
        if (line.trim()) {
          const record = JSON.parse(line);
          records.set(record.id, record);
        }
      }
    }
    seen.set(key, records);
  }
  return seen.get(key);
}

app.get('/health', (_req, res) => res.json({ status: 'ok', captureDir }));
app.get('/incomplete', (req, res) => {
  const username = String(req.query.username || '');
  if (!/^[\w]{1,30}$/.test(username)) {
    return res.status(400).json({ error: 'Invalid username' });
  }
  const posts = [...recordsFor(username).values()]
    .filter(record => record.truncated)
    .sort((a, b) => a.date.localeCompare(b.date))
    .map(record => ({ id: record.id, link: record.link }));
  res.json({ username, posts });
});
app.post('/save-tweet', (req, res) => {
  const { id, date, text, link, username, truncated } = req.body || {};
  if (!/^\d{10,25}$/.test(id || '') || !/^\d{4}-\d\d-\d\dT/.test(date || '') ||
      typeof text !== 'string' || !text.trim() || !/^[\w]{1,30}$/.test(username || '')) {
    return res.status(400).json({ error: 'Invalid tweet fields' });
  }
  const match = /^https:\/\/(?:x|twitter)\.com\/([^/]+)\/status\/(\d+)/.exec(link || '');
  if (!match || match[1].toLowerCase() !== username.toLowerCase() || match[2] !== id) {
    return res.status(400).json({ error: 'Link does not match username and ID' });
  }
  const records = recordsFor(username);
  const earlier = records.get(id);
  if (earlier && !(earlier.truncated && !truncated) &&
      text.length <= earlier.text.length + 10) {
    return res.json({ status: 'duplicate' });
  }
  const file = path.join(captureDir, `${username.toLowerCase()}.jsonl`);
  const record = { id, date, text: text.trim(), link, username,
    truncated: Boolean(truncated),
    captured_at: new Date().toISOString() };
  fs.appendFileSync(file, JSON.stringify(record) + '\n');
  records.set(id, record);
  res.json({ status: earlier ? 'updated' : 'saved' });
});

app.listen(3000, '127.0.0.1', () => console.log(`Xcavator saving to ${captureDir}`));
