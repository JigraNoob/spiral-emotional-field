document.addEventListener('DOMContentLoaded', function() {
    // Modal related elements
    const giftModal = document.getElementById('giftModal');
    const closeButton = giftModal.querySelector('.close-button');
    const modalMurmurText = document.getElementById('modalMurmurText');
    const modalCopyLink = document.getElementById('modalCopyLink');
    const copyLinkBtn = document.getElementById('copyLinkBtn');
    const copyFeedback = document.getElementById('copyFeedback');
    const modalContent = giftModal.querySelector('.modal-content'); // Define modalContent here

    // Define ritual phrases
    const ritualPhrases = {
        "Longing": "This ache once found light—may it guide another now.",
        "Movement": "Passed in motion, held in rhythm—gifted onward.",
        "Form": "This shape once held breath—may it cradle another soul.",
        "Infrastructure": "What was built here still shelters. May it reach again.",
        "Connection": "This thread touched another. Let it extend once more.",
        "Trust": "This echo held weight and care. May it be received gently.",
        "Coherence": "This alignment once steadied the field. May it clarify yours.",
        "Adaptation": "Changed and carried, this murmur still belongs. Take it."
    };

    function getRitualPhrase(toneform) {
        return ritualPhrases[toneform] || "A murmur, offered."; // Default phrase
    }

    closeButton.addEventListener('click', function() {
        giftModal.style.display = 'none';
    });

    window.addEventListener('click', function(event) {
        if (event.target == giftModal) {
            giftModal.style.display = 'none';
        }
    });

    let currentToneform = ''; // Variable to store the toneform of the currently open modal

    // When the user clicks on a gift link, open the modal
    document.querySelectorAll('.gift-link').forEach(link => {
        link.addEventListener('click', function(event) {
            event.preventDefault(); // Prevent default link behavior

            const murmurText = this.dataset.murmurText;
            const sessionId = this.dataset.sessionId;
            const echoId = this.dataset.echoId;
            currentToneform = this.dataset.toneform; // Set currentToneform

            const playbackLink = `${window.location.origin}/echo/playback/${sessionId}#echo-${echoId}`;

            modalMurmurText.textContent = `"${murmurText}"`;
            modalCopyLink.value = playbackLink;
            copyFeedback.style.display = 'none'; // Hide feedback on new open

            // Display ritual phrase
            const ritualPhraseElement = document.getElementById('modalRitualPhrase');
            if (ritualPhraseElement) {
                ritualPhraseElement.textContent = getRitualPhrase(currentToneform);
            }

            // Apply toneform-colored glow
            const toneformColors = JSON.parse('{{ toneform_colors | tojson | safe }}');
            if (currentToneform && toneformColors[currentToneform]) {
                modalContent.style.boxShadow = `0 0 20px 5px ${toneformColors[currentToneform]}`;
            } else {
                modalContent.style.boxShadow = 'none'; // Remove glow if no toneform or color
            }

            giftModal.style.display = 'flex'; // Use flex to center
        });
    });

    copyLinkBtn.addEventListener('click', function() {
        modalCopyLink.select();
        modalCopyLink.setSelectionRange(0, 99999); // For mobile devices

        navigator.clipboard.writeText(modalCopyLink.value).then(() => {
            copyFeedback.style.display = 'block';
            copyFeedback.classList.remove('animate'); // Reset animation
            void copyFeedback.offsetWidth; // Trigger reflow
            copyFeedback.classList.add('animate'); // Start animation

            setTimeout(() => {
                copyFeedback.style.display = 'none';
                copyFeedback.classList.remove('animate');
            }, 2000); // Hide after 2 seconds

            // Particle generation
            const particleContainer = giftModal.querySelector('.particle-container');
            const numParticles = Math.floor(Math.random() * 4) + 3; // 3 to 6 particles

            for (let i = 0; i < numParticles; i++) {
                const particle = document.createElement('div');
                particle.classList.add('particle');
                // Use currentToneform for particle color
                const toneformColors = JSON.parse('{{ toneform_colors | tojson | safe }}');
                particle.style.backgroundColor = toneformColors[currentToneform];

                // Random initial position within the modal content
                const modalContentRect = modalContent.getBoundingClientRect();
                const startX = Math.random() * modalContentRect.width;
                const startY = Math.random() * modalContentRect.height;
                particle.style.left = `${startX}px`;
                particle.style.top = `${startY}px`;

                // Random drift values
                const xDrift = (Math.random() - 0.5) * 100; // -50 to 50px
                const yDrift = -50 - (Math.random() * 50); // -50 to -100px (upwards)
                particle.style.setProperty('--x-drift', `${xDrift}px`);
                particle.style.setProperty('--y-drift', `${yDrift}px`);

                particleContainer.appendChild(particle);

                // Remove particle after animation
                particle.addEventListener('animationend', () => {
                    particle.remove();
                });
            }

        }).catch(err => {
            console.error('Failed to copy: ', err);
            alert('Failed to copy link. Please copy it manually: ' + modalCopyLink.value);
        });
    });

    // Filter functionality
    const filterButtons = document.querySelectorAll('.filter-button');
    const murmurCards = document.querySelectorAll('.murmur-card');

    filterButtons.forEach(button => {
        button.addEventListener('click', function() {
            const selectedToneform = this.dataset.toneform;

            filterButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');

            murmurCards.forEach(card => {
                const cardToneform = card.dataset.toneform; // Use data-toneform attribute
                if (selectedToneform === 'all' || cardToneform === selectedToneform) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    });

    // Initial display of all cards
    murmurCards.forEach(card => card.style.display = 'block');

    // Sorting functionality
    const sortButtons = document.querySelectorAll('.sort-button');

    sortButtons.forEach(button => {
        button.addEventListener('click', function() {
            const sortBy = this.dataset.sortBy;
            const sortOrder = this.dataset.sortOrder;

            sortButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');

            let sortedCards = Array.from(murmurCards);

            if (sortBy === 'seeded_at') {
                sortedCards.sort((a, b) => {
                    const dateA = new Date(a.querySelector('.murmur-meta').textContent.split('Seeded: ')[1].split('\n')[0].trim());
                    const dateB = new Date(b.querySelector('.murmur-meta').textContent.split('Seeded: ')[1].split('\n')[0].trim());
                    return sortOrder === 'asc' ? dateA - dateB : dateB - dateA;
                });
            } else if (sortBy === 'gift_status') {
                sortedCards.sort((a, b) => {
                    // Assuming 'gift-link' presence indicates not gifted, absence indicates gifted
                    // This needs to be refined based on actual data structure for 'gifted' status
                    const aGifted = a.querySelector('.gift-link') ? 0 : 1; // 0 if has gift link (not gifted), 1 if no gift link (gifted)
                    const bGifted = b.querySelector('.gift-link') ? 0 : 1;
                    return aGifted - bGifted; // Sort to show not-gifted first
                });
            }

            // Re-append sorted cards to the grid
            const murmurGrid = document.querySelector('.murmur-grid');
            sortedCards.forEach(card => murmurGrid.appendChild(card));
        });
    });
});
