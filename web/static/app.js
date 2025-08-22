async function postFiles(url, files, extraFields = {}) {
  const form = new FormData();
  for (const f of files) form.append('files', f);
  for (const [k, v] of Object.entries(extraFields)) form.append(k, v);
  const res = await fetch(url, { method: 'POST', body: form });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

function bindSummarize() {
  const form = document.getElementById('summarize-form');
  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const files = document.getElementById('summarize-files').files;
    const out = document.getElementById('summarize-result');
    out.textContent = 'Working...';
    try {
      const data = await postFiles('/summarize/', files);
      out.textContent = data.summary || JSON.stringify(data, null, 2);
    } catch (err) {
      out.textContent = 'Error: ' + err.message;
    }
  });
}

function bindKG() {
  const form = document.getElementById('kg-form');
  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const files = document.getElementById('kg-files').files;
    const status = document.getElementById('kg-status');
    status.textContent = 'Building graph...';
    try {
      const data = await postFiles('/knowledge-graph/', files);
      const nodes = (data.nodes || []).map(n => ({ data: { id: n.id, label: n.id } }));
      const edges = (data.edges || []).map((e, idx) => ({
        data: { id: e.id || `${e.source}->${e.target}-${idx}`, source: e.source, target: e.target, weight: e.weight || 1 }
      }));

      let cy = window.__cy;
      if (!cy) {
        cy = window.__cy = cytoscape({
          container: document.getElementById('cy'),
          elements: [],
          style: [
            { selector: 'node', style: { 'background-color': '#4f46e5', 'label': 'data(label)', 'color': '#fff', 'font-size': '10px', 'text-wrap': 'wrap', 'text-max-width': '120px', 'text-valign': 'center', 'text-halign': 'center' } },
            { selector: 'edge', style: { 'width': 'mapData(weight, 1, 10, 1, 6)', 'line-color': '#94a3b8', 'curve-style': 'bezier' } },
            { selector: ':selected', style: { 'border-width': 2, 'border-color': '#22d3ee' } }
          ],
          layout: { name: 'cose', animate: true }
        });
      }
      cy.elements().remove();
      cy.add([...nodes, ...edges]);
      cy.layout({ name: 'cose', animate: true }).run();
      cy.fit(undefined, 30);
      status.textContent = `Nodes: ${nodes.length}, Edges: ${edges.length}`;
    } catch (err) {
      status.textContent = 'Error: ' + err.message;
    }
  });
}

function bindQA() {
  const form = document.getElementById('qa-form');
  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const files = document.getElementById('qa-files').files;
    const question = document.getElementById('qa-question').value;
    const out = document.getElementById('qa-result');
    out.textContent = 'Working...';
    try {
      const data = await postFiles('/qa/', files, { question });
      out.textContent = JSON.stringify(data, null, 2);
    } catch (err) {
      out.textContent = 'Error: ' + err.message;
    }
  });
}

window.addEventListener('DOMContentLoaded', () => {
  bindSummarize();
  bindKG();
  bindQA();
});
