// Displaying current date in the Notice Bar
const today = new Date();
  // Format the date manually
  const dayName = today.toLocaleDateString('en-US', { weekday: 'long' });
  const dayNumber = today.getDate();
  const monthName = today.toLocaleDateString('en-US', { month: 'long' });
  document.getElementById('current-date').textContent =
      `${dayName}, ${dayNumber} ${monthName}`;