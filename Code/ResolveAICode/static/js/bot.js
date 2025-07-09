// Resolve AI Chatbot Logic (Plagiarism-Free, Modern, Accessible)

document.addEventListener('DOMContentLoaded', () => {
  const startBtn = document.getElementById('start-journey');
  const chatSection = document.getElementById('chat-section');
  const header = document.querySelector('.resolve-header');
  const chatForm = document.getElementById('chat-form');
  const chatInput = document.getElementById('user-input');
  const chatMessages = document.getElementById('chat-messages');
  const suggestionsDiv = document.getElementById('suggestions');

  // Sentiment-aware suggestions (simple demo)
  const suggestions = [
    'I feel anxious',
    'I need motivation',
    'Can you help me relax?',
    'I want to talk about my day',
    'I feel happy today',
  ];

  function showSuggestions() {
    suggestionsDiv.innerHTML = '';
    suggestions.forEach(text => {
      const btn = document.createElement('button');
      btn.className = 'suggestion-btn';
      btn.textContent = text;
      btn.onclick = () => {
        chatInput.value = text;
        chatInput.focus();
      };
      suggestionsDiv.appendChild(btn);
    });
  }

  // Onboarding to chat transition
  startBtn.addEventListener('click', () => {
    header.style.display = 'none';
    chatSection.style.display = 'flex';
    chatInput.focus();
    showSuggestions();
    addBotMessage('Welcome to Resolve AI! This is a safe, supportive space. How are you feeling today?');
  });

  // Typing animation for AI
  function addBotMessage(text) {
    const msgDiv = document.createElement('div');
    msgDiv.className = 'message bot';
    const bubble = document.createElement('div');
    bubble.className = 'bubble bot';
    bubble.setAttribute('aria-live', 'polite');
    bubble.textContent = '';
    msgDiv.appendChild(bubble);
    chatMessages.appendChild(msgDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    let i = 0;
    function typeChar() {
      if (i < text.length) {
        bubble.textContent += text[i++];
        setTimeout(typeChar, 18 + Math.random() * 30);
      }
    }
    typeChar();
  }

  function addUserMessage(text) {
    const msgDiv = document.createElement('div');
    msgDiv.className = 'message user';
    const bubble = document.createElement('div');
    bubble.className = 'bubble user';
    bubble.textContent = text;
    msgDiv.appendChild(bubble);
    chatMessages.appendChild(msgDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }

  // Chat form submit
  chatForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const userText = chatInput.value.trim();
    if (!userText) return;
    addUserMessage(userText);
    chatInput.value = '';
    showSuggestions();
    addBotMessage('...'); // Typing indicator
    // Fetch AI response
    try {
      const res = await fetch('/get?msg=' + encodeURIComponent(userText));
      const data = await res.text();
      // Remove typing indicator
      chatMessages.removeChild(chatMessages.lastChild);
      addBotMessage(data);
    } catch {
      chatMessages.removeChild(chatMessages.lastChild);
      addBotMessage('Sorry, I am having trouble responding right now.');
    }
  });

  // Accessibility: focus chat on new message
  const observer = new MutationObserver(() => {
    chatMessages.setAttribute('tabindex', '0');
    chatMessages.focus();
  });
  observer.observe(chatMessages, { childList: true });
});
