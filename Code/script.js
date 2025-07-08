// Mood Journal logic
const journalForm = document.getElementById('journalForm');
const journalEntry = document.getElementById('journalEntry');
const journalEntries = document.getElementById('journalEntries');

if (journalForm && journalEntry && journalEntries) {
  // Load entries from localStorage
  function loadEntries() {
    journalEntries.innerHTML = '';
    const entries = JSON.parse(localStorage.getItem('moodJournal') || '[]');
    entries.forEach((entry, idx) => {
      const div = document.createElement('div');
      div.className = 'journal-entry';
      div.textContent = entry;
      journalEntries.appendChild(div);
    });
  }

  journalForm.addEventListener('submit', function(e) {
    e.preventDefault();
    const value = journalEntry.value.trim();
    if (value) {
      const entries = JSON.parse(localStorage.getItem('moodJournal') || '[]');
      entries.unshift(value);
      localStorage.setItem('moodJournal', JSON.stringify(entries));
      journalEntry.value = '';
      loadEntries();
    }
  });

  loadEntries();
}

// Chat input placeholder logic
const chatInput = document.querySelector('.chat-input');
const chatWindow = document.querySelector('.chat-window');
if (chatInput && chatWindow) {
  chatInput.addEventListener('submit', function(e) {
    e.preventDefault();
    const input = document.getElementById('userInput');
    const value = input.value.trim();
    if (value) {
      const userMsg = document.createElement('div');
      userMsg.className = 'message user';
      userMsg.textContent = value;
      chatWindow.appendChild(userMsg);
      input.value = '';
      // Placeholder for AI response
      setTimeout(() => {
        const aiMsg = document.createElement('div');
        aiMsg.className = 'message ai';
        aiMsg.textContent = 'Thank you for sharing! (AI response placeholder)';
        chatWindow.appendChild(aiMsg);
        chatWindow.scrollTop = chatWindow.scrollHeight;
      }, 700);
      chatWindow.scrollTop = chatWindow.scrollHeight;
    }
  });
} 