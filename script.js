document.addEventListener('DOMContentLoaded', function() {
    const voiceButton = document.getElementById('voice-button');

    if (voiceButton) {
        voiceButton.addEventListener('click', function() {
            // Trigger voice search
            fetch('/voice_search', {
                method: 'POST'
            })
            .then(response => response.text())
            .then(data => {
                document.querySelector('.container').innerHTML = data;
            });
        });
    }
});
