# Xcavator collection adapter

This is an adapted copy of [David Kwakernaak's Xcavator](https://github.com/dvdkwak/Xcavator), based on upstream commit `b35daa5`. It reads visible X pages in Chrome or Zen and posts records to a local server. It does not use X's developer API.

The adaptation handles the current X page markup, saves every visible post immediately, separates accounts, checks that a post link belongs to the selected account, and deduplicates IDs across runs. Raw captures are JSONL files in `data/presidential_twitter/raw/`; they are included with the corpus so the combined CSV can be rebuilt.

## Run

```bash
cd tools/xcavator
npm install
XCAVATOR_OUTPUT_DIR="$PWD/../../data/presidential_twitter/raw" npm start
```

In a signed-in Chrome window, visit `chrome://extensions`, enable Developer Mode, and load `tools/xcavator/chrome` as an unpacked extension. In **Zen or Firefox**, open `about:debugging#/runtime/this-firefox`, choose **Load Temporary Add-on**, and select `tools/xcavator/chrome/manifest.json`. The extension in Zen is temporary and must be loaded again after restarting the browser. Its manifest supports both Chrome's service worker and Firefox's background script.

Open one target profile or a `from:account` search in the same browser window. Click the Xcavator icon, then **Start** and **Start Scroll**. If the icon popup is inaccessible, open the extension's `popup.html` URL in another tab of the **same window**; it will target the X tab. The scroll script stops after 20 passes without a newly seen post. Use **Stop Scroll** and **Stop** to interrupt it. The **Check** button reports visible posts and save errors. The server stays local on `127.0.0.1:3000`.

For Lee, **Collect Lee presidency by month** searches from June 4, 2025 through the current day in monthly intervals in the existing Lee tab. **Resolve shortened Lee posts** visits each incomplete post page in that same tab and saves its full text when available. Both can be stopped from the extension page and rerun; the local server deduplicates post IDs. Rebuild the CSV after collection. These controls navigate the Lee tab, so leave it free until the run finishes.

Targets for this collection:

- `https://x.com/sukyeol__yoon`
- `https://x.com/Jaemyung_Lee`

The account profile and a `from:account since:YYYY-MM-DD until:YYYY-MM-DD` search are supported. X requires sign-in for longer timelines and search. The `truncated` field flags posts whose timeline text shows a “Show more” link. A profile scroll may stop before older posts become accessible, and search can omit posts, so the oldest collected date is a coverage boundary, not proof that earlier posts do not exist. Media-only posts are skipped because they have no text for this NLP corpus.
