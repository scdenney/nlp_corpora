// Xcavator content script: collect visible posts for one account from X's UI.
(() => {
  if (window.xcavator?.active) return;

  const pathHandle = location.pathname.split('/')[1];
  const searchHandle = decodeURIComponent(new URLSearchParams(location.search).get('q') || '')
    .match(/(?:^|\s)from:([A-Za-z0-9_]+)/i)?.[1];
  const username = searchHandle || pathHandle;
  if (!/^[A-Za-z0-9_]{1,30}$/.test(username) ||
      ['search', 'home', 'explore', 'i'].includes(username.toLowerCase())) {
    console.error('Xcavator: open a user profile or a from:account search first');
    return;
  }

  const state = { active: true, username, seen: new Set(), errors: 0, saved: 0 };
  window.xcavator = state;

  function extract(article) {
    if (article.parentElement?.closest('article')) return null; // quoted post
    const statusLink = Array.from(article.querySelectorAll('a[href*="/status/"]'))
      .find(a => a.closest('article') === article &&
        (a.getAttribute('href') || '').toLowerCase()
        .startsWith(`/${username.toLowerCase()}/status/`));
    if (!statusLink) return null;
    const relative = statusLink.getAttribute('href');
    const id = relative.match(/\/status\/(\d+)/)?.[1];
    if (!id) return null;

    // X currently renders post text in a whitespace-pre-wrap div; retain the
    // older data-testid selector for compatibility with its previous UI.
    const textNode = Array.from(article.querySelectorAll(
      '[data-testid="tweetText"], div[dir="auto"].whitespace-pre-wrap'))
      .find(node => node.closest('article') === article);
    if (!textNode) return null; // media-only post
    const text = textNode.innerText.trim();
    if (!text) return null;
    const timeNode = Array.from(article.querySelectorAll('time[datetime]'))
      .find(node => node.closest('article') === article);
    const timestamp = timeNode?.getAttribute('datetime') ||
      new Date(Number((BigInt(id) >> 22n) + 1288834974657n)).toISOString();
    const truncated = Array.from(article.querySelectorAll('a, button'))
      .some(el => el.closest('article') === article &&
        /^(show more|read more|더 보기|더보기|meer weergeven)$/i.test(el.innerText.trim()));
    return { id, date: timestamp, text, link: `https://x.com/${username}/status/${id}`,
      username, truncated };
  }

  async function save(post) {
    if (state.seen.has(post.id)) return;
    state.seen.add(post.id);
    try {
      const response = await chrome.runtime.sendMessage({ type: 'savePost', post });
      if (!response?.ok) throw new Error(response?.error || `HTTP ${response?.status}`);
      state.saved++;
    } catch (error) {
      state.seen.delete(post.id);
      state.errors++;
      state.lastError = String(error);
      console.error('Xcavator save failed', post.id, error);
    }
  }

  function scan() {
    if (!state.active) return;
    document.querySelectorAll('article').forEach(article => {
      const post = extract(article);
      if (post) save(post);
    });
  }

  const observer = new MutationObserver(scan);
  observer.observe(document.documentElement, { childList: true, subtree: true });
  const timer = setInterval(scan, 1500);
  state.stop = () => { state.active = false; observer.disconnect(); clearInterval(timer); };
  state.scan = scan;
  scan();
  console.log(`Xcavator collecting @${username}`);
})();
