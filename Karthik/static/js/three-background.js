// Three.js 3D Background Animation with Programming Symbols
let scene, camera, renderer, symbolsGroup;
let mouseX = 0, mouseY = 0;
const symbolTextures = [];
const symbols = ['{ }', '</>', '#', ';', '()', '[]', '=>', '++', '!=', '&&', '||', 'Py', 'C++', 'Js', 'Java'];

function createSymbolTexture(text) {
    const canvas = document.createElement('canvas');
    canvas.width = 128;
    canvas.height = 128;
    const ctx = canvas.getContext('2d');

    ctx.fillStyle = 'rgba(255, 255, 255, 0)';
    ctx.fillRect(0, 0, 128, 128);

    ctx.font = 'bold 50px "Courier New", monospace';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';

    // Gradient text for a premium look
    const gradient = ctx.createLinearGradient(0, 0, 128, 128);
    gradient.addColorStop(0, '#667eea');
    gradient.addColorStop(1, '#764ba2');

    ctx.shadowColor = 'rgba(102, 126, 234, 0.5)';
    ctx.shadowBlur = 15;
    ctx.fillStyle = gradient;
    ctx.fillText(text, 64, 64);

    return new THREE.CanvasTexture(canvas);
}

function initBackground() {
    const container = document.getElementById('three-container');
    if (!container) return;

    scene = new THREE.Scene();
    camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    camera.position.z = 50;

    renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(window.devicePixelRatio);
    container.appendChild(renderer.domElement);

    // Pre-create textures
    symbols.forEach(s => symbolTextures.push(createSymbolTexture(s)));

    // Create 3D floating symbols group
    symbolsGroup = new THREE.Group();
    for (let i = 0; i < 120; i++) {
        const texture = symbolTextures[Math.floor(Math.random() * symbolTextures.length)];
        const material = new THREE.SpriteMaterial({
            map: texture,
            transparent: true,
            opacity: Math.random() * 0.3 + 0.1 // Keeping it subtle
        });
        const sprite = new THREE.Sprite(material);

        const scale = Math.random() * 5 + 3;
        sprite.scale.set(scale, scale, 1);

        sprite.position.set(
            (Math.random() - 0.5) * 150,
            (Math.random() - 0.5) * 150,
            (Math.random() - 0.5) * 150
        );

        sprite.userData = {
            rotationSpeed: (Math.random() - 0.5) * 0.015,
            phase: Math.random() * Math.PI * 2,
            yOffset: (Math.random() - 0.5) * 20
        };

        symbolsGroup.add(sprite);
    }
    scene.add(symbolsGroup);

    window.addEventListener('resize', onWindowResize, false);
    document.addEventListener('mousemove', onDocumentMouseMove, false);

    animateBackground();
}

function onWindowResize() {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
}

function onDocumentMouseMove(event) {
    mouseX = (event.clientX - window.innerWidth / 2) / 100;
    mouseY = (event.clientY - window.innerHeight / 2) / 100;
}

function animateBackground() {
    requestAnimationFrame(animateBackground);

    const time = Date.now() * 0.0008;

    symbolsGroup.children.forEach(sprite => {
        // Floating motion
        sprite.position.y += Math.sin(time + sprite.userData.phase) * 0.03;
        sprite.material.rotation += sprite.userData.rotationSpeed;
    });

    // Gentle camera parallax
    symbolsGroup.rotation.x += (mouseY * 0.08 - symbolsGroup.rotation.x) * 0.05;
    symbolsGroup.rotation.y += (mouseX * 0.08 - symbolsGroup.rotation.y) * 0.05;

    renderer.render(scene, camera);
}

// Start if three.js loaded
if (typeof THREE !== 'undefined') {
    initBackground();
} else {
    // Fallback if script loading is async
    window.addEventListener('load', () => {
        if (typeof THREE !== 'undefined') initBackground();
    });
}
