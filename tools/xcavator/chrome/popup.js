async function targetTab() {
  const [active] = await chrome.tabs.query({ active: true, currentWindow: true });
  if (/^https?:\/\/(?:www\.)?(?:x|twitter)\.com\//.test(active?.url || "")) return active;
  const tabs = await chrome.tabs.query({ currentWindow: true });
  const tab = tabs.find(t => /^https?:\/\/(?:www\.)?(?:x|twitter)\.com\//.test(t.url || ""));
  if (!tab) throw new Error("Open an X profile or search in this Chrome window first");
  return tab;
}

async function leeTab() {
  const tabs = await chrome.tabs.query({ currentWindow: true });
  const tab = tabs.find(t => /^https:\/\/x\.com\/Jaemyung_Lee(?:\/|$)/i.test(t.url || '')) ||
    tabs.find(t => /^https:\/\/x\.com\/search\?/i.test(t.url || '') &&
      decodeURIComponent(t.url).includes('from:Jaemyung_Lee'));
  if (!tab) throw new Error('Open the Lee profile or collection search in this Zen window');
  return tab;
}

const status = document.createElement("pre");
status.style.cssText = "white-space:pre-wrap;color:white;font:13px sans-serif";
document.body.append(status);

async function run(file) {
  try {
    const tab = await targetTab();
    await chrome.scripting.executeScript({ target: { tabId: tab.id }, files: [file] });
    const [diagnostic] = await chrome.scripting.executeScript({
      target: { tabId: tab.id },
      func: () => ({
        articles: document.querySelectorAll('article').length,
        statusLinks: document.querySelectorAll('article a[href*="/status/"]').length,
        textNodes: document.querySelectorAll('article div[dir="auto"].whitespace-pre-wrap').length,
        state: window.xcavator && { username: window.xcavator.username,
          saved: window.xcavator.saved, errors: window.xcavator.errors,
          seen: window.xcavator.seen.size, lastError: window.xcavator.lastError },
      }),
    });
    status.textContent = `${file} in ${tab.url}\n${JSON.stringify(diagnostic.result)}`;
  } catch (error) {
    status.textContent = `${file}: ${error.message}`;
  }
}

const check = document.createElement("button");
check.textContent = "Check";
check.onclick = () => run("check.js");
document.body.append(check);

document.getElementById("start").addEventListener("click", async () => {
  await run("start.js");
});

document.getElementById("stop").addEventListener("click", async () => {
  await run("stop.js");
});

document.getElementById("start_scroll").addEventListener("click", async () => {
  await run("start-scroll.js");
});

document.getElementById("stop_scroll").addEventListener("click", async () => {
  await run("stop-scroll.js");
});

const batch = document.createElement("button");
batch.textContent = "Collect Lee presidency by month";
document.body.append(batch);
let cancelBatch = false;

const cancel = document.createElement("button");
cancel.textContent = "Cancel month run";
cancel.onclick = () => { cancelBatch = true; };
document.body.append(cancel);

const pause = ms => new Promise(resolve => setTimeout(resolve, ms));
async function captureMonth(tab, since, until) {
  const q = `from:Jaemyung_Lee since:${since} until:${until}`;
  const url = `https://x.com/search?q=${encodeURIComponent(q)}&src=typed_query&f=live`;
  await chrome.tabs.update(tab.id, { url });
  for (let i = 0; i < 40; i++) {
    await pause(500);
    const current = await chrome.tabs.get(tab.id);
    if (current.status === "complete" && current.url?.startsWith("https://x.com/search")) break;
  }
  await pause(1200);
  await chrome.scripting.executeScript({ target: { tabId: tab.id }, files: ["start.js"] });
  await chrome.scripting.executeScript({ target: { tabId: tab.id }, func: () => {
    window.xcavatorScrollDelay = 700;
    window.xcavatorScrollIdleLimit = 8;
  }});
  await chrome.scripting.executeScript({ target: { tabId: tab.id }, files: ["start-scroll.js"] });
  let last = null;
  for (let i = 0; i < 120; i++) {
    await pause(1000);
    const [result] = await chrome.scripting.executeScript({ target: { tabId: tab.id },
      func: () => ({ seen: window.xcavator?.seen.size || 0,
        saved: window.xcavator?.saved || 0, errors: window.xcavator?.errors || 0,
        scrolling: Boolean(window.scrollActive),
        page: location.href }),
    });
    last = result.result;
    status.textContent = `${since} to ${until}: ${JSON.stringify(last)}`;
    if (cancelBatch || !last.scrolling) break;
  }
  await chrome.scripting.executeScript({ target: { tabId: tab.id }, files: ["stop-scroll.js", "stop.js"] });
  return last;
}

batch.onclick = async () => {
  cancelBatch = false;
  batch.disabled = true;
  try {
    const tab = await leeTab();
    const begin = new Date("2025-06-04T00:00:00Z");
    const end = new Date();
    end.setUTCHours(0, 0, 0, 0);
    end.setUTCDate(end.getUTCDate() + 1);
    let completed = 0;
    for (let cursor = begin; cursor < end && !cancelBatch; ) {
      const next = new Date(Date.UTC(cursor.getUTCFullYear(), cursor.getUTCMonth() + 1, 1));
      const until = next < end ? next : end;
      const sinceText = cursor.toISOString().slice(0, 10);
      const untilText = until.toISOString().slice(0, 10);
      await captureMonth(tab, sinceText, untilText);
      completed++;
      cursor = until;
      await pause(1500);
    }
    status.textContent = `Lee month run ${cancelBatch ? "cancelled" : "finished"}: ${completed} months. Rebuild the CSV from raw captures.`;
  } catch (error) {
    status.textContent = `Lee month run failed: ${error.message}`;
  } finally {
    batch.disabled = false;
  }
};

const resolve = document.createElement('button');
resolve.textContent = 'Resolve shortened Lee posts';
document.body.append(resolve);
let cancelResolve = false;
const stopResolve = document.createElement('button');
stopResolve.textContent = 'Stop resolving';
stopResolve.onclick = () => { cancelResolve = true; };
document.body.append(stopResolve);

resolve.onclick = async () => {
  cancelResolve = false;
  resolve.disabled = true;
  try {
    const tab = await leeTab();
    const response = await fetch('http://127.0.0.1:3000/incomplete?username=Jaemyung_Lee');
    if (!response.ok) throw new Error(`Local server returned HTTP ${response.status}`);
    const { posts } = await response.json();
    let updated = 0;
    let failed = 0;
    let consecutiveFailures = 0;
    let stoppedAfterFailures = false;
    for (let i = 0; i < posts.length && !cancelResolve; i++) {
      const post = posts[i];
      try {
        await chrome.tabs.update(tab.id, { url: post.link });
        for (let attempt = 0; attempt < 30; attempt++) {
          await pause(400);
          const current = await chrome.tabs.get(tab.id);
          if (current.status === 'complete' && current.url?.includes(`/status/${post.id}`)) break;
        }
        await pause(650);
        await chrome.scripting.executeScript({ target: { tabId: tab.id }, files: ['start.js'] });
        let saved = false;
        for (let attempt = 0; attempt < 30; attempt++) {
          await pause(500);
          const [check] = await chrome.scripting.executeScript({ target: { tabId: tab.id },
            func: id => ({ seen: window.xcavator?.seen.has(id),
              saved: window.xcavator?.saved, error: window.xcavator?.lastError }), args: [post.id] });
          if (check.result.seen && check.result.saved) { saved = true; break; }
        }
        if (!saved) {
          const latest = await fetch('http://127.0.0.1:3000/incomplete?username=Jaemyung_Lee');
          const data = await latest.json();
          saved = !data.posts.some(item => item.id === post.id);
        }
        if (saved) {
          updated++;
          consecutiveFailures = 0;
        } else {
          failed++;
          consecutiveFailures++;
        }
      } catch (error) {
        failed++;
        consecutiveFailures++;
        console.warn('Could not resolve post', post.id, error);
      }
      status.textContent = `Full Lee posts: ${i + 1}/${posts.length}; saved ${updated}; unresolved ${failed}`;
      if (consecutiveFailures >= 6) {
        stoppedAfterFailures = true;
        break;
      }
      await pause(1200);
    }
    status.textContent = `Full Lee run ${cancelResolve || stoppedAfterFailures ? 'stopped' : 'finished'}: saved ${updated}, unresolved ${failed}, from ${posts.length} shortened posts.` +
      (stoppedAfterFailures ? ' X stopped returning post pages; retry when it loads again.' : '');
  } catch (error) {
    status.textContent = `Full Lee run failed: ${error.message}`;
  } finally {
    resolve.disabled = false;
  }
};
