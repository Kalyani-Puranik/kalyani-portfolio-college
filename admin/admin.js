/* ═══════════════════════════════════════════════════
   KALYANI PORTFOLIO — ADMIN DASHBOARD JS
   ═══════════════════════════════════════════════════ */

const API = 'http://localhost:8000';
let token = localStorage.getItem('admin_token');

/* ── INIT ──────────────────────────────────────────── */
window.addEventListener('DOMContentLoaded', () => {
  if (token) {
    showDashboard();
  }
});

/* ── AUTH ──────────────────────────────────────────── */
document.getElementById('loginForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  const errEl = document.getElementById('loginError');
  errEl.textContent = '';

  const username = document.getElementById('loginUsername').value;
  const password = document.getElementById('loginPassword').value;

  try {
    const res = await fetch(`${API}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password })
    });

    if (!res.ok) throw new Error('Invalid credentials');

    const data = await res.json();
    token = data.access_token;
    localStorage.setItem('admin_token', token);
    showDashboard();
  } catch (err) {
    errEl.textContent = 'Invalid username or password';
  }
});

function showDashboard() {
  document.getElementById('loginScreen').style.display = 'none';
  document.getElementById('dashboard').classList.add('active');
  loadOverview();
  loadBlogs();
  loadProjects();
  loadMessages();
}

function logout() {
  localStorage.removeItem('admin_token');
  token = null;
  document.getElementById('loginScreen').style.display = 'flex';
  document.getElementById('dashboard').classList.remove('active');
}

function authHeader() {
  return { 'Authorization': `Bearer ${token}`, 'Content-Type': 'application/json' };
}

/* ── PANEL NAVIGATION ──────────────────────────────── */
function showPanel(name) {
  document.querySelectorAll('.panel').forEach(p => p.classList.remove('active'));
  document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
  document.getElementById(`panel-${name}`).classList.add('active');
  event.currentTarget.classList.add('active');

  if (name === 'analytics') loadAnalytics();
}

/* ── OVERVIEW ──────────────────────────────────────── */
async function loadOverview() {
  try {
    const [blogsRes, projectsRes, messagesRes, analyticsRes] = await Promise.allSettled([
      fetch(`${API}/blogs?limit=1`, { headers: authHeader() }),
      fetch(`${API}/projects`, { headers: authHeader() }),
      fetch(`${API}/contact`, { headers: authHeader() }),
      fetch(`${API}/analytics/summary`, { headers: authHeader() }),
    ]);

    if (blogsRes.status === 'fulfilled' && blogsRes.value.ok) {
      const d = await blogsRes.value.json();
      document.getElementById('statBlogs').textContent = d.total || 0;
    }
    if (projectsRes.status === 'fulfilled' && projectsRes.value.ok) {
      const d = await projectsRes.value.json();
      document.getElementById('statProjects').textContent = d.length || 0;
    }
    if (messagesRes.status === 'fulfilled' && messagesRes.value.ok) {
      const d = await messagesRes.value.json();
      document.getElementById('statMessages').textContent = d.length || 0;
      renderRecentMessages(d.slice(0, 5));
    }
    if (analyticsRes.status === 'fulfilled' && analyticsRes.value.ok) {
      const d = await analyticsRes.value.json();
      document.getElementById('statVisits').textContent = d.total_visits || 0;
    }
  } catch (e) {
    console.error('Overview load error:', e);
  }
}

function renderRecentMessages(messages) {
  const tbody = document.getElementById('recentMessages');
  if (!messages.length) {
    tbody.innerHTML = '<tr><td colspan="4" style="color:var(--text-muted);text-align:center;padding:2rem">No messages yet</td></tr>';
    return;
  }
  tbody.innerHTML = messages.map(m => `
    <tr>
      <td><strong>${esc(m.name)}</strong></td>
      <td class="truncate text-muted">${esc(m.subject || '—')}</td>
      <td class="text-muted">${formatDate(m.created_at)}</td>
      <td><span class="badge ${m.read ? 'badge-green' : 'badge-puce'}">${m.read ? 'read' : 'new'}</span></td>
    </tr>
  `).join('');
}

/* ── BLOGS ──────────────────────────────────────────── */
let allBlogs = [];

async function loadBlogs() {
  try {
    const res = await fetch(`${API}/blogs?limit=50&published_only=false`, { headers: authHeader() });
    const data = await res.json();
    allBlogs = data.blogs || [];
    renderBlogsTable(allBlogs);
  } catch (e) {
    document.getElementById('blogsTable').innerHTML = `<tr><td colspan="6" style="color:var(--red);padding:2rem;text-align:center">Failed to load blogs</td></tr>`;
  }
}

function renderBlogsTable(blogs) {
  const tbody = document.getElementById('blogsTable');
  if (!blogs.length) {
    tbody.innerHTML = '<tr><td colspan="6" style="color:var(--text-muted);text-align:center;padding:2rem">No posts yet. Create your first! ✨</td></tr>';
    return;
  }
  tbody.innerHTML = blogs.map(b => `
    <tr>
      <td class="truncate"><strong>${esc(b.title)}</strong></td>
      <td><span class="badge badge-puce">${esc(b.tag)}</span></td>
      <td><span class="badge ${b.published ? 'badge-green' : 'badge-red'}">${b.published ? 'published' : 'draft'}</span></td>
      <td class="text-muted">${b.views}</td>
      <td class="text-muted">${formatDate(b.created_at)}</td>
      <td>
        <div style="display:flex;gap:0.5rem">
          <button class="btn btn-ghost btn-sm" onclick="editBlog('${b.id}')"><i class="fas fa-pen"></i></button>
          <button class="btn btn-danger btn-sm" onclick="deleteBlog('${b.id}')"><i class="fas fa-trash"></i></button>
        </div>
      </td>
    </tr>
  `).join('');
}

function editBlog(id) {
  const blog = allBlogs.find(b => b.id === id);
  if (!blog) return;

  document.getElementById('blogModalTitle').textContent = 'Edit Blog Post';
  document.getElementById('blogSubmitBtn').textContent = 'Update Post';
  document.getElementById('blogId').value = id;
  document.getElementById('blogTitle').value = blog.title;
  document.getElementById('blogSlug').value = blog.slug;
  document.getElementById('blogExcerpt').value = blog.excerpt;
  document.getElementById('blogContent').value = blog.content || '';
  document.getElementById('blogTag').value = blog.tag;
  document.getElementById('blogReadTime').value = blog.read_time;
  document.getElementById('blogCoverImage').value = blog.cover_image || '';
  document.getElementById('blogPublished').checked = blog.published;
  document.getElementById('blogFeatured').checked = blog.featured;

  openModal('blog');
}

async function deleteBlog(id) {
  if (!confirm('Delete this blog post? This cannot be undone.')) return;
  try {
    const res = await fetch(`${API}/blogs/${id}`, { method: 'DELETE', headers: authHeader() });
    if (res.ok) {
      loadBlogs();
      showToast('Blog deleted');
    }
  } catch (e) {
    showToast('Delete failed', true);
  }
}

document.getElementById('blogForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  const id = document.getElementById('blogId').value;
  const isEdit = !!id;
  const fb = document.getElementById('blogFeedback');
  const btn = document.getElementById('blogSubmitBtn');

  btn.textContent = isEdit ? 'Updating...' : 'Creating...';
  btn.disabled = true;
  fb.className = 'feedback';

  const payload = {
    title: document.getElementById('blogTitle').value,
    slug: document.getElementById('blogSlug').value,
    excerpt: document.getElementById('blogExcerpt').value,
    content: document.getElementById('blogContent').value,
    tag: document.getElementById('blogTag').value,
    read_time: document.getElementById('blogReadTime').value || '5 min read',
    cover_image: document.getElementById('blogCoverImage').value || null,
    published: document.getElementById('blogPublished').checked,
    featured: document.getElementById('blogFeatured').checked,
  };

  try {
    const url = isEdit ? `${API}/blogs/${id}` : `${API}/blogs/`;
    const method = isEdit ? 'PUT' : 'POST';
    const res = await fetch(url, { method, headers: authHeader(), body: JSON.stringify(payload) });

    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || 'Failed');
    }

    fb.className = 'feedback success';
    fb.textContent = isEdit ? '✓ Blog updated!' : '✓ Blog created!';
    loadBlogs();
    setTimeout(() => closeModal('blog'), 1200);
  } catch (err) {
    fb.className = 'feedback error';
    fb.textContent = err.message;
  }

  btn.textContent = isEdit ? 'Update Post' : 'Create Post';
  btn.disabled = false;
});

// Auto-generate slug from title
document.getElementById('blogTitle').addEventListener('input', (e) => {
  if (!document.getElementById('blogId').value) {
    document.getElementById('blogSlug').value = slugify(e.target.value);
  }
});

/* ── PROJECTS ───────────────────────────────────────── */
let allProjects = [];

async function loadProjects() {
  try {
    const res = await fetch(`${API}/projects/`, { headers: authHeader() });
    allProjects = await res.json();
    renderProjectsTable(allProjects);
  } catch (e) {
    document.getElementById('projectsTable').innerHTML = `<tr><td colspan="6" style="color:var(--red);padding:2rem;text-align:center">Failed to load projects</td></tr>`;
  }
}

function renderProjectsTable(projects) {
  const tbody = document.getElementById('projectsTable');
  if (!projects.length) {
    tbody.innerHTML = '<tr><td colspan="6" style="color:var(--text-muted);text-align:center;padding:2rem">No projects yet.</td></tr>';
    return;
  }
  tbody.innerHTML = projects.map(p => `
    <tr>
      <td><strong>${esc(p.title)}</strong></td>
      <td class="text-muted">${esc(p.project_type || '—')}</td>
      <td><div style="display:flex;gap:0.3rem;flex-wrap:wrap">${(p.tech_stack || []).slice(0, 3).map(t => `<span class="badge badge-puce">${esc(t)}</span>`).join('')}</div></td>
      <td>${p.featured ? '<span class="badge badge-green">yes</span>' : '<span class="badge badge-red">no</span>'}</td>
      <td class="text-muted">${p.order}</td>
      <td>
        <div style="display:flex;gap:0.5rem">
          <button class="btn btn-ghost btn-sm" onclick="editProject('${p.id}')"><i class="fas fa-pen"></i></button>
          <button class="btn btn-danger btn-sm" onclick="deleteProject('${p.id}')"><i class="fas fa-trash"></i></button>
        </div>
      </td>
    </tr>
  `).join('');
}

function editProject(id) {
  const project = allProjects.find(p => p.id === id);
  if (!project) return;

  document.getElementById('projectModalTitle').textContent = 'Edit Project';
  document.getElementById('projectSubmitBtn').textContent = 'Update Project';
  document.getElementById('projectId').value = id;
  document.getElementById('projectTitle').value = project.title;
  document.getElementById('projectSlug').value = project.slug;
  document.getElementById('projectDescription').value = project.description;
  document.getElementById('projectProblem').value = project.problem;
  document.getElementById('projectSolution').value = project.solution;
  document.getElementById('projectImpact').value = project.impact;
  document.getElementById('projectTechStack').value = (project.tech_stack || []).join(', ');
  document.getElementById('projectGithub').value = project.github_url || '';
  document.getElementById('projectDemo').value = project.demo_url || '';
  document.getElementById('projectYear').value = project.year || '';
  document.getElementById('projectType').value = project.project_type || '';

  openModal('project');
}

async function deleteProject(id) {
  if (!confirm('Delete this project?')) return;
  try {
    const res = await fetch(`${API}/projects/${id}`, { method: 'DELETE', headers: authHeader() });
    if (res.ok) { loadProjects(); showToast('Project deleted'); }
  } catch { showToast('Delete failed', true); }
}

document.getElementById('projectForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  const id = document.getElementById('projectId').value;
  const isEdit = !!id;
  const fb = document.getElementById('projectFeedback');
  const btn = document.getElementById('projectSubmitBtn');

  btn.textContent = 'Saving...';
  btn.disabled = true;
  fb.className = 'feedback';

  const techRaw = document.getElementById('projectTechStack').value;
  const payload = {
    title: document.getElementById('projectTitle').value,
    slug: document.getElementById('projectSlug').value,
    description: document.getElementById('projectDescription').value,
    problem: document.getElementById('projectProblem').value,
    solution: document.getElementById('projectSolution').value,
    impact: document.getElementById('projectImpact').value,
    tech_stack: techRaw ? techRaw.split(',').map(s => s.trim()).filter(Boolean) : [],
    github_url: document.getElementById('projectGithub').value || null,
    demo_url: document.getElementById('projectDemo').value || null,
    year: document.getElementById('projectYear').value,
    project_type: document.getElementById('projectType').value,
  };

  try {
    const url = isEdit ? `${API}/projects/${id}` : `${API}/projects/`;
    const method = isEdit ? 'PUT' : 'POST';
    const res = await fetch(url, { method, headers: authHeader(), body: JSON.stringify(payload) });
    if (!res.ok) throw new Error((await res.json()).detail || 'Failed');

    fb.className = 'feedback success';
    fb.textContent = isEdit ? '✓ Project updated!' : '✓ Project created!';
    loadProjects();
    setTimeout(() => closeModal('project'), 1200);
  } catch (err) {
    fb.className = 'feedback error';
    fb.textContent = err.message;
  }

  btn.textContent = isEdit ? 'Update Project' : 'Create Project';
  btn.disabled = false;
});

document.getElementById('projectTitle').addEventListener('input', (e) => {
  if (!document.getElementById('projectId').value) {
    document.getElementById('projectSlug').value = slugify(e.target.value);
  }
});

/* ── MESSAGES ───────────────────────────────────────── */
async function loadMessages() {
  try {
    const res = await fetch(`${API}/contact/`, { headers: authHeader() });
    if (!res.ok) throw new Error();
    const messages = await res.json();
    renderMessagesTable(messages);
  } catch {
    document.getElementById('messagesTable').innerHTML = `<tr><td colspan="5" style="color:var(--red);padding:2rem;text-align:center">Failed to load messages</td></tr>`;
  }
}

function renderMessagesTable(messages) {
  const tbody = document.getElementById('messagesTable');
  if (!messages.length) {
    tbody.innerHTML = '<tr><td colspan="5" style="color:var(--text-muted);text-align:center;padding:2rem">No messages yet</td></tr>';
    return;
  }
  tbody.innerHTML = messages.map(m => `
    <tr class="message-row ${m.read ? '' : 'unread'}" onclick="toggleMessage('${m.id || ''}', this)">
      <td><strong>${esc(m.name)}</strong></td>
      <td class="text-muted">${esc(m.email)}</td>
      <td class="text-muted">${esc(m.subject || '—')}</td>
      <td class="text-muted">${formatDate(m.created_at)}</td>
      <td><span class="badge ${m.read ? 'badge-green' : 'badge-puce'}">${m.read ? 'read' : 'new'}</span></td>
    </tr>
    <tr><td colspan="5" style="padding:0">
      <div class="message-detail" id="msg-${m.id || m._id}">
        <p style="color:var(--text-muted);font-size:0.85rem;margin-bottom:0.75rem">
          From: <strong>${esc(m.name)}</strong> · ${esc(m.email)} · ${formatDate(m.created_at)}
        </p>
        <p style="font-size:0.95rem;line-height:1.7">${esc(m.message)}</p>
        <div style="margin-top:1rem">
          <a href="mailto:${esc(m.email)}?subject=Re: ${esc(m.subject || '')}" class="btn btn-primary btn-sm">
            <i class="fas fa-reply"></i> Reply via Email
          </a>
        </div>
      </div>
    </td></tr>
  `).join('');
}

function toggleMessage(id, row) {
  const detail = document.getElementById(`msg-${id}`);
  if (detail) detail.classList.toggle('open');
}

/* ── ANALYTICS ──────────────────────────────────────── */
async function loadAnalytics() {
  try {
    const res = await fetch(`${API}/analytics/summary`, { headers: authHeader() });
    if (!res.ok) throw new Error();
    const data = await res.json();

    document.getElementById('aStatTotal').textContent = data.total_visits || 0;
    document.getElementById('aStatToday').textContent = data.today_visits || 0;
    document.getElementById('aStatWeek').textContent = data.weekly_visits || 0;

    const tbody = document.getElementById('analyticsTable');
    const breakdown = data.page_breakdown || {};
    tbody.innerHTML = Object.entries(breakdown).map(([page, count]) => `
      <tr>
        <td><code>${esc(page)}</code></td>
        <td><strong>${count}</strong></td>
      </tr>
    `).join('') || '<tr><td colspan="2" style="color:var(--text-muted);text-align:center;padding:2rem">No data yet</td></tr>';
  } catch {
    document.getElementById('aStatTotal').textContent = '—';
  }
}

/* ── MODAL ──────────────────────────────────────────── */
function openModal(name) {
  document.getElementById(`modal-${name}`).classList.add('open');
}

function closeModal(name) {
  document.getElementById(`modal-${name}`).classList.remove('open');
  // Reset form
  const form = document.getElementById(`${name}Form`);
  if (form) {
    form.reset();
    form.querySelectorAll('input[type="hidden"]').forEach(i => i.value = '');
  }
  // Reset modal titles
  if (name === 'blog') {
    document.getElementById('blogModalTitle').textContent = 'New Blog Post';
    document.getElementById('blogSubmitBtn').textContent = 'Create Post';
    document.getElementById('blogFeedback').className = 'feedback';
  }
  if (name === 'project') {
    document.getElementById('projectModalTitle').textContent = 'New Project';
    document.getElementById('projectSubmitBtn').textContent = 'Create Project';
    document.getElementById('projectFeedback').className = 'feedback';
  }
}

// Close modal on overlay click
document.querySelectorAll('.modal-overlay').forEach(overlay => {
  overlay.addEventListener('click', (e) => {
    if (e.target === overlay) {
      const name = overlay.id.replace('modal-', '');
      closeModal(name);
    }
  });
});

/* ── UTILITIES ──────────────────────────────────────── */
function esc(str) {
  if (!str) return '';
  return String(str).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

function formatDate(dateStr) {
  if (!dateStr) return '—';
  return new Date(dateStr).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
}

function slugify(text) {
  return text.toLowerCase().trim()
    .replace(/[^\w\s-]/g, '')
    .replace(/[\s_-]+/g, '-')
    .replace(/^-+|-+$/g, '');
}

// Toast notification
function showToast(msg, isError = false) {
  const toast = document.createElement('div');
  toast.textContent = msg;
  Object.assign(toast.style, {
    position: 'fixed', bottom: '2rem', right: '2rem',
    background: isError ? 'var(--red)' : 'var(--green)',
    color: '#fff', padding: '0.75rem 1.5rem',
    borderRadius: '999px', fontSize: '0.875rem',
    zIndex: '9999', boxShadow: '0 8px 24px rgba(0,0,0,0.2)',
    animation: 'fadeIn 0.3s ease'
  });
  document.body.appendChild(toast);
  setTimeout(() => toast.remove(), 3000);
}
