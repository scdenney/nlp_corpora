window.startScrolling = async function () {
  if (window.scrollActive) return;
  window.scrollActive = true;
  let idle = 0;
  const delay = window.xcavatorScrollDelay || 1400;
  const idleLimit = window.xcavatorScrollIdleLimit || 20;
  while (window.scrollActive) {
    const before = window.xcavator?.seen.size || 0;
    const height = document.body.scrollHeight;
    window.scrollTo({ top: height, behavior: 'instant' });
    await new Promise(resolve => setTimeout(resolve, delay));
    window.xcavator?.scan();
    idle = (window.xcavator?.seen.size || 0) > before ? 0 : idle + 1;
    if (idle >= idleLimit) {
      window.scrollActive = false;
      console.log(`Xcavator: stopped after ${idleLimit} scrolls with no new posts`);
    }
  }
};
void window.startScrolling();
