const express = require('express');
const cors = require('cors');
const fetch = require('node-fetch');
require('dotenv').config();

const app = express();
app.use(cors());
app.use(express.json());

app.post('/chat', async (req, res) => {
  const userMessage = req.body.message;

  const apiResponse = await fetch('https://api.openai.com/v1/chat/completions', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${process.env.OPENAI_API_KEY}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      model: 'gpt-3.5-turbo',
      messages: [
        { role: 'system', content: 'You are a helpful legal assistant for Mahboob Rizvi Law Associates. Provide only general legal information and suggest contacting a lawyer for specific help.' },
        { role: 'user', content: userMessage }
      ],
      temperature: 0.6
    })
  });

  const json = await apiResponse.json();
  const reply = json.choices?.[0]?.message?.content?.trim() || 'Sorry, I couldn’t get a response.';
  res.json({ reply });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Legal chatbot running on port ${PORT}`));
