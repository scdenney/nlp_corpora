chrome.runtime.onMessage.addListener((message, sender, respond) => {
  if (message?.type !== 'savePost' || !sender.tab?.url?.match(/^https?:\/\/(?:www\.)?(?:x|twitter)\.com\//)) return;
  fetch('http://127.0.0.1:3000/save-tweet', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(message.post),
  }).then(async response => {
    const body = await response.json().catch(() => ({}));
    respond({ ok: response.ok, status: response.status, body });
  }).catch(error => respond({ ok: false, error: error.message }));
  return true;
});
