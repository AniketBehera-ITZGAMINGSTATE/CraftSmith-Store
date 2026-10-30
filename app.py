import os
from flask import Flask, render_template_string

app = Flask(__name__)

HTML_CONTENT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Craft Smith: India's Paper Craft Store</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: Roboto, Arial, sans-serif; }
        body { background-color: #f1f2f6; color: #212121; padding-bottom: 40px; }
        .domain-bar { background-color: #1e293b; color: #94a3b8; font-size: 12px; padding: 6px 16px; text-align: center; }
        .domain-bar span.lock { color: #10b981; font-weight: bold; }
        header { background-color: #2874f0; color: white; padding: 12px 10%; display: flex; align-items: center; justify-content: space-between; gap: 20px; }
        .logo { font-size: 22px; font-weight: bold; font-style: italic; }
        .search-bar { display: flex; flex: 1; max-width: 500px; }
        .search-bar input { width: 100%; padding: 8px 12px; border: none; border-radius: 2px 0 0 2px; outline: none; }
        .search-bar button { background: #ffe500; border: none; padding: 8px 16px; cursor: pointer; font-weight: bold; color: #2874f0; border-radius: 0 2px 2px 0; }
        .nav-categories { background: white; display: flex; justify-content: center; gap: 30px; padding: 12px; box-shadow: 0 1px 2px rgba(0,0,0,0.1); font-size: 14px; font-weight: 500; }
        .container { max-width: 1200px; margin: 20px auto; padding: 0 15px; }
        .banner { background: #172337; color: white; padding: 25px; border-radius: 4px; margin-bottom: 20px; text-align: center; }
        .banner h2 { color: #ffe500; font-size: 24px; margin-bottom: 5px; }
        .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 15px; }
        .card { background: white; border-radius: 4px; padding: 15px; text-align: center; border: 1px solid #e0e0e0; display: flex; flex-direction: column; justify-content: space-between; transition: transform 0.2s; }
        .card:hover { transform: translateY(-3px); box-shadow: 0 4px 8px rgba(0,0,0,0.1); }
        .card img { width: 100%; height: 160px; object-fit: cover; border-radius: 4px; margin-bottom: 10px; }
        .card h4 { font-size: 15px; margin-bottom: 6px; }
        .card .price { font-size: 16px; font-weight: bold; color: #388e3c; }
        .btn-add { background: #ff9f00; color: white; border: none; padding: 8px 14px; margin-top: 10px; border-radius: 2px; cursor: pointer; font-weight: bold; width: 100%; }
        .btn-add:hover { background: #e68f00; }
    </style>
</head>
<body>

    <div class="domain-bar">
        🔒 <span class="lock">SSL Secure</span> Web Address: <strong>https://craftsmith-store.onrender.com</strong>
    </div>

    <header>
        <div class="logo">Craft Smith</div>
        <div class="search-bar">
            <input type="text" placeholder="Search paper wallets, slinky, origami...">
            <button>Search</button>
        </div>
        <div>
            <button style="background: white; color: #2874f0; border: none; padding: 6px 20px; font-weight: bold; border-radius: 2px; cursor: pointer;">Sign In</button>
        </div>
    </header>

    <div class="nav-categories">
        <span>💳 Wallets & Card Holders</span>
        <span>🌀 Paper Slinky</span>
        <span>✈️ Origami Airplanes</span>
        <span>🎯 Korean Ddakji</span>
    </div>

    <div class="container">
        <div class="banner">
            <h2>Craft Smith Premium Paper Collection</h2>
            <p>Handcrafted Paper Crafts — Flat rates starting at ₹10!</p>
        </div>

        <h3 style="margin-bottom: 15px;">Trending Paper Crafts</h3>
        <div class="grid" id="product-grid"></div>
    </div>

    <script>
        const products = [
            { 
                id: 1, 
                name: "Paper Wallet (Classic Bifold)", 
                price: 10, 
                image: "https://images.unsplash.com/photo-1627123424574-724758594e93?w=500&auto=format&fit=crop&q=80" 
            },
            { 
                id: 2, 
                name: "Rainbow Paper Slinky", 
                price: 30, 
                image: "https://images.unsplash.com/photo-1513519245088-0e12902e5a38?w=500&auto=format&fit=crop&q=80" 
            },
            { 
                id: 3, 
                name: "Origami Super Glider Airplane", 
                price: 10, 
                image: "https://images.unsplash.com/photo-1517976487492-5750f3195933?w=500&auto=format&fit=crop&q=80" 
            },
            { 
                id: 4, 
                name: "Korean Ddakji Battle Tile", 
                price: 10, 
                image: "https://images.unsplash.com/photo-1544816155-12df9643f363?w=500&auto=format&fit=crop&q=80" 
            }
        ];

        const grid = document.getElementById('product-grid');
        grid.innerHTML = products.map(p => `
            <div class="card">
                <img src="${p.image}" alt="${p.name}">
                <h4>${p.name}</h4>
                <div>
                    <span class="price">₹${p.price}</span>
                </div>
                <button class="btn-add" onclick="alert('Added ' + p.name + ' to cart!')">Add to Cart</button>
            </div>
        `).join('');
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
