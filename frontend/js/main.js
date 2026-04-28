/* ═══════════════════════════════════════════════════
   KALYANI PORTFOLIO — MAIN JAVASCRIPT
   ═══════════════════════════════════════════════════ */

const API_BASE = 'https://kalyani-puranik-portfolio.onrender.com';

/* ── PAGE LOADER ──────────────────────────────────── */
window.addEventListener('load', () => {
  setTimeout(() => {
    document.getElementById('pageLoader').classList.add('hidden');
    initRevealObserver();
    animateCounters();
  }, 1500);
});

/* ── CUSTOM CURSOR ────────────────────────────────── */
const dot = document.querySelector('.cursor-dot');
const ring = document.querySelector('.cursor-ring');

let mouseX = 0, mouseY = 0;
let ringX = 0, ringY = 0;

document.addEventListener('mousemove', (e) => {
  mouseX = e.clientX;
  mouseY = e.clientY;
  dot.style.left = mouseX + 'px';
  dot.style.top = mouseY + 'px';
});

function animateRing() {
  ringX += (mouseX - ringX) * 0.12;
  ringY += (mouseY - ringY) * 0.12;
  ring.style.left = ringX + 'px';
  ring.style.top = ringY + 'px';
  requestAnimationFrame(animateRing);
}
animateRing();

// Hide cursor on mobile
if ('ontouchstart' in window) {
  dot.style.display = 'none';
  ring.style.display = 'none';
  document.body.style.cursor = 'auto';
}

/* ── NAV ──────────────────────────────────────────── */
const nav = document.getElementById('nav');

window.addEventListener('scroll', () => {
  nav.classList.toggle('scrolled', window.scrollY > 60);
});

/* ── MOBILE MENU ──────────────────────────────────── */
const hamburger = document.getElementById('hamburger');
const mobileMenu = document.getElementById('mobileMenu');

hamburger.addEventListener('click', () => {
  mobileMenu.classList.toggle('open');
  const bars = hamburger.querySelectorAll('span');
  const isOpen = mobileMenu.classList.contains('open');
  bars[0].style.transform = isOpen ? 'rotate(45deg) translateY(6px)' : '';
  bars[1].style.opacity = isOpen ? '0' : '1';
  bars[2].style.transform = isOpen ? 'rotate(-45deg) translateY(-6px)' : '';
});

function closeMobile() {
  mobileMenu.classList.remove('open');
  hamburger.querySelectorAll('span').forEach(s => {
    s.style.transform = '';
    s.style.opacity = '';
  });
}

/* ── THEME TOGGLE ─────────────────────────────────── */
const themeToggle = document.getElementById('themeToggle');
const html = document.documentElement;

const savedTheme = localStorage.getItem('kalyani-theme') || 'light';
html.setAttribute('data-theme', savedTheme);

themeToggle.addEventListener('click', () => {
  const current = html.getAttribute('data-theme');
  const next = current === 'light' ? 'dark' : 'light';
  html.setAttribute('data-theme', next);
  localStorage.setItem('kalyani-theme', next);
});

/* ── SCROLL REVEAL ────────────────────────────────── */
function initRevealObserver() {
  const elements = document.querySelectorAll('.reveal-up, .reveal-left, .reveal-right');

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('in-view');
      }
    });
  }, { threshold: 0.1, rootMargin: '0px 0px -50px 0px' });

  elements.forEach(el => observer.observe(el));
}

/* ── COUNTER ANIMATION ────────────────────────────── */
function animateCounters() {
  const counters = document.querySelectorAll('.stat-num[data-target]');

  const obs = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const el = entry.target;
        const target = parseInt(el.dataset.target);
        let count = 0;
        const step = target / 40;
        const timer = setInterval(() => {
          count = Math.min(count + step, target);
          el.textContent = Math.floor(count);
          if (count >= target) clearInterval(timer);
        }, 30);
        obs.unobserve(el);
      }
    });
  }, { threshold: 0.5 });

  counters.forEach(el => obs.observe(el));
}

/* ── SKILL BARS ───────────────────────────────────── */
const skillObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      const fills = entry.target.querySelectorAll('.skill-fill');
      fills.forEach(fill => {
        const level = fill.dataset.level;
        setTimeout(() => {
          fill.style.width = level + '%';
        }, 200);
      });
      skillObserver.unobserve(entry.target);
    }
  });
}, { threshold: 0.3 });

document.querySelectorAll('.skill-card').forEach(card => {
  skillObserver.observe(card);
});

