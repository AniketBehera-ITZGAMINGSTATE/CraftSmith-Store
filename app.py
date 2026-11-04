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
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', Roboto, sans-serif; }
        body { background-color: #f1f2f6; color: #212121; padding-bottom: 60px; }
        
        header { 
            background-color: #2874f0; 
            color: white; 
            padding: 12px 6%; 
            display: flex; 
            align-items: center; 
            justify-content: space-between; 
            gap: 15px;
            position: sticky; 
            top: 0; 
            z-index: 1000; 
            box-shadow: 0 3px 6px rgba(0,0,0,0.15); 
        }
        .logo { font-size: 22px; font-weight: bold; font-style: italic; white-space: nowrap; }
        
        .search-container { display: flex; flex: 1; max-width: 500px; }
        .search-container input { width: 100%; padding: 8px 12px; border: none; border-radius: 4px 0 0 4px; outline: none; font-size: 13px; }
        .search-container button { background: #ffe500; border: none; padding: 8px 16px; cursor: pointer; font-weight: bold; color: #2874f0; border-radius: 0 4px 4px 0; }

        .header-actions { display: flex; gap: 10px; align-items: center; white-space: nowrap; }
        .auth-btn { background: white; color: #2874f0; border: none; padding: 8px 14px; font-weight: bold; border-radius: 4px; cursor: pointer; font-size: 13px; }
        .cart-icon-btn { background: #ffe500; color: #2874f0; border: none; padding: 8px 14px; font-weight: bold; border-radius: 4px; cursor: pointer; font-size: 13px; }
        
        .container { max-width: 1240px; margin: 25px auto; padding: 0 20px; }
        .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(270px, 1fr)); gap: 24px; align-items: start; }
        
        .card { 
            background: white; 
            border-radius: 8px; 
            padding: 16px; 
            text-align: center; 
            border: 1px solid #e0e0e0; 
            display: flex; 
            flex-direction: column; 
            justify-content: space-between; 
            box-shadow: 0 2px 8px rgba(0,0,0,0.06); 
            min-height: 520px;
        }
        .card:hover { transform: translateY(-3px); box-shadow: 0 6px 16px rgba(0,0,0,0.12); transition: all 0.2s ease-in-out; }
        
        .card-img-wrapper {
            width: 100%;
            height: 190px;
            background: #fafafa;
            border: 1px solid #eee;
            border-radius: 6px;
            margin-bottom: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 10px;
            overflow: hidden;
        }

        .card-img-wrapper img { 
            width: 100%; 
            height: 100%; 
            object-fit: contain; 
            border-radius: 4px; 
        }
        
        .card h4 { font-size: 16px; margin-bottom: 6px; color: #111; }
        .card .price { font-size: 18px; font-weight: bold; color: #28a745; margin-bottom: 8px; }
        
        .theme-select-box { display: flex; flex-direction: column; gap: 6px; margin: 8px 0; text-align: left; }
        .theme-select-box label { font-size: 11px; font-weight: bold; color: #555; text-transform: uppercase; }
        .theme-select-box select, .theme-select-box input { width: 100%; padding: 7px; border: 1px solid #ccc; border-radius: 4px; font-size: 12px; outline: none; }
        
        /* Dedicated Drawing Canvas Box */
        .canvas-container {
            border: 2px dashed #2874f0;
            background: #ffffff;
            border-radius: 6px;
            margin-top: 6px;
            padding: 4px;
            text-align: center;
        }

        canvas {
            background: #ffffff;
            border: 1px solid #e0e0e0;
            border-radius: 4px;
            cursor: crosshair;
            touch-action: none;
        }

        .color-palette {
            display: flex;
            gap: 6px;
            align-items: center;
            justify-content: center;
            margin-top: 6px;
        }

        .color-swatch {
            width: 18px;
            height: 18px;
            border-radius: 50%;
            cursor: pointer;
            border: 2px solid #fff;
            box-shadow: 0 0 2px rgba(0,0,0,0.4);
        }
        .color-swatch.active { transform: scale(1.2); border-color: #333; }

        .btn-tool {
            color: white;
            border: none;
            padding: 6px 10px;
            font-size: 11px;
            border-radius: 4px;
            cursor: pointer;
            font-weight: bold;
            margin-top: 6px;
            width: 100%;
        }
        .btn-clear { background: #dc3545; }
        .btn-lock { background: #10b981; }
        .btn-tool:disabled { background: #9ca3af !important; cursor: not-allowed; }
        
        .btn-group { display: flex; gap: 12px; margin-top: 14px; }
        .btn-add { background: #ff9f00; color: white; border: none; padding: 10px; border-radius: 4px; cursor: pointer; font-weight: bold; flex: 1; font-size: 13px; }
        .btn-buy { background: #fb641b; color: white; border: none; padding: 10px; border-radius: 4px; cursor: pointer; font-weight: bold; flex: 1; font-size: 13px; }
        .btn-add:hover { background: #e68f00; }
        .btn-buy:hover { background: #e0530f; }

        /* MODALS */
        .modal-overlay { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.6); display: none; justify-content: center; align-items: center; z-index: 2000; }
        .modal-box { background: white; padding: 24px; border-radius: 8px; width: 90%; max-width: 480px; box-shadow: 0 5px 20px rgba(0,0,0,0.2); position: relative; }
        .modal-box h3 { margin-bottom: 15px; color: #111; font-size: 18px; border-bottom: 1px solid #eee; padding-bottom: 8px; }
        .modal-box .close-btn { position: absolute; top: 12px; right: 16px; font-size: 20px; cursor: pointer; color: #888; }
        .form-group { margin-bottom: 12px; text-align: left; }
        .form-group label { display: block; font-size: 12px; font-weight: bold; margin-bottom: 4px; color: #444; }
        .form-group input, .form-group select { width: 100%; padding: 8px; border: 1px solid #ccc; border-radius: 4px; font-size: 13px; }
        .summary-row { display: flex; justify-content: space-between; font-size: 14px; margin: 8px 0; }
        .total-row { font-size: 16px; font-weight: bold; border-top: 1px solid #ddd; padding-top: 8px; margin-top: 8px; color: #2874f0; }
        .btn-confirm { background: #2874f0; color: white; border: none; padding: 10px; width: 100%; border-radius: 4px; font-size: 15px; font-weight: bold; cursor: pointer; margin-top: 12px; }
        .auth-switch { font-size: 12px; margin-top: 10px; color: #2874f0; cursor: pointer; text-decoration: underline; }
    </style>
</head>
<body>

    <header>
        <div class="logo">Craft Smith</div>
        
        <div class="search-container">
            <input type="text" id="searchInput" placeholder="Search paper wallets, ddakji, glider..." onkeyup="filterProducts()">
            <button>Search</button>
        </div>

        <div class="header-actions">
            <span id="userGreeting" style="font-size:13px; font-weight:bold; display:none;"></span>
            <button class="auth-btn" id="loginHeaderBtn" onclick="openModal('authModal')">Sign In / Register</button>
            <button class="cart-icon-btn" onclick="openCartModal()">🛒 Cart (<span id="cart-count">0</span>)</button>
        </div>
    </header>

    <div class="container">
        <h3 style="margin-bottom: 20px; color: #333; font-size: 20px;">Handcrafted Paper Collection</h3>
        <div class="grid" id="product-grid"></div>
    </div>

    <!-- AUTH MODAL -->
    <div class="modal-overlay" id="authModal">
        <div class="modal-box">
            <span class="close-btn" onclick="closeModal('authModal')">&times;</span>
            <h3 id="authTitle">Sign In</h3>
            
            <div class="form-group" id="nameGroup" style="display:none;">
                <label>Full Name</label>
                <input type="text" id="authName" placeholder="Enter full name">
            </div>
            <div class="form-group">
                <label>Email Address</label>
                <input type="email" id="authEmail" placeholder="name@example.com">
            </div>
            <div class="form-group">
                <label>Password</label>
                <input type="password" id="authPassword" placeholder="Enter password">
            </div>

            <button class="btn-confirm" id="authSubmitBtn" onclick="handleAuth()">Sign In</button>
            <div style="text-align:center;">
                <span class="auth-switch" id="authToggle" onclick="toggleAuthMode()">New to Craft Smith? Create an account</span>
            </div>
        </div>
    </div>

    <!-- BUY NOW MODAL -->
    <div class="modal-overlay" id="buyModal">
        <div class="modal-box">
            <span class="close-btn" onclick="closeModal('buyModal')">&times;</span>
            <h3>Checkout Order</h3>
            <div id="buyProductDetails" style="font-size:13px; margin-bottom:12px; color:#555; background:#f9f9f9; padding:8px; border-radius:4px;"></div>
            
            <div class="form-group">
                <label>Full Name</label>
                <input type="text" id="custName" placeholder="Enter your full name">
            </div>
            <div class="form-group">
                <label>Delivery Address</label>
                <input type="text" id="custAddress" placeholder="Street, Apartment / House No.">
            </div>
            <div class="form-group">
                <label>Delivery Location</label>
                <select id="custLocation" onchange="updateShipping()">
                    <option value="30">Local City / Metro (₹30 Delivery)</option>
                    <option value="50">Regional State (₹50 Delivery)</option>
                    <option value="90">National Outstation (₹90 Delivery)</option>
                    <option value="120">Express Air Delivery (₹120 Delivery)</option>
                </select>
            </div>

            <div class="summary-row">
                <span>Item Price:</span>
                <span id="summaryPrice">₹0</span>
            </div>
            <div class="summary-row">
                <span>Delivery Charge:</span>
                <span id="summaryShipping">₹30</span>
            </div>
            <div class="summary-row total-row">
                <span>Total Amount Payable:</span>
                <span id="summaryTotal">₹0</span>
            </div>

            <button class="btn-confirm" onclick="confirmOrder()">Confirm Order</button>
        </div>
    </div>

    <!-- CART MODAL -->
    <div class="modal-overlay" id="cartModal">
        <div class="modal-box">
            <span class="close-btn" onclick="closeModal('cartModal')">&times;</span>
            <h3>Your Shopping Cart</h3>
            <div id="cartList" style="max-height: 200px; overflow-y: auto; text-align: left; margin-bottom: 12px;"></div>
            <div class="summary-row total-row">
                <span>Cart Subtotal:</span>
                <span id="cartSubtotal">₹0</span>
            </div>
            <button class="btn-confirm" style="background:#fb641b;" onclick="checkoutCart()">Proceed to Buy All</button>
        </div>
    </div>

    <script>
        const footballTeams = ["Real Madrid", "Barcelona", "Liverpool", "Arsenal", "Al Nassr", "Bayern Munich", "Juventus", "Manchester United", "Manchester City", "Chelsea", "Santos FC"];
        const carModels = ["BMW", "Mercedes", "Lamborghini", "Ferrari", "Supra", "Bugatti"];
        const bikeModels = ["Kawasaki Ninja H2R", "Ducati Panigale V4 R", "Yamaha YZF-R1 [Black/Stealth Edition]", "Royal Enfield Meteor"];
        const marvelHeroes = ["1. Spider-Man", "2. Iron Man", "3. Thor", "4. Hulk", "5. Wolverine"];

        const walletThemes = [
            "1. Pokémon",
            "2. Football",
            "3. Limited Edition- 2026-27",
            "4. Space",
            "5. Custom (Import Picture or Draw)",
            "6. Barbie",
            "7. Hello Kitty",
            "8. Cute Smiley",
            "9. Cinnamoroll",
            "10. Kuromi",
            "11. My Melody",
            "12. Cars",
            "13. Bikes"
        ];

        const availableColors = ["#2874f0", "#dc3545", "#28a745", "#111111", "#ff9f00", "#6f42c1"];

        const imgCardHolderWallet = "data:image/svg+xml;charset=utf-8,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 -20 500 380' fill='%23ffffff' stroke='%23d0d0d0' stroke-width='2'%3E%3Crect x='10' y='10' width='480' height='320' rx='4' fill='%23fafafa'/%3E%3Crect x='30' y='10' width='440' height='60' fill='%23e6ecef' stroke='%23bcc4ca'/%3E%3Ctext x='150' y='48' font-size='20' fill='%231b7e46' font-weight='bold' stroke='none'%3E₹500 RESERVE BANK OF INDIA%3C/text%3E%3Crect x='30' y='90' width='440' height='220' fill='%23ffffff' stroke='%23cccccc'/%3E%3Crect x='50' y='140' width='190' height='100' fill='%230f4c81' rx='4'/%3E%3Ctext x='140' y='195' font-size='20' fill='%23ffffff' font-weight='bold' stroke='none'%3EVISA%3C/text%3E%3Crect x='260' y='140' width='190' height='100' fill='%231e1e1e' rx='4'/%3E%3Ctext x='340' y='195' font-size='20' fill='%23ea5b0c' font-weight='bold' stroke='none'%3ERuPay%3C/text%3E%3C/svg%3E";
        const imgDiamondSlotWallet = "data:image/svg+xml;charset=utf-8,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 -20 500 380' fill='%23ffffff' stroke='%23d0d0d0' stroke-width='2'%3E%3Crect x='10' y='10' width='480' height='320' rx='4' fill='%23fafafa'/%3E%3Crect x='30' y='10' width='440' height='60' fill='%23e6ecef' stroke='%23bcc4ca'/%3E%3Ctext x='150' y='48' font-size='20' fill='%231b7e46' font-weight='bold' stroke='none'%3E₹500 RESERVE BANK OF INDIA%3C/text%3E%3Crect x='30' y='90' width='440' height='220' fill='%23ffffff' stroke='%23cccccc'/%3E%3Cpolygon points='50,200 145,110 240,200 145,290' fill='%230f4c81'/%3E%3Cpolygon points='260,200 355,110 450,200 355,290' fill='%231e1e1e'/%3E%3Ctext x='115' y='205' font-size='16' fill='%23ffffff' font-weight='bold' stroke='none'%3EVISA%3C/text%3E%3Ctext x='315' y='205' font-size='16' fill='%23ea5b0c' font-weight='bold' stroke='none'%3ERuPay%3C/text%3E%3C/svg%3E";
        const imgEnvelopeFoldWallet = "data:image/svg+xml;charset=utf-8,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 -10 500 340' fill='none' stroke='%23cccccc' stroke-width='3'%3E%3Crect x='20' y='10' width='140' height='290' fill='%2300a8ff' rx='4'/%3E%3Cpolygon points='20,10 160,10 90,150' fill='%230088cc'/%3E%3Crect x='180' y='10' width='140' height='290' fill='%23e84118' rx='4'/%3E%3Cpolygon points='180,10 320,10 250,150' fill='%23c23616'/%3E%3Crect x='340' y='10' width='140' height='290' fill='%23ffffff' rx='4' stroke='%23b2bec3'/%3E%3Cpolygon points='340,10 480,10 410,150' fill='%23f5f6fa' stroke='%23b2bec3'/%3E%3C/svg%3E";
        const imgDdakjiTile = "data:image/svg+xml;charset=utf-8,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 -10 300 240' fill='none' stroke='%23333' stroke-width='2'%3E%3Crect x='30' y='10' width='110' height='110' fill='%234b7bec'/%3E%3Cpolygon points='30,10 140,120 30,120' fill='%233867d6'/%3E%3Crect x='160' y='10' width='110' height='110' fill='%23eb3b5a'/%3E%3Cpolygon points='160,10 270,120 160,120' fill='%23fc5c65'/%3E%3Ctext x='70' y='180' font-size='16' fill='%23555' stroke='none'%3EKorean Ddakji Battle Tile%3C/text%3E%3C/svg%3E";
        const imgCustomDdakjiTile = "data:image/svg+xml;charset=utf-8,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 -10 300 240' fill='none' stroke='%232874f0' stroke-width='2'%3E%3Crect x='30' y='10' width='240' height='150' fill='%23f0f7ff' rx='6' stroke-dasharray='4'/%3E%3Ctext x='75' y='90' font-size='15' fill='%232874f0' font-weight='bold' stroke='none'%3ECustom Artwork Ddakji%3C/text%3E%3C/svg%3E";
        const imgGliderPlaneCombined = "data:image/svg+xml;charset=utf-8,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 500 280' fill='none' stroke='%23555' stroke-width='3'%3E%3Cg transform='translate(20,20)'%3E%3Cpolygon points='100,10 10,230 100,200 190,230' fill='%23ffffff' stroke='%23888'/%3E%3Cline x1='100' y1='10' x2='100' y2='200' stroke='%23888'/%3E%3Ctext x='50' y='255' font-size='13' fill='%23666' stroke='none'%3ETop Fold View%3C/text%3E%3C/g%3E%3Cg transform='translate(240,20)'%3E%3Cpolygon points='10,40 220,130 10,190' fill='%23f5f5f5' stroke='%23888'/%3E%3Cpolygon points='10,40 220,130 30,90' fill='%23ffffff' stroke='%23888'/%3E%3Ctext x='70' y='255' font-size='13' fill='%23666' stroke='none'%3ESide Wing View%3C/text%3E%3C/g%3E%3C/svg%3E";

        const products = [
            { id: 1, name: "Card Holder Paper Wallet", price: 10, isWallet: true, image: imgCardHolderWallet },
            { id: 2, name: "Diamond Slot Paper Wallet", price: 10, isWallet: true, image: imgDiamondSlotWallet },
            { id: 3, name: "Envelope Fold Paper Wallet", price: 10, isWallet: true, image: imgEnvelopeFoldWallet },
            { id: 4, name: "Korean Ddakji (Classic Battle Tile)", price: 10, isWallet: false, image: imgDdakjiTile },
            { id: 5, name: "Custom Korean Ddakji (Import / Draw Tile)", price: 10, isCustomDdakji: true, image: imgCustomDdakjiTile },
            { id: 6, name: "Glider Paper Plane (Top & Side Fold)", price: 10, isWallet: false, image: imgGliderPlaneCombined }
        ];

        let cartItems = [];
        let currentCheckoutProduct = null;
        let isSignUpMode = false;
        let currentUser = null;
        const canvasStates = {};

        function renderProducts(list) {
            const grid = document.getElementById('product-grid');
            grid.innerHTML = list.map(p => {
                let themeControls = '';
                if (p.isWallet) {
                    themeControls = `
                        <div class="theme-select-box">
                            <label>Theme Option:</label>
                            <select id="theme-${p.id}" onchange="handleThemeChange(${p.id})">
                                ${walletThemes.map(t => `<option value="${t}">${t}</option>`).join('')}
                            </select>
                            
                            <div id="sub-team-container-${p.id}" style="display: none;">
                                <label>Choose Football Club:</label>
                                <select id="team-${p.id}">
                                    ${footballTeams.map(ft => `<option value="${ft}">${ft}</option>`).join('')}
                                </select>
                            </div>

                            <div id="sub-marvel-container-${p.id}" style="display: none;">
                                <label>Select Superhero:</label>
                                <select id="marvel-${p.id}">
                                    ${marvelHeroes.map(m => `<option value="${m}">${m}</option>`).join('')}
                                </select>
                            </div>

                            <div id="sub-car-container-${p.id}" style="display: none;">
                                <label>Select Car Model:</label>
                                <select id="car-${p.id}">
                                    ${carModels.map(c => `<option value="${c}">${c}</option>`).join('')}
                                </select>
                            </div>

                            <div id="sub-bike-container-${p.id}" style="display: none;">
                                <label>Select Bike Model:</label>
                                <select id="bike-${p.id}">
                                    ${bikeModels.map(b => `<option value="${b}">${b}</option>`).join('')}
                                </select>
                            </div>

                            <div id="custom-container-${p.id}" style="display: none;">
                                ${renderCanvasControls(p.id)}
                            </div>
                        </div>
                    `;
                } else if (p.isCustomDdakji) {
                    themeControls = `
                        <div class="theme-select-box">
                            <label>Custom Ddakji Design:</label>
                            ${renderCanvasControls(p.id)}
                        </div>
                    `;
                }

                return `
                    <div class="card" id="card-${p.id}">
                        <div>
                            <div class="card-img-wrapper">
                                <img id="card-main-img-${p.id}" src="${p.image}" alt="${p.name}">
                            </div>
                            <h4>${p.name}</h4>
                            <div class="price">₹${p.price}</div>
                            ${themeControls}
                        </div>
                        <div class="btn-group">
                            <button class="btn-add" onclick="addToCart(${p.id})">Add to Cart</button>
                            <button class="btn-buy" onclick="buyNow(${p.id})">Buy Now</button>
                        </div>
                    </div>
                `;
            }).join('');

            list.forEach(p => {
                if (p.isCustomDdakji) initCanvas(p.id);
            });
        }

        function renderCanvasControls(id) {
            return `
                <div class="canvas-container">
                    <label style="font-size:10px; font-weight:bold; color:#666;">Draw or Upload Picture Below:</label>
                    <canvas id="canvas-${id}" width="220" height="110"></canvas>
                    
                    <div class="color-palette">
                        <span style="font-size:10px; font-weight:bold;">Color:</span>
                        ${availableColors.map((c, i) => `<div class="color-swatch ${i===0?'active':''}" style="background:${c};" onclick="setPenColor(${id}, '${c}', this)"></div>`).join('')}
                    </div>

                    <input type="file" id="file-${id}" accept="image/*" onchange="importImageToCanvas(${id}, event)" style="font-size:10px; margin-top:4px; width:100%;">
                    
                    <button class="btn-tool btn-clear" id="btn-clear-${id}" onclick="clearCanvas(${id})">Clear Drawing</button>
                    <button class="btn-tool btn-lock" id="btn-lock-${id}" onclick="lockCanvas(${id})">🔒 Lock Picture Permanent</button>
                </div>
            `;
        }

        renderProducts(products);

        function filterProducts() {
            const query = document.getElementById('searchInput').value.toLowerCase();
            const filtered = products.filter(p => p.name.toLowerCase().includes(query));
            renderProducts(filtered);
        }

        function initCanvas(id) {
            const canvas = document.getElementById(`canvas-${id}`);
            if (!canvas || canvasStates[id]) return;
            const ctx = canvas.getContext('2d');
            let drawing = false;

            canvasStates[id] = { canvas, ctx, color: availableColors[0], locked: false, loadedSrc: null };

            function getPos(e) {
                const rect = canvas.getBoundingClientRect();
                const clientX = e.touches ? e.touches[0].clientX : e.clientX;
                const clientY = e.touches ? e.touches[0].clientY : e.clientY;
                return { x: clientX - rect.left, y: clientY - rect.top };
            }

            function startDraw(e) {
                if (canvasStates[id].locked) return;
                drawing = true;
                const pos = getPos(e);
                ctx.beginPath();
                ctx.moveTo(pos.x, pos.y);
            }

            function draw(e) {
                if (!drawing || canvasStates[id].locked) return;
                const pos = getPos(e);
                ctx.lineWidth = 3;
                ctx.lineCap = 'round';
                ctx.strokeStyle = canvasStates[id].color;
                ctx.lineTo(pos.x, pos.y);
                ctx.stroke();
            }

            function stopDraw() {
                drawing = false;
                ctx.beginPath();
            }

            canvas.addEventListener('mousedown', startDraw);
            canvas.addEventListener('mousemove', draw);
            canvas.addEventListener('mouseup', stopDraw);
            canvas.addEventListener('mouseleave', stopDraw);

            canvas.addEventListener('touchstart', startDraw);
            canvas.addEventListener('touchmove', draw);
            canvas.addEventListener('touchend', stopDraw);

            loadSavedPicture(id);
        }

        function setPenColor(id, color, elem) {
            if (canvasStates[id]) {
                canvasStates[id].color = color;
                const parent = elem.parentElement;
                parent.querySelectorAll('.color-swatch').forEach(s => s.classList.remove('active'));
                elem.classList.add('active');
            }
        }

        function importImageToCanvas(id, event) {
            if (canvasStates[id] && canvasStates[id].locked) return alert('Locked permanent!');
            const file = event.target.files[0];
            if (!file) return;

            const reader = new FileReader();
            reader.onload = function(e) {
                const imgData = e.target.result;
                const img = new Image();
                img.onload = function() {
                    const { canvas, ctx } = canvasStates[id];
                    ctx.clearRect(0, 0, canvas.width, canvas.height);
                    ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
                    canvasStates[id].loadedSrc = imgData;
                };
                img.src = imgData;
            };
            reader.readAsDataURL(file);
        }

        function lockCanvas(id) {
            if (!canvasStates[id]) return;
            const state = canvasStates[id];
            state.locked = true;

            const finalImageSrc = state.canvas.toDataURL();
            localStorage.setItem(`craftsmith_public_locked_pic_${id}`, finalImageSrc);
            applyPublicLockUI(id, finalImageSrc);
            alert('Picture locked permanent and saved!');
        }

        function clearCanvas(id) {
            if (canvasStates[id] && !canvasStates[id].locked) {
                canvasStates[id].ctx.clearRect(0, 0, 220, 110);
                canvasStates[id].loadedSrc = null;
                const fileInput = document.getElementById(`file-${id}`);
                if (fileInput) fileInput.value = '';
            }
        }

        function applyPublicLockUI(id, imgSrc) {
            const mainCardImg = document.getElementById(`card-main-img-${id}`);
            const lockBtn = document.getElementById(`btn-lock-${id}`);
            const clearBtn = document.getElementById(`btn-clear-${id}`);
            const fileInput = document.getElementById(`file-${id}`);

            if (mainCardImg) mainCardImg.src = imgSrc;

            if (lockBtn) {
                lockBtn.disabled = true;
                lockBtn.innerText = "🔒 Locked Permanent";
            }
            if (clearBtn) clearBtn.disabled = true;
            if (fileInput) fileInput.disabled = true;
        }

        function loadSavedPicture(id) {
            const savedData = localStorage.getItem(`craftsmith_public_locked_pic_${id}`);
            if (savedData && canvasStates[id]) {
                canvasStates[id].locked = true;
                const img = new Image();
                img.onload = function() {
                    canvasStates[id].ctx.drawImage(img, 0, 0);
                };
                img.src = savedData;
                applyPublicLockUI(id, savedData);
            }
        }

        function handleThemeChange(productId) {
            const themeVal = document.getElementById(`theme-${productId}`).value;
            
            const teamBox = document.getElementById(`sub-team-container-${productId}`);
            const marvelBox = document.getElementById(`sub-marvel-container-${productId}`);
            const carBox = document.getElementById(`sub-car-container-${productId}`);
            const bikeBox = document.getElementById(`sub-bike-container-${productId}`);

            if (teamBox) teamBox.style.display = themeVal.includes("Football") ? "block" : "none";
            if (marvelBox) marvelBox.style.display = themeVal.includes("Limited Edition") ? "block" : "none";
            if (carBox) carBox.style.display = themeVal.includes("Cars") ? "block" : "none";
            if (bikeBox) bikeBox.style.display = themeVal.includes("Bikes") ? "block" : "none";

            const isCustom = themeVal.includes("Custom");
            const customBox = document.getElementById(`custom-container-${productId}`);
            if (customBox) {
                customBox.style.display = isCustom ? "block" : "none";
                if (isCustom) initCanvas(productId);
            }
        }

        function getSelectedProductDetails(productId) {
            const product = products.find(p => p.id === productId);
            let details = `${product.name}`;

            const themeSelect = document.getElementById(`theme-${productId}`);
            if (themeSelect) {
                const themeVal = themeSelect.value;
                details += ` (${themeVal}`;

                if (themeVal.includes("Football")) {
                    details += ` - ${document.getElementById(`team-${productId}`).value}`;
                } else if (themeVal.includes("Limited Edition")) {
                    details += ` - ${document.getElementById(`marvel-${productId}`).value}`;
                } else if (themeVal.includes("Cars")) {
                    details += ` - ${document.getElementById(`car-${productId}`).value}`;
                } else if (themeVal.includes("Bikes")) {
                    details += ` - ${document.getElementById(`bike-${productId}`).value}`;
                }
                details += `)`;
            }
            
            const isPictureLocked = localStorage.getItem(`craftsmith_public_locked_pic_${productId}`);
            if (isPictureLocked) {
                details += ` [Custom Locked Artwork Attached]`;
            }
            return { product, details };
        }

        /* AUTH MODAL HANDLERS */
        function toggleAuthMode() {
            isSignUpMode = !isSignUpMode;
            document.getElementById('authTitle').innerText = isSignUpMode ? "Create Account" : "Sign In";
            document.getElementById('authSubmitBtn').innerText = isSignUpMode ? "Register" : "Sign In";
            document.getElementById('nameGroup').style.display = isSignUpMode ? "block" : "none";
            document.getElementById('authToggle').innerText = isSignUpMode ? "Already have an account? Sign In" : "New to Craft Smith? Create an account";
        }

        function handleAuth() {
            const email = document.getElementById('authEmail').value;
            if (!email) return alert('Please enter your email!');

            currentUser = isSignUpMode ? document.getElementById('authName').value || "Customer" : email.split('@')[0];
            document.getElementById('userGreeting').innerText = `Hi, ${currentUser}`;
            document.getElementById('userGreeting').style.display = "inline";
            document.getElementById('loginHeaderBtn').style.display = "none";
            document.getElementById('custName').value = currentUser;
            
            closeModal('authModal');
            alert(isSignUpMode ? `Welcome to Craft Smith, ${currentUser}!` : `Signed in successfully as ${currentUser}`);
        }

        /* CART & CHECKOUT */
        function addToCart(productId) {
            const { product, details } = getSelectedProductDetails(productId);
            cartItems.push({ ...product, details });
            document.getElementById('cart-count').innerText = cartItems.length;
            alert(`Added to Cart!\n${details}`);
        }

        function buyNow(productId) {
            const { product, details } = getSelectedProductDetails(productId);
            currentCheckoutProduct = { ...product, details };
            
            document.getElementById('buyProductDetails').innerText = details + ` — ₹${product.price}`;
            document.getElementById('summaryPrice').innerText = `₹${product.price}`;
            updateShipping();
            openModal('buyModal');
        }

        function updateShipping() {
            const shipping = parseInt(document.getElementById('custLocation').value) || 30;
            const price = currentCheckoutProduct ? currentCheckoutProduct.price : 0;
            document.getElementById('summaryShipping').innerText = `₹${shipping}`;
            document.getElementById('summaryTotal').innerText = `₹${price + shipping}`;
        }

        function openCartModal() {
            const cartList = document.getElementById('cartList');
            if (cartItems.length === 0) {
                cartList.innerHTML = '<p style="color:#888;">Your cart is currently empty.</p>';
                document.getElementById('cartSubtotal').innerText = '₹0';
            } else {
                let subtotal = 0;
                cartList.innerHTML = cartItems.map((item, idx) => {
                    subtotal += item.price;
                    return `<div style="border-bottom:1px solid #eee; padding:6px 0;"><strong>${idx+1}. ${item.details}</strong><br><span style="color:#28a745; font-weight:bold;">₹${item.price}</span></div>`;
                }).join('');
                document.getElementById('cartSubtotal').innerText = `₹${subtotal}`;
            }
            openModal('cartModal');
        }

        function checkoutCart() {
            if (cartItems.length === 0) return alert('Your cart is empty!');
            const subtotal = cartItems.reduce((acc, i) => acc + i.price, 0);
            currentCheckoutProduct = { price: subtotal, details: `${cartItems.length} items from Cart` };
            closeModal('cartModal');
            document.getElementById('buyProductDetails').innerText = `${cartItems.length} Items Subtotal — ₹${subtotal}`;
            document.getElementById('summaryPrice').innerText = `₹${subtotal}`;
            updateShipping();
            openModal('buyModal');
        }

        function confirmOrder() {
            const name = document.getElementById('custName').value;
            const address = document.getElementById('custAddress').value;
            if (!name || !address) return alert('Please enter your Name and Address to complete order!');
            
            alert(`Order Placed Successfully!\n\nThank you ${name}. Your paper crafts will be delivered to:\n${address}`);
            cartItems = [];
            document.getElementById('cart-count').innerText = 0;
            closeModal('buyModal');
        }

        function openModal(id) {
            document.getElementById(id).style.display = 'flex';
        }

        function closeModal(id) {
            document.getElementById(id).style.display = 'none';
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
