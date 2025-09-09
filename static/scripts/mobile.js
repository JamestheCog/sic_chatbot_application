function setupMobileViewport() {
    // Check if mobile device
    const isMobile = /iPhone|iPad|iPod|Android/i.test(navigator.userAgent);
    
    if (isMobile) {
        // Set viewport height properly
        document.documentElement.style.setProperty('--vh', `${window.innerHeight * 0.01}px`);
        
        // Listen for window resize (keyboard show/hide)
        window.addEventListener('resize', () => {
            document.documentElement.style.setProperty('--vh', `${window.innerHeight * 0.01}px`);
        });
        
        // Scroll to bottom when input is focused
        chat_input.addEventListener('focus', () => {
            setTimeout(() => {
                chat_messages.scrollTop = chat_messages.scrollHeight;
            }, 300);
        });
    }
}