/* ── BLOGS (from API) ─────────────────────────────── */
async function fetchBlogs() {
  const grid = document.getElementById('blogGrid');

  try {
    const res = await fetch(`${API_BASE}/blogs?limit=3`);
    if (!res.ok) throw new Error('API unavailable');
    const data = await res.json();
    renderBlogs(data.blogs || data);
  } catch (e) {
    renderBlogs(sampleBlogs);
  }
}

const sampleBlogs = [
  {
    _id: '1',
    title: 'Junk Data Junk Data Junk Data Junk Data ',
    excerpt: 'Junk Data Junk Data Junk Data Junk Data Junk Data Junk Data Junk Data Junk Data Junk Data Junk Data ',
    tag: 'ML',
    date: '2024-11-15',
    read_time: '8 min read'
  },
  {
    _id: '2',
    title: 'Junk Data Junk Data Junk Data Junk Data ',
    excerpt: 'Junk Data Junk Data Junk Data Junk Data Junk Data Junk Data Junk Data Junk Data Junk Data Junk Data ',
    tag: 'NLP',
    date: '2024-10-22',
    read_time: '12 min read'
  },
  {
    _id: '3',
    title: 'Junk Data Junk Data Junk Data Junk Data ',
    excerpt: 'Junk Data Junk Data Junk Data Junk Data Junk Data Junk Data Junk Data Junk Data Junk Data Junk Data ',
    tag: 'personal',
    date: '2024-09-10',
    read_time: '6 min read'
  }
];

function renderBlogs(blogs) {
  const grid = document.getElementById('blogGrid');

  if (!blogs || blogs.length === 0) {
    grid.innerHTML = '<p style="text-align:center; color: var(--text-muted); padding: 3rem">No posts yet — check back soon! ✨</p>';
    return;
  }

  grid.innerHTML = blogs.map((blog, i) => `
    <article class="blog-card reveal-up" style="transition-delay: ${i * 0.1}s" onclick="openBlog('${blog._id}')">
      <span class="blog-tag">${blog.tag || 'thoughts'}</span>
      <h3 class="blog-title">${blog.title}</h3>
      <p class="blog-excerpt">${blog.excerpt}</p>
      <div class="blog-footer">
        <span class="blog-date">${formatDate(blog.date || blog.created_at)}</span>
        <span class="blog-read-time">${blog.read_time || '5 min read'}</span>
      </div>
    </article>
  `).join('');

  // Re-observe new elements
  document.querySelectorAll('#blogGrid .reveal-up').forEach(el => {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) entry.target.classList.add('in-view');
      });
    }, { threshold: 0.1 });
    observer.observe(el);
  });
}

function openBlog(id) {
  console.log('Opening blog:', id);
}

function formatDate(dateStr) {
  if (!dateStr) return '';
  const d = new Date(dateStr);
  return d.toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric' });
}

/* ── GITHUB STATS ─────────────────────────────────── */
async function loadGithubStats() {
  try {
    const res = await fetch(`${API_BASE}/github/stats`);
    const data = await res.json();

    const setStat = (id, value) => {
      const el = document.getElementById(id);
      if (!el) return;

      el.setAttribute("data-target", value);
      el.textContent = "0";
    };

    // set values
    setStat("githubRepos", data.public_repos ?? 0);
    setStat("githubStars", data.total_stars ?? 0);
    setStat("githubFollowers", data.followers ?? 0);
    setStat("githubContribs", data.contributions_year ?? 0);

    // animation function
    const animateStat = (el, target) => {
      let count = 0;
      const step = target / 40;

      const timer = setInterval(() => {
        count += step;

        if (count >= target) {
          el.textContent = target;
          clearInterval(timer);
        } else {
          el.textContent = Math.floor(count);
        }
      }, 20);
    };

    // animate each stat
    ["githubRepos", "githubStars", "githubFollowers", "githubContribs"].forEach(id => {
      const el = document.getElementById(id);
      if (!el) return;

      const target = parseInt(el.getAttribute("data-target")) || 0;
      animateStat(el, target);
    });

    // bottom card (no animation)
    document.getElementById("githubTotalStars").innerText = data.total_stars ?? 0;
    document.getElementById("githubCommits").innerText = data.total_commits ?? 0;
    document.getElementById("githubPRs").innerText = data.total_prs ?? 0;
    document.getElementById("githubIssues").innerText = data.total_issues ?? 0;
    document.getElementById("githubContributions").innerText = data.contributions_year ?? 0;

  } catch (err) {
    console.error("GitHub fetch failed", err);
  }
}

