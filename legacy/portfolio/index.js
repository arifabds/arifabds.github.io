// Form Gönderim İşlemi
document.getElementById('contactForm').addEventListener('submit', function(event) {
    event.preventDefault();
    alert('Teşekkürler! Mesajınız başarıyla gönderildi.');
    this.reset();
});

// Geçiş Animasyonları
const sections = document.querySelectorAll('section');

window.addEventListener('scroll', () => {
    const triggerBottom = window.innerHeight * 0.8;

    sections.forEach(section => {
        const sectionTop = section.getBoundingClientRect().top;

        if (sectionTop < triggerBottom) {
            section.style.opacity = '1';
            section.style.transform = 'translateY(0)';
        } else {
            section.style.opacity = '0';
            section.style.transform = 'translateY(30px)';
        }
    });
});
