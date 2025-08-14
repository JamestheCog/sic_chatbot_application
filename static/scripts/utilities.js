const night_mode = document.querySelector('.mode-toggle');

// Add an event listener here:
night_mode.addEventListener('click', () => {
    document.body.setAttribute(
        'data-theme', document.body.getAttribute('data-theme') === 'dark' ? 'light' : 'dark'
    )
})