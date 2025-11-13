let currentDocId = null;

function addMsg(role, text) {
  const w = document.getElementById('chatWindow');
  const div = document.createElement('div');
  div.className = 'msg';
  const who = document.createElement('div');
  who.className = 'role';
  who.textContent = role + ':';
  const content = document.createElement('div');
  content.textContent = text;
  div.appendChild(who);
  div.appendChild(content);
  w.appendChild(div);
  w.scrollTop = w.scrollHeight;
}

async function uploadPdf() {
  const file = document.getElementById('fileInput').files[0];
  if (!file) { alert('Please choose a PDF first.'); return; }
  const fd = new FormData();
  fd.append('file', file);
  document.getElementById('uploadStatus').textContent = 'Uploading & processing…';
  const res = await fetch('/api/upload', { method: 'POST', body: fd });
  if (!res.ok) {
    const err = await res.json().catch(()=>({detail:'Upload failed'}));
    document.getElementById('uploadStatus').textContent = '❌ ' + (err.detail || 'Upload failed');
    return;
  }
  const data = await res.json();
  currentDocId = data.doc_id;
  document.getElementById('uploadStatus').textContent = `✅ Uploaded: ${data.filename} (doc_id=${currentDocId})`;
  const sum = await fetch(`/api/docs/${currentDocId}/summary`);
  const sumData = await sum.json();
  document.getElementById('summaryText').textContent = sumData.summary;
}

async function sendMessage() {
  const input = document.getElementById('userMessage');
  const msg = input.value.trim();
  if (!msg) return;
  if (!currentDocId) { alert('Upload a PDF first.'); return; }
  addMsg('You', msg);
  input.value = '';

  const res = await fetch('/api/chat', {
    method: 'POST',
    headers: {'Content-Type':'application/json'},
    body: JSON.stringify({ doc_id: currentDocId, message: msg })
  });
  if (!res.ok) {
    const err = await res.json().catch(()=>({detail:'Request failed'}));
    addMsg('Bot', '❌ ' + (err.detail || 'Could not answer.'));
    return;
  }
  const data = await res.json();
  addMsg('Bot', data.answer);
  if (data.sources && data.sources.length) {
    data.sources.forEach((s, i) => {
      const w = document.getElementById('chatWindow');
      const el = document.createElement('div');
      el.className = 'source';
      el.textContent = `[${i+1}] score=${s.score.toFixed(3)} — ` + s.chunk.slice(0, 180) + '…';
      w.appendChild(el);
    });
  }
}

document.getElementById('uploadBtn').addEventListener('click', uploadPdf);
document.getElementById('sendBtn').addEventListener('click', sendMessage);
document.getElementById('userMessage').addEventListener('keydown', (e) => {
  if (e.key === 'Enter') sendMessage();
});
