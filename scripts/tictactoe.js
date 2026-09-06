const fs = require('fs');
const path = require('path');

const DATA_FILE = path.join(__dirname, '../data/tictactoe.json');
const README_FILE = path.join(__dirname, '../README.md');

function loadState() {
  if (fs.existsSync(DATA_FILE)) {
    try {
      return JSON.parse(fs.readFileSync(DATA_FILE, 'utf8'));
    } catch (e) {
      // fallback
    }
  }
  return {
    board: [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]],
    status: "in_progress",
    totalGames: 0,
    playerWins: 0,
    botWins: 0,
    draws: 0,
    lastPlayer: "Visitor"
  };
}

function saveState(state) {
  fs.writeFileSync(DATA_FILE, JSON.stringify(state, null, 2));
}

function checkWinner(b) {
  const lines = [
    // rows
    [b[0][0], b[0][1], b[0][2]],
    [b[1][0], b[1][1], b[1][2]],
    [b[2][0], b[2][1], b[2][2]],
    // cols
    [b[0][0], b[1][0], b[2][0]],
    [b[0][1], b[1][1], b[2][1]],
    [b[0][2], b[1][2], b[2][2]],
    // diags
    [b[0][0], b[1][1], b[2][2]],
    [b[0][2], b[1][1], b[2][0]]
  ];

  for (const line of lines) {
    if (line[0] !== " " && line[0] === line[1] && line[1] === line[2]) {
      return line[0];
    }
  }

  const isFull = b.every(row => row.every(cell => cell !== " "));
  if (isFull) return "DRAW";

  return null;
}

function botMove(b) {
  // Check if bot can win in 1 move
  for (let r = 0; r < 3; r++) {
    for (let c = 0; c < 3; c++) {
      if (b[r][c] === " ") {
        b[r][c] = "O";
        if (checkWinner(b) === "O") return [r, c];
        b[r][c] = " ";
      }
    }
  }

  // Check if player could win in 1 move, block them
  for (let r = 0; r < 3; r++) {
    for (let c = 0; c < 3; c++) {
      if (b[r][c] === " ") {
        b[r][c] = "X";
        if (checkWinner(b) === "X") {
          b[r][c] = " ";
          return [r, c];
        }
        b[r][c] = " ";
      }
    }
  }

  // Pick center if available
  if (b[1][1] === " ") return [1, 1];

  // Pick corners
  const corners = [[0, 0], [0, 2], [2, 0], [2, 2]].filter(([r, c]) => b[r][c] === " ");
  if (corners.length > 0) {
    return corners[Math.floor(Math.random() * corners.length)];
  }

  // Pick any remaining
  const remaining = [];
  for (let r = 0; r < 3; r++) {
    for (let c = 0; c < 3; c++) {
      if (b[r][c] === " ") remaining.push([r, c]);
    }
  }
  if (remaining.length > 0) {
    return remaining[Math.floor(Math.random() * remaining.length)];
  }

  return null;
}

function renderMarkdown(state) {
  const b = state.board;
  const repo = "Lazizdeveloper/Lazizdeveloper";

  let statusMsg = "";
  if (state.status === "player_won") {
    statusMsg = `🎉 **Tabriklaymiz! Siz (❌) g'alaba qozondingiz!**`;
  } else if (state.status === "bot_won") {
    statusMsg = `🤖 **Bot (⭕) yutib chiqdi! Keyingi safar omad kulib boqadi.**`;
  } else if (state.status === "draw") {
    statusMsg = `🤝 **Durang! Do'stlik g'alaba qozondi.**`;
  } else {
    statusMsg = `🎮 **Sizning navbatingiz (❌)!** Bo'sh katakchalardan birini bosing:`;
  }

  let table = "| 1 | 2 | 3 |\n| :---: | :---: | :---: |\n";
  for (let r = 0; r < 3; r++) {
    const row = [];
    for (let c = 0; c < 3; c++) {
      const cell = b[r][c];
      if (cell === "X") {
        row.push("❌");
      } else if (cell === "O") {
        row.push("⭕");
      } else {
        if (state.status === "in_progress") {
          const link = `https://github.com/${repo}/issues/new?title=ttt%7C${r}%7C${c}&body=Hech+narsani+o%27zgartirmang.+Faqat+%27Submit+new+issue%27+tugmasini+bosing.`;
          row.push(`[⬜](${link})`);
        } else {
          row.push("⬜");
        }
      }
    }
    table += `| ${row.join(" | ")} |\n`;
  }

  const resetLink = `https://github.com/${repo}/issues/new?title=ttt%7Creset&body=Hech+narsani+o%27zgartirmang.+Faqat+%27Submit+new+issue%27+tugmasini+bosing.`;

  return `
${statusMsg}

${table}
<p align="center">
  <a href="${resetLink}">
    <img src="https://img.shields.io/badge/🔄_Yangi_o'yin_boshlash-Restart-blue?style=for-the-badge" alt="Restart Game" />
  </a>
</p>

> 📊 **O'yinlar statistikasi:** Jami o'yinlar: **${state.totalGames}** | O'yinchilar yutug'i: **${state.playerWins}** | Bot yutug'i: **${state.botWins}** | Durang: **${state.draws}**
`;
}

async function main() {
  const issueTitle = process.env.ISSUE_TITLE || "";
  const issueUser = process.env.ISSUE_USER || "Visitor";
  const state = loadState();

  if (issueTitle.includes("ttt|reset")) {
    state.board = [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]];
    state.status = "in_progress";
    state.lastPlayer = issueUser;
  } else if (issueTitle.startsWith("ttt|")) {
    const parts = issueTitle.split("|");
    const r = parseInt(parts[1], 10);
    const c = parseInt(parts[2], 10);

    if (!isNaN(r) && !isNaN(c) && r >= 0 && r < 3 && c >= 0 && c < 3) {
      if (state.status === "in_progress" && state.board[r][c] === " ") {
        // Player move
        state.board[r][c] = "X";
        state.lastPlayer = issueUser;

        let res = checkWinner(state.board);
        if (res === "X") {
          state.status = "player_won";
          state.totalGames++;
          state.playerWins++;
        } else if (res === "DRAW") {
          state.status = "draw";
          state.totalGames++;
          state.draws++;
        } else {
          // Bot move
          const bm = botMove(state.board);
          if (bm) {
            state.board[bm[0]][bm[1]] = "O";
            res = checkWinner(state.board);
            if (res === "O") {
              state.status = "bot_won";
              state.totalGames++;
              state.botWins++;
            } else if (res === "DRAW") {
              state.status = "draw";
              state.totalGames++;
              state.draws++;
            }
          }
        }
      }
    }
  }

  saveState(state);

  // Update README
  const content = renderMarkdown(state);
  let readme = fs.readFileSync(README_FILE, 'utf8');
  const startTag = "<!-- TIC_TAC_TOE_START -->";
  const endTag = "<!-- TIC_TAC_TOE_END -->";

  if (readme.includes(startTag) && readme.includes(endTag)) {
    const before = readme.substring(0, readme.indexOf(startTag) + startTag.length);
    const after = readme.substring(readme.indexOf(endTag));
    readme = `${before}\n${content}\n${after}`;
    fs.writeFileSync(README_FILE, readme);
    console.log("README.md updated with game board!");
  } else {
    console.log("TIC_TAC_TOE tags not found in README.md");
  }
}

main().catch(console.error);
