document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('groupForm');
    const messageParagraph = document.getElementById('message');

    form.addEventListener('submit', async (event) => {
        event.preventDefault();

        const formData = new FormData(form);
        const data = {};
        formData.forEach((value, key) => {
            if (key === 'stewards' || key === 'assigned_seeds') {
                data[key] = value.split(',').map(item => item.trim());
            } else {
                data[key] = value;
            }
        });

        try {
            const response = await fetch('/record_group', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });

            const result = await response.json();

            if (response.ok) {
                messageParagraph.textContent = `Success: ${result.message}`;
                messageParagraph.style.color = 'green';
                form.reset(); // Clear the form on success
            } else {
                messageParagraph.textContent = `Error: ${result.error || 'Something went wrong'}`;
                messageParagraph.style.color = 'red';
            }
        } catch (error) {
            console.error('Error:', error);
            messageParagraph.textContent = `Network Error: ${error.message}`;
            messageParagraph.style.color = 'red';
        }
    });
});
