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
        header { background-color: #2874f0; color: white; padding: 12px 8%; display: flex; align-items: center; justify-content: space-between; sticky: top; z-index: 100; }
        .logo { font-size: 22px; font-weight: bold; font-style: italic; }
        
        .cart-icon-btn { background: #ffe500; color: #2874f0; border: none; padding: 8px 16px; font-weight: bold; border-radius: 4px; cursor: pointer; }
        
        .container { max-width: 1200px; margin: 20px auto; padding: 0 15px; }
        .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 20px; }
        .card { background: white; border-radius: 8px; padding: 15px; text-align: center; border: 1px solid #e0e0e0; display: flex; flex-direction: column; justify-content: space-between; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }
        .card:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
        
        .card img { width: 100%; height: 180px; object-fit: contain; border-radius: 6px; margin-bottom: 10px; background: #fafafa; border: 1px solid #eee; }
        .card h4 { font-size: 16px; margin-bottom: 6px; }
        .card .price { font-size: 18px; font-weight: bold; color: #28a745; margin-bottom: 8px; }
        
        .theme-select-box { display: flex; flex-direction: column; gap: 6px; margin: 8px 0; text-align: left; }
        .theme-select-box label { font-size: 11px; font-weight: bold; color: #555; text-transform: uppercase; }
        .theme-select-box select, .theme-select-box input { width: 100%; padding: 6px; border: 1px solid #ccc; border-radius: 4px; font-size: 12px; outline: none; }
        
        canvas { border: 1px dashed #888; background: #fff; cursor: crosshair; margin-top: 4px; border-radius: 4px; }
        .btn-clear { background: #dc3545; color: white; border: none; padding: 4px 8px; font-size: 10px; border-radius: 3px; cursor: pointer; margin-top: 4px; }
        
        .btn-group { display: flex; gap: 8px; margin-top: 10px; }
        .btn-add { background: #ff9f00; color: white; border: none; padding: 9px; border-radius: 4px; cursor: pointer; font-weight: bold; flex: 1; font-size: 13px; }
        .btn-buy { background: #fb641b; color: white; border: none; padding: 9px; border-radius: 4px; cursor: pointer; font-weight: bold; flex: 1; font-size: 13px; }
        .btn-add:hover { background: #e68f00; }
        .btn-buy:hover { background: #e0530f; }

        /* AMAZON-STYLE POPUP MODALS */
        .modal-overlay { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.6); display: none; justify-content: center; align-items: center; z-index: 1000; }
        .modal-box { background: white; padding: 24px; border-radius: 8px; width: 90%; max-width: 480px; box-shadow: 0 5px 20px rgba(0,0,0,0.2); position: relative; }
        .modal-box h3 { margin-bottom: 15px; color: #111; font-size: 18px; border-bottom: 1px solid #eee; padding-bottom: 8px; }
        .modal-box .close-btn { position: absolute; top: 12px; right: 16px; font-size: 20px; cursor: pointer; color: #888; }
        .form-group { margin-bottom: 12px; text-align: left; }
        .form-group label { display: block; font-size: 12px; font-weight: bold; margin-bottom: 4px; color: #444; }
        .form-group input, .form-group select { width: 100%; padding: 8px; border: 1px solid #ccc; border-radius: 4px; font-size: 13px; }
        .summary-row { display: flex; justify-content: space-between; font-size: 14px; margin: 8px 0; }
        .total-row { font-size: 16px; font-weight: bold; border-top: 1px solid #ddd; padding-top: 8px; margin-top: 8px; color: #2874f0; }
        .btn-confirm { background: #2874f0; color: white; border: none; padding: 10px; width: 100%; border-radius: 4px; font-size: 15px; font-weight: bold; cursor: pointer; margin-top: 12px; }
    </style>
</head>
<body>

    <header>
        <div class="logo">Craft Smith</div>
        <button class="cart-icon-btn" onclick="openCartModal()">🛒 Cart (<span id="cart-count">0</span>)</button>
    </header>

    <div class="container">
        <h3 style="margin-bottom: 15px; color: #333;">Handcrafted Paper Collection</h3>
        <div class="grid" id="product-grid"></div>
    </div>

    <!-- BUY NOW / CHECKOUT POPUP MODAL -->
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
                <label>Delivery Location (Select to calculate shipping charge)</label>
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

    <!-- CART POPUP MODAL -->
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

        const themes = [
            "1. Pokémon",
            "2. Football",
            "3. Limited Edition- 2026-27",
            "4. Space",
            "5. Custom (Draw below)",
            "6. Barbie",
            "7. Hello Kitty",
            "8. Cute Smiley",
            "9. Cinnamoroll",
            "10. Kuromi",
            "11. My Melody",
            "12. Cars",
            "13. Bikes"
        ];

        // Clean encoded inline SVG illustrations matching uploaded screenshots
        const imgCardHolderWallet = "data:image/svg+xml;charset=utf-8,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 500 320' fill='%23ffffff' stroke='%23d0d0d0' stroke-width='2'%3E%3Crect x='10' y='10' width='480' height='300' rx='4' fill='%23fafafa'/%3E%3Crect x='30' y='30' width='440' height='50' fill='%23e6ecef' stroke='%23bcc4ca'/%3E%3Ctext x='180' y='60' font-size='18' fill='%231b7e46' font-weight='bold' stroke='none'%3E₹500 RESERVE BANK OF INDIA%3C/text%3E%3Crect x='30' y='100' width='440' height='200' fill='%23ffffff' stroke='%23cccccc'/%3E%3Crect x='50' y='140' width='190' height='100' fill='%230f4c81' rx='4'/%3E%3Ctext x='140' y='195' font-size='20' fill='%23ffffff' font-weight='bold' stroke='none'%3EVISA%3C/text%3E%3Crect x='260' y='140' width='190' height='100' fill='%231e1e1e' rx='4'/%3E%3Ctext x='340' y='195' font-size='20' fill='%23ea5b0c' font-weight='bold' stroke='none'%3ERuPay%3C/text%3E%3C/svg%3E";

        const imgDiamondSlotWallet = "data:image/svg+xml;charset=utf-8,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 500 320' fill='%23ffffff' stroke='%23d0d0d0' stroke-width='2'%3E%3Crect x='10' y='10' width='480' height='300' rx='4' fill='%23fafafa'/%3E%3Crect x='30' y='30' width='440' height='50' fill='%23e6ecef' stroke='%23bcc4ca'/%3E%3Ctext x='180' y='60' font-size='18' fill='%231b7e46' font-weight='bold' stroke='none'%3E₹500 RESERVE BANK OF INDIA%3C/text%3E%3Crect x='30' y='100' width='440' height='200' fill='%23ffffff' stroke='%23cccccc'/%3E%3Cpolygon points='50,200 145,110 240,200 145,290' fill='%230f4c81'/%3E%3Cpolygon points='260,200 355,110 450,200 355,290' fill='%231e1e1e'/%3E%3Ctext x='115' y='205' font-size='16' fill='%23ffffff' font-weight='bold' stroke='none'%3EVISA%3C/text%3E%3Ctext x='315' y='205' font-size='16' fill='%23ea5b0c' font-weight='bold' stroke='none'%3ERuPay%3C/text%3E%3C/svg%3E";

        const imgEnvelopeFoldWallet = "data:image/svg+xml;charset=utf-8,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 500 300' fill='none' stroke='%23cccccc' stroke-width='3'%3E%3Crect x='20' y='20' width='140' height='260' fill='%2300a8ff' rx='4'/%3E%3Cpolygon points='20,20 160,20 90,150' fill='%230088cc'/%3E%3Crect x='180' y='20' width='140' height='260' fill='%23e84118' rx='4'/%3E%3Cpolygon points='180,20 320,20 250,150' fill='%23c23616'/%3E%3Crect x='340' y='20' width='140' height='260' fill='%23ffffff' rx='4' stroke='%23b2bec3'/%3E%3Cpolygon points='340,20 480,20 410,150' fill='%23f5f6fa' stroke='%23b2bec3'/%3E%3C/svg%3E";

        const imgDdakjiTile = "data:image/svg+xml;charset=utf-8,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 300 240' fill='none' stroke='%23333' stroke-width='2'%3E%3Crect x='30' y='30' width='110' height='110' fill='%234b7bec'/%3E%3Cpolygon points='30,30 140,140 30,140' fill='%233867d6'/%3E%3Crect x='160' y='30' width='110' height='110' fill='%23eb3b5a'/%3E%3Cpolygon points='160,30 270,140 160,140' fill='%23fc5c65'/%3E%3Ctext x='90' y='200' font-size='16' fill='%23555' stroke='none'%3EKorean Ddakji Battle Tile%3C/text%3E%3C/svg%3E";

        const imgGliderPlaneCombined = "data:image/svg+xml;charset=utf-8,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 500 280' fill='none' stroke='%23555' stroke-width='3'%3E%3Cg transform='translate(20,20)'%3E%3Cpolygon points='100,10 10,230 100,200 190,230' fill='%23ffffff' stroke='%23888'/%3E%3Cline x1='100' y1='10' x2='100' y2='200' stroke='%23888'/%3E%3Ctext x='50' y='255' font-size='13' fill='%23666' stroke='none'%3ETop Fold View%3C/text%3E%3C/g%3E%3Cg transform='translate(240,20)'%3E%3Cpolygon points='10,40 220,130 10,190' fill='%23f5f5f5' stroke='%23888'/%3E%3Cpolygon points='10,40 220,130 30,90' fill='%23ffffff' stroke='%23888'/%3E%3Ctext x='70' y='255' font-size='13' fill='%23666' stroke='none'%3ESide Wing View%3C/text%3E%3C/g%3E%3C/svg%3E";

        const products = [
            { id: 1, name: "Card Holder Paper Wallet", price: 10, isWallet: true, image: imgCardHolderWallet },
            { id: 2, name: "Diamond Slot Paper Wallet", price: 10, isWallet: true, image: imgDiamondSlotWallet },
            { id: 3, name: "Envelope Fold Paper Wallet", price: 10, isWallet: true, image: imgEnvelopeFoldWallet },
            { id: 4, name: "Korean Ddakji Battle Tile", price: 10, isWallet: false, image: imgDdakjiTile },
            { id: 5, name: "Glider Paper Plane (Top & Side Fold)", price: 10, isWallet: false, image: imgGliderPlaneCombined }
        ];

        let cartItems = [];
        let currentCheckoutProduct = null;

        const grid = document.getElementById('product-grid');
        grid.innerHTML = products.map(p => {
            let themeControls = '';
            if (p.isWallet) {
                themeControls = `
                    <div class="theme-select-box">
                        <label>Theme Option:</label>
                        <select id="theme-${p.id}" onchange="handleThemeChange(${p.id})">
                            ${themes.map(t => `<option value="${t}">${t}</option>`).join('')}
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
                            <label>Draw Custom Artwork:</label>
                            <canvas id="canvas-${p.id}" width="220" height="90"></canvas>
                            <button class="btn-clear" onclick="clearCanvas(${p.id})">Clear Canvas</button>
                        </div>
                    </div>
                `;
            }

            return `
                <div class="card">
                    <img src="${p.image}" alt="${p.name}">
                    <h4>${p.name}</h4>
                    <div class="price">₹${p.price}</div>
                    ${themeControls}
                    <div class="btn-group">
                        <button class="btn-add" onclick="addToCart(${p.id})">Add to Cart</button>
                        <button class="btn-buy" onclick="buyNow(${p.id})">Buy Now</button>
                    </div>
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
                ctx.strokeStyle = '#2874f0';
                ctx.lineTo(e.clientX - rect.left, e.clientY - rect.top);
                ctx.stroke();
                ctx.beginPath();
                ctx.moveTo(e.clientX - rect.left, e.clientY - rect.top);
            });
            canvasStates[id] = { canvas, ctx };
        }

        function clearCanvas(id) {
            if (canvasStates[id]) canvasStates[id].ctx.clearRect(0, 0, 220, 90);
        }

        function handleThemeChange(productId) {
            const themeVal = document.getElementById(`theme-${productId}`).value;
            
            document.getElementById(`sub-team-container-${productId}`).style.display = themeVal.includes("Football") ? "block" : "none";
            document.getElementById(`sub-marvel-container-${productId}`).style.display = themeVal.includes("Limited Edition") ? "block" : "none";
            document.getElementById(`sub-car-container-${productId}`).style.display = themeVal.includes("Cars") ? "block" : "none";
            document.getElementById(`sub-bike-container-${productId}`).style.display = themeVal.includes("Bikes") ? "block" : "none";
            
            const isCustom = themeVal.includes("Custom");
            document.getElementById(`custom-container-${productId}`).style.display = isCustom ? "block" : "none";
            if (isCustom) initCanvas(productId);
        }

        function getSelectedProductDetails(productId) {
            const product = products.find(p => p.id === productId);
            let details = `${product.name}`;

            if (product.isWallet) {
                const themeVal = document.getElementById(`theme-${productId}`).value;
                details += ` (${themeVal}`;

                if (themeVal.includes("Football")) {
                    details += ` - ${document.getElementById(`team-${productId}`).value}`;
                } else if (themeVal.includes("Limited Edition")) {
                    details += ` - ${document.getElementById(`marvel-${productId}`).value}`;
                } else if (themeVal.includes("Cars")) {
                    details += ` - ${document.getElementById(`car-${productId}`).value}`;
                } else if (themeVal.includes("Bikes")) {
                    details += ` - ${document.getElementById(`bike-${productId}`).value}`;
                } else if (themeVal.includes("Custom")) {
                    details += ` - Canvas Drawing Attached`;
                }
                details += `)`;
            }
            return { product, details };
        }

        function addToCart(productId) {
            const { product, details } = getSelectedProductDetails(productId);
            cartItems.push({ ...product, details });
            document.getElementById('cart-count').innerText = cartItems.length;
            alert(`Added to Cart!\\n${details}`);
        }

        function buyNow(productId) {
            const { product, details } = getSelectedProductDetails(productId);
            currentCheckoutProduct = { ...product, details };
            
            document.getElementById('buyProductDetails').innerText = details + ` — ₹${product.price}`;
            document.getElementById('summaryPrice').innerText = `₹${product.price}`;
            updateShipping();
            document.getElementById('buyModal').style.display = 'flex';
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
            document.getElementById('cartModal').style.display = 'flex';
        }

        function checkoutCart() {
            if (cartItems.length === 0) return alert('Your cart is empty!');
            const subtotal = cartItems.reduce((acc, i) => acc + i.price, 0);
            currentCheckoutProduct = { price: subtotal, details: `${cartItems.length} items from Cart` };
            closeModal('cartModal');
            document.getElementById('buyProductDetails').innerText = `${cartItems.length} Items Subtotal — ₹${subtotal}`;
            document.getElementById('summaryPrice').innerText = `₹${subtotal}`;
            updateShipping();
            document.getElementById('buyModal').style.display = 'flex';
        }

        function confirmOrder() {
            const name = document.getElementById('custName').value;
            const address = document.getElementById('custAddress').value;
            if (!name || !address) return alert('Please enter your Name and Address to complete order!');
            
            alert(`Order Placed Successfully!\\n\\nThank you ${name}. Your paper crafts will be delivered to:\\n${address}`);
            cartItems = [];
            document.getElementById('cart-count').innerText = 0;
            closeModal('buyModal');
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
