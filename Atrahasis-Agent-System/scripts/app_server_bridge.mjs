#!/usr/bin/env node

const wsUrl = process.argv[2];

if (!wsUrl) {
  process.stderr.write("Usage: node app_server_bridge.mjs <ws-url>\n");
  process.exit(2);
}

let socket = null;
let isOpen = false;
const queue = [];

function emit(payload) {
  process.stdout.write(`${JSON.stringify(payload)}\n`);
}

function flushQueue() {
  while (queue.length > 0 && socket && isOpen) {
    socket.send(queue.shift());
  }
}

function sendJson(payload) {
  const serialized = JSON.stringify(payload);
  if (socket && isOpen) {
    socket.send(serialized);
    return;
  }
  queue.push(serialized);
}

function connect() {
  socket = new WebSocket(wsUrl);
  socket.addEventListener("open", () => {
    isOpen = true;
    emit({ type: "connected", url: wsUrl });
    flushQueue();
  });
  socket.addEventListener("message", (event) => {
    let message;
    try {
      message = JSON.parse(String(event.data));
    } catch (error) {
      emit({ type: "bridge_error", message: `Invalid App Server JSON: ${String(event.data)}` });
      return;
    }
    if (Object.prototype.hasOwnProperty.call(message, "id") &&
        (Object.prototype.hasOwnProperty.call(message, "result") || Object.prototype.hasOwnProperty.call(message, "error"))) {
      if (message.error) {
        emit({
          type: "rpc_error",
          id: String(message.id),
          message: message.error.message || JSON.stringify(message.error),
          error: message.error,
        });
        return;
      }
      emit({ type: "rpc_response", id: String(message.id), result: message.result || {} });
      return;
    }
    if (message.method && Object.prototype.hasOwnProperty.call(message, "id")) {
      emit({
        type: "server_request",
        id: String(message.id),
        method: message.method,
        params: message.params || {},
      });
      return;
    }
    if (message.method) {
      emit({
        type: "notification",
        method: message.method,
        params: message.params || {},
      });
      return;
    }
    emit({ type: "bridge_message", payload: message });
  });
  socket.addEventListener("close", (event) => {
    isOpen = false;
    emit({ type: "closed", code: event.code, reason: event.reason || "" });
  });
  socket.addEventListener("error", (event) => {
    emit({ type: "bridge_error", message: event.message || "WebSocket error" });
  });
}

process.stdin.setEncoding("utf8");
let buffer = "";
process.stdin.on("data", (chunk) => {
  buffer += chunk;
  while (true) {
    const index = buffer.indexOf("\n");
    if (index === -1) {
      break;
    }
    const line = buffer.slice(0, index).trim();
    buffer = buffer.slice(index + 1);
    if (!line) {
      continue;
    }
    let command;
    try {
      command = JSON.parse(line);
    } catch (error) {
      emit({ type: "bridge_error", message: `Invalid command JSON: ${line}` });
      continue;
    }
    if (command.type === "close") {
      if (socket) {
        socket.close();
      }
      continue;
    }
    if (command.type === "request") {
      sendJson({
        jsonrpc: "2.0",
        id: command.id,
        method: command.method,
        params: command.params || {},
      });
      continue;
    }
    if (command.type === "respond") {
      sendJson({
        jsonrpc: "2.0",
        id: command.id,
        result: command.result || {},
      });
      continue;
    }
    emit({ type: "bridge_error", message: `Unknown command type: ${command.type}` });
  }
});

connect();
