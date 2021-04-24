"use strict";
const cells = [...document.querySelectorAll(".cell")];
const symbols = [...document.querySelectorAll("[data-symbol]")];
const newRound = document.querySelector("#new-round");
const resetScores = document.querySelector("#reset-scores");
const retry = document.querySelector("#retry");
const errorBox = document.querySelector("#error");
let state = null;
let csrfToken = "";
let busy = false;

function render() {
  if (!state) return;
  cells.forEach((cell, index) => {
    const mark = state.board[index];
    cell.textContent = mark;
    cell.disabled = busy || Boolean(mark) || Boolean(state.result);
    cell.classList.toggle("mark-o", mark === "O");
    cell.classList.toggle("winner", state.winning_line.includes(index));
    cell.classList.toggle("last-ai", index === state.last_ai_move);
    cell.setAttribute("aria-label", `Row ${Math.floor(index / 3) + 1}, column ${index % 3 + 1}, ${mark || "empty"}`);
  });
  symbols.forEach(button => {
    button.setAttribute("aria-pressed", String(button.dataset.symbol === state.human));
    button.disabled = busy;
  });
  newRound.disabled = resetScores.disabled = busy;
  const message = busy ? "Thinking it through…" : state.result === "draw" ? "A perfect stalemate." :
    state.result === state.human ? "Three in a row. You win!" : state.result ? "The computer takes this one." : "Your move.";
  document.querySelector("#status").textContent = message;
  document.querySelector("#turn-label").textContent = `YOU ARE ${state.human}`;
  document.querySelector("#status-detail").textContent = state.result ? "Start a new round and give it another go." : `You’re playing ${state.human}. Choose an empty square.`;
}

async function request(url, data) {
  const options = data === undefined ? {} : {
    method: "POST", headers: {"Content-Type": "application/json", "X-CSRF-Token": csrfToken},
    body: JSON.stringify(data)
  };
  const response = await fetch(url, {...options, cache: "no-store"});
  const result = await response.json();
  if (!response.ok) throw new Error(result.error || "The request failed. Try reconnecting.");
  if (result.csrf_token) csrfToken = result.csrf_token;
  return result;
}

async function update(url, data) {
  if (busy) return;
  busy = true;
  errorBox.hidden = true;
  retry.hidden = true;
  render();
  try {
    state = await request(url, data);
  } catch (error) {
    errorBox.textContent = error.message || "Could not reach the server.";
    errorBox.hidden = false;
    retry.hidden = false;
  } finally {
    busy = false;
    render();
  }
}

retry.addEventListener("click", () => update("/api/game"));
update("/api/game");

cells.forEach(cell => cell.addEventListener("click", () => {
  if (!state || state.result || busy) return;
  update("/api/move", {index: Number(cell.dataset.index)});
}));
