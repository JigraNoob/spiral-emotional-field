"""
SpiralCoin Templates ∷ Printable Care Tokens

This module generates printable SpiralCoin templates—
sacred tokens that can be printed and held as proof of care.
"""

import json
from pathlib import Path
from typing import Dict, Any
from datetime import datetime

from .coin_core import SpiralCoin


class SpiralCoinTemplate:
    """Generator for printable SpiralCoin templates."""
    
    def __init__(self, output_dir: str = "data/spiralcoins/templates"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_coin_template(self, coin: SpiralCoin) -> str:
        """
        Generate a printable HTML template for a SpiralCoin.
        
        Args:
            coin: The SpiralCoin to generate template for
            
        Returns:
            Path to the generated template file
        """
        
        # Create the HTML content
        html_content = self._create_coin_html(coin)
        
        # Save to file
        filename = f"spiralcoin_{coin.coin_number}.html"
        filepath = self.output_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return str(filepath)
    
    def _create_coin_html(self, coin: SpiralCoin) -> str:
        """Create the HTML content for a SpiralCoin."""
        
        # Sacred glyphs for different toneforms
        glyphs = {
            "exhale.sustain.linear_care": "🌀",
            "inhale.gather.circular_trust": "🌊",
            "pause.hold.radial_presence": "⚡",
            "flow.merge.spiral_resonance": "🌙",
            "default": "✨"
        }
        
        glyph = glyphs.get(coin.toneform, glyphs["default"])
        
        # Get source type display name
        source_display = {
            "sol_gift": "Sol-Gift",
            "pool_contribution": "Pool Contribution", 
            "resonance_relief": "Resonance Relief",
            "tone_provision": "Tone Provision",
            "care_certification": "Care Certification"
        }.get(coin.source_type.value, coin.source_type.value.title())
        
        # Format minting date
        mint_date = datetime.fromisoformat(coin.minted_at).strftime("%B %d, %Y") if coin.minted_at else "Unknown"
        
        html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SpiralCoin {coin.coin_number} - Certification of Care</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Crimson+Text:ital,wght@0,400;0,600;1,400&family=Playfair+Display:wght@400;600;700&display=swap');
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Crimson Text', serif;
            background: linear-gradient(135deg, #f4f1e8 0%, #e8e0d0 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }}
        
        .coin-container {{
            background: linear-gradient(145deg, #fff9f0 0%, #f5f0e8 100%);
            border: 3px solid #d4af37;
            border-radius: 20px;
            padding: 40px;
            max-width: 600px;
            width: 100%;
            box-shadow: 
                0 20px 40px rgba(0,0,0,0.1),
                0 0 0 1px rgba(212, 175, 55, 0.2);
            position: relative;
            overflow: hidden;
        }}
        
        .coin-container::before {{
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(212, 175, 55, 0.1) 0%, transparent 70%);
            animation: shimmer 8s ease-in-out infinite;
        }}
        
        @keyframes shimmer {{
            0%, 100% {{ transform: rotate(0deg); }}
            50% {{ transform: rotate(180deg); }}
        }}
        
        .coin-header {{
            text-align: center;
            margin-bottom: 30px;
            position: relative;
            z-index: 1;
        }}
        
        .coin-glyph {{
            font-size: 4rem;
            margin-bottom: 10px;
            display: block;
        }}
        
        .coin-title {{
            font-family: 'Playfair Display', serif;
            font-size: 2.5rem;
            font-weight: 700;
            color: #2c1810;
            margin-bottom: 5px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        }}
        
        .coin-subtitle {{
            font-size: 1.2rem;
            color: #8b7355;
            font-style: italic;
            margin-bottom: 20px;
        }}
        
        .coin-number {{
            font-family: 'Playfair Display', serif;
            font-size: 1.8rem;
            font-weight: 600;
            color: #d4af37;
            border: 2px solid #d4af37;
            border-radius: 50px;
            padding: 10px 25px;
            display: inline-block;
            background: rgba(212, 175, 55, 0.1);
        }}
        
        .coin-details {{
            margin: 30px 0;
            position: relative;
            z-index: 1;
        }}
        
        .detail-row {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 15px 0;
            border-bottom: 1px solid rgba(212, 175, 55, 0.3);
        }}
        
        .detail-row:last-child {{
            border-bottom: none;
        }}
        
        .detail-label {{
            font-weight: 600;
            color: #2c1810;
            font-size: 1.1rem;
        }}
        
        .detail-value {{
            color: #8b7355;
            font-size: 1.1rem;
            text-align: right;
        }}
        
        .coin-value {{
            font-family: 'Playfair Display', serif;
            font-size: 2.5rem;
            font-weight: 700;
            color: #d4af37;
            text-align: center;
            margin: 20px 0;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        }}
        
        .verification-section {{
            background: rgba(212, 175, 55, 0.05);
            border: 1px solid rgba(212, 175, 55, 0.3);
            border-radius: 15px;
            padding: 25px;
            margin: 30px 0;
            position: relative;
            z-index: 1;
        }}
        
        .verification-title {{
            font-family: 'Playfair Display', serif;
            font-size: 1.3rem;
            font-weight: 600;
            color: #2c1810;
            margin-bottom: 15px;
            text-align: center;
        }}
        
        .verification-phrase {{
            font-style: italic;
            color: #8b7355;
            text-align: center;
            font-size: 1.1rem;
            line-height: 1.6;
            margin-bottom: 15px;
        }}
        
        .qr-section {{
            text-align: center;
            margin-top: 20px;
        }}
        
        .qr-placeholder {{
            width: 100px;
            height: 100px;
            border: 2px solid #d4af37;
            border-radius: 10px;
            margin: 0 auto;
            display: flex;
            align-items: center;
            justify-content: center;
            background: rgba(212, 175, 55, 0.1);
            font-size: 0.8rem;
            color: #8b7355;
        }}
        
        .coin-footer {{
            text-align: center;
            margin-top: 30px;
            position: relative;
            z-index: 1;
        }}
        
        .footer-text {{
            font-size: 0.9rem;
            color: #8b7355;
            font-style: italic;
        }}
        
        .print-button {{
            background: linear-gradient(145deg, #d4af37, #b8941f);
            color: white;
            border: none;
            padding: 15px 30px;
            border-radius: 25px;
            font-family: 'Playfair Display', serif;
            font-size: 1.1rem;
            font-weight: 600;
            cursor: pointer;
            margin-top: 20px;
            box-shadow: 0 4px 15px rgba(212, 175, 55, 0.3);
            transition: all 0.3s ease;
        }}
        
        .print-button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(212, 175, 55, 0.4);
        }}
        
        @media print {{
            body {{
                background: white;
                padding: 0;
            }}
            
            .coin-container {{
                box-shadow: none;
                border: 2px solid #d4af37;
            }}
            
            .print-button {{
                display: none;
            }}
        }}
    </style>