/* ── SPOTIFY ──────────────────────────────────────── */
async function fetchSpotify() {
  try {
    const res = await fetch(`${API_BASE}/spotify/now-playing`);
    const data = await res.json();

    const songEl = document.getElementById('spotifySong');
    const artistEl = document.getElementById('spotifyArtist');

    const albumEl = document.querySelector('.album-placeholder');

    if (albumEl && data.album_art) {
      albumEl.innerHTML = `
      <img src="${data.album_art}" 
      style="width:100%;height:100%;object-fit:cover;border-radius:10px">
    `;
    }
    if (songEl) songEl.innerText = data.track_name || "not listening rn";
    if (artistEl) artistEl.innerText = data.artist || "";

    if (data.album_art) {
      document.querySelector('.album-placeholder').innerHTML =
        `<img src="${data.album_art}" style="width:100%;height:100%;object-fit:cover;border-radius:6px">`;
    }

  } catch {
    document.getElementById('spotifySong').textContent = 'not listening rn';
    document.getElementById('spotifyArtist').textContent = '';
  }
}

/* ── CONTACT FORM ─────────────────────────────────── */
document.getElementById('contactForm').addEventListener('submit', async (e) => {
  e.preventDefault();

  const btn = document.getElementById('submitBtn');
  const feedback = document.getElementById('formFeedback');

  btn.textContent = 'sending... ✈️';
  btn.disabled = true;

  const payload = {
    name: document.getElementById('name').value,
    email: document.getElementById('email').value,
    subject: document.getElementById('subject').value,
    message: document.getElementById('message').value
  };

  try {
    const res = await fetch(`${API_BASE}/contact`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    if (res.ok) {
      feedback.textContent = 'got it! i\'ll write back soon 💌';
      feedback.style.color = '#5a7a4a';
      e.target.reset();
    } else {
      throw new Error();
    }
  } catch {
    // Simulate success for demo
    feedback.textContent = 'message received! talk soon ✨';
    feedback.style.color = 'var(--puce)';
    e.target.reset();
  }

  btn.textContent = 'send it ✈️';
  btn.disabled = false;

  setTimeout(() => { feedback.textContent = ''; }, 5000);
});

/* ── RESUME DOWNLOAD ─────────────────────────────── */
function downloadResume() {
  window.open("/fronend/public/resume.pdf", "_blank");
}

/* ── ANALYTICS ────────────────────────────────────── */
async function trackVisit() {
  try {
    await fetch(`${API_BASE}/analytics/visit`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        page: '/',
        referrer: document.referrer,
        timestamp: new Date().toISOString()
      })
    });
  } catch { /* Silently fail */ }
}

/* ── EASTER EGG ───────────────────────────────────── */
function triggerEasterEgg() {
  document.getElementById('easterEgg').classList.add('active');
}

// Konami code easter egg
const konami = ['ArrowUp','ArrowUp','ArrowDown','ArrowDown','ArrowLeft','ArrowRight','ArrowLeft','ArrowRight','b','a'];
let konamiIndex = 0;

document.addEventListener('keydown', (e) => {
  if (e.key === konami[konamiIndex]) {
    konamiIndex++;
    if (konamiIndex === konami.length) {
      triggerEasterEgg();
      konamiIndex = 0;
    }
  } else {
    konamiIndex = 0;
  }
});

/* ── PARALLAX ─────────────────────────────────────── */
window.addEventListener('scroll', () => {
  const scrollY = window.scrollY;
  const orbs = document.querySelectorAll('.hero-orb');
  orbs.forEach((orb, i) => {
    const speed = 0.2 + i * 0.1;
    orb.style.transform = `translateY(${scrollY * speed}px)`;
  });
}, { passive: true });

/* ── SMOOTH ACTIVE NAV ──────────────────────────────── */
const sections = document.querySelectorAll('section[id]');

const sectionObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      const id = entry.target.id;
      document.querySelectorAll('.nav-links a').forEach(a => {
        a.classList.toggle('active', a.getAttribute('href') === `#${id}`);
      });
    }
  });
}, { threshold: 0.4 });

sections.forEach(s => sectionObserver.observe(s));

/* ── INIT ─────────────────────────────────────────── */
document.addEventListener('DOMContentLoaded', () => {
  fetchBlogs();
  loadGithubStats();
  fetchSpotify();
  trackVisit();

  setInterval(fetchSpotify, 30000);
});
