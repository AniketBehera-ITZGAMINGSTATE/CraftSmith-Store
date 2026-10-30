import os
from flask import Flask, render_template_string

app = Flask(__name__)

HTML_CONTENT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Craft Smith</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: Roboto, Arial, sans-serif; }
        body { background-color: #f1f2f6; color: #212121; padding-bottom: 40px; }
        header { background-color: #2874f0; color: white; padding: 12px 10%; display: flex; align-items: center; justify-content: space-between; }
        .logo { font-size: 22px; font-weight: bold; font-style: italic; }
        .container { max-width: 1200px; margin: 20px auto; padding: 0 15px; }
        .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(240px, 1fr)); gap: 18px; }
        .card { background: white; border-radius: 6px; padding: 15px; text-align: center; border: 1px solid #e0e0e0; display: flex; flex-direction: column; justify-content: space-between; }
        
        /* Paper craft style for first two items */
        .paper-style {
            background-color: #fcf8ed !important;
            border: 2px dashed #b5a48b !important;
            box-shadow: 2px 3px 0px #d4c5b0;
        }
        
        .card img { width: 100%; height: 170px; object-fit: contain; border-radius: 4px; margin-bottom: 10px; background: #fff; }
        .card h4 { font-size: 15px; margin-bottom: 6px; }
        .card .price { font-size: 17px; font-weight: bold; color: #388e3c; margin-bottom: 8px; }
        
        .theme-select-box { display: flex; flex-direction: column; gap: 6px; margin: 8px 0; text-align: left; }
        .theme-select-box label { font-size: 12px; font-weight: bold; color: #555; }
        .theme-select-box select, .theme-select-box input { width: 100%; padding: 6px; border: 1px solid #ccc; border-radius: 4px; font-size: 12px; outline: none; }
        
        canvas { border: 1px dashed #888; background: #fff; cursor: crosshair; margin-top: 4px; }
        .btn-clear { background: #e74c3c; color: white; border: none; padding: 3px 8px; font-size: 10px; border-radius: 3px; cursor: pointer; margin-top: 2px; }
        
        .btn-add { background: #ff9f00; color: white; border: none; padding: 9px 14px; margin-top: 10px; border-radius: 4px; cursor: pointer; font-weight: bold; width: 100%; font-size: 14px; }
        .btn-add:hover { background: #e68f00; }
    </style>
</head>
<body>

    <header>
        <div class="logo">Craft Smith</div>
    </header>

    <div class="container">
        <h3 style="margin-bottom: 15px;">Paper Crafts</h3>
        <div class="grid" id="product-grid"></div>
    </div>

    <script>
        const footballTeams = [
            "Real Madrid", "Barcelona", "Liverpool", "Arsenal", "Al Nassr", 
            "Bayern Munich", "Juventus", "Manchester United", "Manchester City", "Chelsea", "Santos FC"
        ];

        const carModels = ["BMW", "Mercedes", "Lamborghini", "Ferrari", "Supra", "Bugatti"];
        const bikeModels = ["Kawasaki Ninja H2R", "Ducati Panigale V4 R", "Yamaha YZF-R1 [Black/Stealth Edition]", "Royal Enfield Meteor"];

        const themes = [
            "1. Pokémon",
            "2. Football",
            "3. Space",
            "4. Custom (Draw below)",
            "5. Barbie",
            "6. Hello Kitty",
            "7. Cute Smiley",
            "8. Cinnamoroll",
            "9. Kuromi",
            "10. My Melody",
            "11. Cars",
            "12. Bikes"
        ];

        // Clean SVG string definitions with quotes properly escaped
        const sketchWalletA = "data:image/svg+xml;charset=utf-8,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 500 400' fill='none' stroke='black' stroke-width='4'%3E%3Crect x='20' y='50' width='460' height='300'/%3E%3Cpath d='M 20 50 Q 250 10 480 50'/%3E%3Cpolygon points='250,50 480,200 250,350 20,200'/%3E%3Cline x1='250' y1='50' x2='250' y2='350'/%3E%3Cline x1='20' y1='200' x2='120' y2='200'/%3E%3Cline x1='480' y1='200' x2='380' y2='200'/%3E%3Ccircle cx='230' cy='110' r='3' fill='black'/%3E%3Ccircle cx='120' cy='220' r='3' fill='black'/%3E%3Ccircle cx='380' cy='280' r='3' fill='black'/%3E%3C/svg%3E";
        
        const sketchWalletB = "data:image/svg+xml;charset=utf-8,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 500 300' fill='none' stroke='black' stroke-width='4'%3E%3Crect x='20' y='40' width='460' height='220'/%3E%3Cpath d='M 20 40 Q 250 10 480 40'/%3E%3Cline x1='250' y1='40' x2='250' y2='260'/%3E%3Cpolygon points='250,40 330,150 250,230 170,150'/%3E%3Cline x1='240' y1='40' x2='240' y2='230'/%3E%3Cline x1='260' y1='40' x2='260' y2='230'/%3E%3Ctext x='180' y='140' font-size='20' fill='black' stroke='none'%3Etokin%3C/text%3E%3Ctext x='270' y='140' font-size='20' fill='black' stroke='none'%3Ectb+%3C/text%3E%3C/svg%3E";

        const sketchOrigamiWallet = "data:image/svg+xml;charset=utf-8,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 300 200' fill='none' stroke='%23333' stroke-width='3'%3E%3Crect x='10' y='20' width='130' height='150' fill='%23f7b731'/%3E%3Crect x='140' y='20' width='130' height='150' fill='%23f7b731'/%3E%3Crect x='150' y='40' width='110' height='40' fill='%23fa8231'/%3E%3Crect x='160' y='30' width='90' height='30' fill='%2320bf6b'/%3E%3C/svg%3E";

        const sketchSlinky = "data:image/svg+xml;charset=utf-8,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 200 200'%3E%3Cpath d='M 20 180 Q 20 20 100 20 Q 180 20 180 180' fill='none' stroke='%23ff5252' stroke-width='20'/%3E%3Cpath d='M 30 180 Q 30 40 100 40 Q 170 40 170 180' fill='none' stroke='%23ffb142' stroke-width='20'/%3E%3Cpath d='M 40 180 Q 40 60 100 60 Q 160 60 160 180' fill='none' stroke='%232ed573' stroke-width='20'/%3E%3C/svg%3E";

        const sketchAirplane = "data:image/svg+xml;charset=utf-8,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 300 200' fill='none' stroke='%23333' stroke-width='3'%3E%3Cpolygon points='20,100 280,30 200,100' fill='%23ffffff'/%3E%3Cpolygon points='20,100 280,30 250,170' fill='%23e0e0e0'/%3E%3C/svg%3E";

        const sketchDdakji = "data:image/svg+xml;charset=utf-8,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 200 200' fill='none' stroke='%23333' stroke-width='2'%3E%3Crect x='20' y='20' width='70' height='70' fill='%234b7bec'/%3E%3Cpolygon points='20,20 90,90 20,90' fill='%233867d6'/%3E%3Crect x='100' y='20' width='70' height='70' fill='%23eb3b5a'/%3E%3Cpolygon points='100,20 170,90 100,90' fill='%23fc5c65'/%3E%3C/svg%3E";

        const products = [
            { id: 1, name: "Paper Wallet (Design 1)", price: 10, isWallet: true, isPaper: true, image: sketchWalletA },
            { id: 2, name: "Paper Wallet (Design 2)", price: 10, isWallet: true, isPaper: true, image: sketchWalletB },
            { id: 3, name: "Origami Paper Wallet", price: 10, isWallet: true, isPaper: false, image: sketchOrigamiWallet },
            { id: 4, name: "Paper Slinky", price: 30, isWallet: false, isPaper: false, image: sketchSlinky },
            { id: 5, name: "Origami Glider Airplane", price: 10, isWallet: false, isPaper: false, image: sketchAirplane },
            { id: 6, name: "Korean Ddakji", price: 10, isWallet: false, isPaper: false, image: sketchDdakji }
        ];

        const grid = document.getElementById('product-grid');
        grid.innerHTML = products.map(p => {
            let themeControls = '';
            if (p.isWallet) {
                themeControls = `
                    <div class="theme-select-box">
                        <label>Theme:</label>
                        <select id="theme-${p.id}" onchange="handleThemeChange(${p.id})">
                            ${themes.map(t => `<option value="${t}">${t}</option>`).join('')}
                        </select>
                        
                        <div id="sub-team-container-${p.id}" style="display: none;">
                            <label>Club:</label>
                            <select id="team-${p.id}">
                                ${footballTeams.map(ft => `<option value="${ft}">${ft}</option>`).join('')}
                            </select>
                        </div>

                        <div id="sub-car-container-${p.id}" style="display: none;">
                            <label>Car Model:</label>
                            <select id="car-${p.id}">
                                ${carModels.map(c => `<option value="${c}">${c}</option>`).join('')}
                            </select>
                        </div>

                        <div id="sub-bike-container-${p.id}" style="display: none;">
                            <label>Bike Model:</label>
                            <select id="bike-${p.id}">
                                ${bikeModels.map(b => `<option value="${b}">${b}</option>`).join('')}
                            </select>
                        </div>

                        <div id="custom-container-${p.id}" style="display: none;">
                            <label>Draw Custom Design:</label>
                            <canvas id="canvas-${p.id}" width="200" height="100"></canvas>
                            <button class="btn-clear" onclick="clearCanvas(${p.id})">Clear Drawing</button>
                        </div>
                    </div>
                `;
            }

            return `
                <div class="card ${p.isPaper ? 'paper-style' : ''}">
                    <img src="${p.image}" alt="${p.name}">
                    <h4>${p.name}</h4>
                    <div class="price">₹${p.price}</div>
                    ${themeControls}
                    <button class="btn-add" onclick="addToCart(${p.id})">Add to Cart</button>
                </div>
            `;
        }).join('');

        const canvasStates = {};
        function initCanvas(id) {
            const canvas = document.getElementById(`canvas-${id}`);
            if (!canvas || canvasStates[id]) return;
            const ctx = canvas.getContext('2d');
            let drawing = false;

            canvas.addEventListener('mousedown', () => drawing = true);
            canvas.addEventListener('mouseup', () => { drawing = false; ctx.beginPath(); });
            canvas.addEventListener('mousemove', (e) => {
                if (!drawing) return;
                const rect = canvas.getBoundingClientRect();
                ctx.lineWidth = 2;
                ctx.lineCap = 'round';
                ctx.strokeStyle = '#000';
                ctx.lineTo(e.clientX - rect.left, e.clientY - rect.top);
                ctx.stroke();
                ctx.beginPath();
                ctx.moveTo(e.clientX - rect.left, e.clientY - rect.top);
            });
            canvasStates[id] = { canvas, ctx };
        }

        function clearCanvas(id) {
            if (canvasStates[id]) {
                canvasStates[id].ctx.clearRect(0, 0, 200, 100);
            }
        }

        function handleThemeChange(productId) {
            const themeVal = document.getElementById(`theme-${productId}`).value;
            
            document.getElementById(`sub-team-container-${productId}`).style.display = themeVal.includes("Football") ? "block" : "none";
            document.getElementById(`sub-car-container-${productId}`).style.display = themeVal.includes("Cars") ? "block" : "none";
            document.getElementById(`sub-bike-container-${productId}`).style.display = themeVal.includes("Bikes") ? "block" : "none";
            
            const isCustom = themeVal.includes("Custom");
            document.getElementById(`custom-container-${productId}`).style.display = isCustom ? "block" : "none";
            if (isCustom) initCanvas(productId);
        }

        function addToCart(productId) {
            const product = products.find(p => p.id === productId);
            let details = `${product.name} (₹${product.price})`;

            if (product.isWallet) {
                const themeVal = document.getElementById(`theme-${productId}`).value;
                details += `\\nTheme: ${themeVal}`;

                if (themeVal.includes("Football")) {
                    details += ` (${document.getElementById(`team-${productId}`).value})`;
                } else if (themeVal.includes("Cars")) {
                    details += ` (${document.getElementById(`car-${productId}`).value})`;
                } else if (themeVal.includes("Bikes")) {
                    details += ` (${document.getElementById(`bike-${productId}`).value})`;
                } else if (themeVal.includes("Custom")) {
                    details += ` [Custom Drawing Included]`;
                }
            }

            alert('Added to cart!\\n\\n' + details);
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_CONTENT)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