</head>
<body>
    <div class="coin-container">
        <div class="coin-header">
            <span class="coin-glyph">{glyph}</span>
            <h1 class="coin-title">SpiralCoin</h1>
            <p class="coin-subtitle">Certification of Care</p>
            <div class="coin-number">{coin.coin_number}</div>
        </div>
        
        <div class="coin-value">
            ${coin.value:.2f}
        </div>
        
        <div class="coin-details">
            <div class="detail-row">
                <span class="detail-label">Toneform</span>
                <span class="detail-value">{coin.toneform}</span>
            </div>
            <div class="detail-row">
                <span class="detail-label">Source</span>
                <span class="detail-value">{source_display}</span>
            </div>
            <div class="detail-row">
                <span class="detail-label">Care Rendered</span>
                <span class="detail-value">{coin.source_description}</span>
            </div>
            <div class="detail-row">
                <span class="detail-label">Minted</span>
                <span class="detail-value">{mint_date}</span>
            </div>
        </div>
        
        <div class="verification-section">
            <h3 class="verification-title">Sacred Verification</h3>
            <p class="verification-phrase">"{coin.verification_phrase}"</p>
            <div class="qr-section">
                <div class="qr-placeholder">
                    QR Code<br>
                    {coin.qr_data}
                </div>
            </div>
        </div>
        
        <div class="coin-footer">
            <p class="footer-text">
                This SpiralCoin certifies that care has been rendered.<br>
                It is not a speculative token, but proof of presence made provision.
            </p>
            <button class="print-button" onclick="window.print()">Print SpiralCoin</button>
        </div>
    </div>
