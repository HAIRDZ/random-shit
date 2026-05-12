const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

function changeMessage() {
    const msgs = [
        "Mãi đỉnh nhé! 🌟",
        "Tuổi mới giàu sang phú quý! 💰",
        "Luôn cười tươi như hoa nhé! 🌸",
        "Vạn sự như ý! 🎈"
    ];
    document.getElementById('message').innerText = msgs[Math.floor(Math.random() * msgs.length)];
}

// Hiệu ứng pháo hoa đơn giản
class Particle {
    constructor() {
        this.x = Math.random() * canvas.width;
        this.y = canvas.height;
        this.size = Math.random() * 5 + 1;
        this.speedY = Math.random() * 3 + 5;
        this.color = `hsl(${Math.random() * 360}, 100%, 50%)`;
    }
    update() {
        this.y -= this.speedY;
        if (this.size > 0.2) this.size -= 0.1;
    }
    draw() {
        ctx.fillStyle = this.color;
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
        ctx.fill();
    }
}

const particles = [];
function animate() {
    ctx.fillStyle = 'rgba(0, 0, 0, 0.1)';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    if (Math.random() < 0.1) particles.push(new Particle());
    for (let i = 0; i < particles.length; i++) {
        particles[i].update();
        particles[i].draw();
        if (particles[i].y < 0) {
            particles.splice(i, 1);
            i--;
        }
    }
    requestAnimationFrame(animate);
}
animate();