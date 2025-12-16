const express = require("express");
const mysql = require("mysql2/promise");
const cors = require("cors");

const app = express();
app.use(cors());
app.use(express.json());

//DB connections
const db = mysql.createPool({
  host: "127.0.0.1",
  user: "izumo",
  password: "izumo@123",
  database: "izumo-ia",
});

//create new chat
app.post("/api/chat", async (req, res) => {
  const { title } = req.body;
  const [result] = await db.query("INSERT INTO chats (title) VALUES (?)", [
    title,
  ]);
  res.json({ id: result.insertId, title });
});

//add message

app.post("/api/message", async (req, res) => {
  const { chat_id, role, text } = req.body;

  await db.query(
    "INSERT INTO messages (chat_id, role, text) VALUES (?, ?, ?)",
    [chat_id, role, text]
  );
  res.json({ ok: true });
});

//list chats
app.get("/api/chats", async (req, res) => {
  const [rows] = await db.query("SELECT * FROM chats ORDER BY id DESC");
  res.json(rows)
});

//load messages from a chat
app.get("/api/chat/:id", async (req, res) => {
  const chatId = req.params.id;
  const [rows] = await db.query(
    "SELECT * FROM messages WHERE chat_id = ? ORDER BY id ASC",
    [chatId]
  );
  res.json(rows);
});

app.listen(3000, () => console.log("server running on port 3000"));