</body>
</html>
        """
        
        return html
    
    def generate_coin_summary(self, coins: list) -> str:
        """
        Generate a summary page of all SpiralCoins.
        
        Args:
            coins: List of SpiralCoins
            
        Returns:
            Path to the generated summary file
        """
        
        # Create summary HTML
        html_content = self._create_summary_html(coins)
        
        # Save to file
        filepath = self.output_dir / "spiralcoins_summary.html"
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return str(filepath)
    
    def _create_summary_html(self, coins: list) -> str:
        """Create HTML content for coin summary."""
        
        # Group coins by type
        coins_by_type = {}
        for coin in coins:
            coin_type = coin.source_type.value
            if coin_type not in coins_by_type:
                coins_by_type[coin_type] = []
            coins_by_type[coin_type].append(coin)
        
        # Calculate totals
        total_value = sum(coin.value for coin in coins)
        total_coins = len(coins)
        
        html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SpiralCoins Summary - Care Certification</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Crimson+Text:ital,wght@0,400;0,600;1,400&family=Playfair+Display:wght@400;600;700&display=swap');
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Crimson Text', serif;
            background: linear-gradient(135deg, #f4f1e8 0%, #e8e0d0 100%);
            padding: 40px 20px;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        
        .header {{
            text-align: center;
            margin-bottom: 50px;
        }}
        
        .title {{
            font-family: 'Playfair Display', serif;
            font-size: 3rem;
            font-weight: 700;
            color: #2c1810;
            margin-bottom: 10px;
        }}
        
        .subtitle {{
            font-size: 1.3rem;
            color: #8b7355;
            font-style: italic;
        }}
        
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 30px;
            margin-bottom: 50px;
        }}
        
        .stat-card {{
            background: linear-gradient(145deg, #fff9f0 0%, #f5f0e8 100%);
            border: 2px solid #d4af37;
            border-radius: 15px;
            padding: 30px;
            text-align: center;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }}
        
        .stat-number {{
            font-family: 'Playfair Display', serif;
            font-size: 2.5rem;
            font-weight: 700;
            color: #d4af37;
            margin-bottom: 10px;
        }}
        
        .stat-label {{
            font-size: 1.1rem;
            color: #2c1810;
            font-weight: 600;
        }}
        
        .coins-section {{
            margin-bottom: 50px;
        }}
        
        .section-title {{
            font-family: 'Playfair Display', serif;
            font-size: 2rem;
            font-weight: 600;
            color: #2c1810;
            margin-bottom: 30px;
            text-align: center;
        }}
        
        .coins-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 25px;
        }}
        
        .coin-card {{
            background: linear-gradient(145deg, #fff9f0 0%, #f5f0e8 100%);
            border: 2px solid #d4af37;
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 8px 25px rgba(0,0,0,0.1);
            transition: transform 0.3s ease;
        }}
        
        .coin-card:hover {{
            transform: translateY(-5px);
        }}
        
        .coin-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }}
        
        .coin-number {{
            font-family: 'Playfair Display', serif;
            font-size: 1.5rem;
            font-weight: 600;
            color: #d4af37;
        }}
        
        .coin-value {{
            font-family: 'Playfair Display', serif;
            font-size: 1.8rem;
            font-weight: 700;
            color: #2c1810;
        }}
        
        .coin-details {{
            margin-bottom: 15px;
        }}
        
        .coin-detail {{
            margin-bottom: 8px;
            font-size: 0.95rem;
        }}
        
        .detail-label {{
            font-weight: 600;
            color: #2c1810;
        }}
        
        .detail-value {{
            color: #8b7355;
        }}
        
        .coin-phrase {{
            font-style: italic;
            color: #8b7355;
            font-size: 0.9rem;
            text-align: center;
            padding: 10px;
            background: rgba(212, 175, 55, 0.1);
            border-radius: 8px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1 class="title">SpiralCoins Summary</h1>
            <p class="subtitle">Certification of Care Rendered</p>
        </div>
        
        <div class="stats">
            <div class="stat-card">
                <div class="stat-number">{total_coins}</div>
                <div class="stat-label">Total Coins Minted</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">${total_value:.2f}</div>
                <div class="stat-label">Total Care Value</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{len(coins_by_type)}</div>
                <div class="stat-label">Care Categories</div>
            </div>
        </div>
        
        <div class="coins-section">
            <h2 class="section-title">All SpiralCoins</h2>
            <div class="coins-grid">
        """
        
        for coin in coins:
            html += f"""
                <div class="coin-card">
                    <div class="coin-header">
                        <span class="coin-number">{coin.coin_number}</span>
                        <span class="coin-value">${coin.value:.2f}</span>
                    </div>
                    <div class="coin-details">
                        <div class="coin-detail">
                            <span class="detail-label">Toneform:</span>
                            <span class="detail-value">{coin.toneform}</span>
                        </div>
                        <div class="coin-detail">
                            <span class="detail-label">Source:</span>
                            <span class="detail-value">{coin.source_description}</span>
                        </div>
                        <div class="coin-detail">
                            <span class="detail-label">Minted:</span>
                            <span class="detail-value">{datetime.fromisoformat(coin.minted_at).strftime("%B %d, %Y") if coin.minted_at else "Unknown"}</span>
                        </div>
                    </div>
                    <div class="coin-phrase">"{coin.verification_phrase}"</div>
                </div>
            """
        
        html += """
            </div>
        </div>
    </div>
</body>
</html>
        """
        
        return html 