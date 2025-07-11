// projects/ambient_ui/FeedbackPane.js
import React, { useState } from 'react';

const FeedbackPane = ({ item }) => {
  const [feedback, setFeedback] = useState('');

  const handleSubmit = () => {
    console.log(`Feedback submitted for item ${item.id}:`, feedback);
    // In a real implementation, this would emit a 'feedback.submitted' event.
  };

  if (!item) {
    return null;
  }

  return (
    <div className="feedback-pane">
      <h4>Feedback for: {item.title}</h4>
      <textarea
        value={feedback}
        onChange={(e) => setFeedback(e.target.value)}
        placeholder="Your feedback..."
      />
      <button onClick={handleSubmit}>Submit</button>
    </div>
  );
};

export default FeedbackPane;
