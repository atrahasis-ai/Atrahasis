const wsUrl = process.argv[2];
const repoRoot = process.argv[3];
let nextId = 1;
const pending = new Map();
const events = [];
const ws = new WebSocket(wsUrl);
function request(method, params) {
  const id = nextId++;
  ws.send(JSON.stringify({ jsonrpc: '2.0', id, method, params }));
  return new Promise((resolve, reject) => pending.set(id, { resolve, reject, method }));
}
ws.addEventListener('message', (event) => {
  const msg = JSON.parse(event.data);
  if (Object.prototype.hasOwnProperty.call(msg, 'id') && (Object.prototype.hasOwnProperty.call(msg, 'result') || Object.prototype.hasOwnProperty.call(msg, 'error'))) {
    const entry = pending.get(msg.id);
    if (!entry) return;
    pending.delete(msg.id);
    if (msg.error) entry.reject(new Error(JSON.stringify(msg.error)));
    else entry.resolve(msg.result);
    return;
  }
  if (msg.method && msg.id) {
    ws.send(JSON.stringify({ jsonrpc: '2.0', id: msg.id, result: { decision: 'accept' } }));
    return;
  }
  events.push({ method: msg.method, params: msg.params });
});
ws.addEventListener('open', async () => {
  try {
    await request('initialize', { clientInfo: { name: 'aas-smoke', version: '0.1.0' }, capabilities: { experimentalApi: true } });
    const threadStart = await request('thread/start', {
      cwd: repoRoot,
      approvalPolicy: 'on-request',
      sandbox: 'workspace-write',
      serviceName: 'Atrahasis WS Smoke',
      baseInstructions: 'Use the full local file docs/ATRAHASIS_SYSTEM_MASTER_PROMPT_v5.md as the operative instructions for this thread.',
      experimentalRawEvents: false,
      persistExtendedHistory: true,
      ephemeral: true,
    });
    const threadId = threadStart.thread.id;
    const turnStart = await request('turn/start', {
      threadId,
      input: [{ type: 'text', text: 'Reply with exactly WS_SMOKE_OK', text_elements: [] }],
      cwd: repoRoot,
      approvalPolicy: 'on-request',
      effort: 'high'
    });
    const deadline = Date.now() + 20000;
    while (Date.now() < deadline) {
      if (events.some((event) => event.method === 'turn/completed' && event.params && event.params.turn && event.params.turn.id === turnStart.turn.id)) {
        break;
      }
      await new Promise((resolve) => setTimeout(resolve, 200));
    }
    console.log(JSON.stringify({
      threadId,
      turnId: turnStart.turn.id,
      completed: events.some((event) => event.method === 'turn/completed' && event.params && event.params.turn && event.params.turn.id === turnStart.turn.id),
      eventMethods: events.map((event) => event.method).filter(Boolean).slice(-20),
    }, null, 2));
    ws.close();
  } catch (error) {
    console.error(String(error));
    process.exitCode = 1;
    ws.close();
  }
});
